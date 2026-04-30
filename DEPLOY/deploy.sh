#!/bin/bash
# HarmoniSense-LV Professional Deployment Script (Version 2.2)
# Location: PROJECT_ROOT/DEPLOY/deploy.sh

set -e

# --- 1. Environment Detection / 环境路径识别 ---
DEPLOY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$DEPLOY_DIR" )"
SERVICE_NAME="harmonisense"
PORT=8053

echo "------------------------------------------------"
echo "🛠️  Starting HarmoniSense-LV Deployment System..."
echo "🛠️  正在启动 HarmoniSense-LV 自动化部署系统..."
echo "📂 Project Root / 项目根目录: $PROJECT_ROOT"
echo "------------------------------------------------"

# --- 2. System Dependency & Lock Handling / 系统依赖检查与锁处理 ---
echo ">>> Checking system environment / 正在检查系统环境..."

# 尝试安装 python3-venv，这是 Ubuntu 默认缺失的
sudo apt update || echo "⚠️  Apt lock detected, but trying to proceed..."
sudo apt install -y python3-pip python3-venv git || {
    echo "❌ Failed to install system dependencies. Please run 'sudo apt install -y python3-venv' manually."
    exit 1
}

# --- 3. Virtual Env Setup & Cleanup / 虚拟环境清理与创建 ---
echo ">>> Configuring Python environment / 正在配置 Python 虚拟环境..."
cd "$PROJECT_ROOT"

# 如果 venv 存在但没有 bin 目录（说明之前创建失败了），则强制删除重做
if [ -d "venv" ] && [ ! -d "venv/bin" ]; then
    echo "⚠️  Incomplete virtualenv detected. Cleaning up / 发现不完整的虚拟环境，正在清理..."
    rm -rf venv
fi

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install gunicorn

if [ -f "requirements.txt" ]; then
    echo ">>> Installing dependencies from requirements.txt / 正在安装依赖..."
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found, installing defaults / 未发现依赖清单，正在安装默认包..."
    pip install dash dash-bootstrap-components pandas networkx numpy scipy openpyxl
fi

# --- 4. Systemd Service Configuration / 服务配置 ---
echo ">>> Generating Systemd service configuration / 正在生成服务配置..."
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=HarmoniSense-LV Physical AI Diagnostic Dashboard
After=network.target

[Service]
User=$USER
WorkingDirectory=$PROJECT_ROOT
Environment="PATH=$PROJECT_ROOT/venv/bin"
ExecStart=$PROJECT_ROOT/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:$PORT dashboard_app:server --timeout 120
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# --- 5. Activation & Firewall / 启动与防火墙 ---
echo ">>> Activating service / 正在激活服务..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo ">>> Configuring Firewall (Port $PORT) / 配置防火墙 (端口 $PORT)..."
sudo ufw allow $PORT/tcp || true

# --- 6. Summary / 部署结果总结 ---
IP_ADDR=$(curl -s ifconfig.me || echo "SERVER_IP")
echo "------------------------------------------------"
echo "✅ Deployment Successful! / 部署成功！"
echo "🌐 URL: http://$IP_ADDR:$PORT"
echo "📊 Check Status / 查看状态: sudo systemctl status $SERVICE_NAME"
echo "------------------------------------------------"
