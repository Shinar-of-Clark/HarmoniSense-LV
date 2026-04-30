#!/bin/bash
# HarmoniSense-LV 工业级自动部署脚本 (Version 2.0)
# 脚本位置: PROJECT_ROOT/DEPLOY/deploy.sh

set -e

# --- 1. 环境路径识别 ---
# 获取脚本所在目录的上一级作为项目根目录
DEPLOY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$DEPLOY_DIR" )"
PROJECT_NAME=$(basename "$PROJECT_ROOT")
SERVICE_NAME="harmonisense"
PORT=8053

echo "------------------------------------------------"
echo "🛠️  正在启动 HarmoniSense-LV 自动化部署系统..."
echo "📂 项目根目录: $PROJECT_ROOT"
echo "------------------------------------------------"

# --- 2. 系统依赖检查 ---
echo ">>> 检查系统环境..."
sudo apt update && sudo apt install -y python3-pip python3-venv git

# --- 3. 虚拟环境与依赖安装 ---
echo ">>> 正在配置 Python 虚拟环境..."
cd "$PROJECT_ROOT"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install gunicorn

# 检查根目录下是否有 requirements.txt，如果没有则安装核心包
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ 未发现 requirements.txt，正在安装默认依赖..."
    pip install dash dash-bootstrap-components pandas networkx numpy scipy openpyxl
fi

# --- 4. 自动生成 Systemd 服务配置 ---
echo ">>> 正在生成 Systemd 守护进程配置..."
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

# --- 5. 启动与防火墙 ---
echo ">>> 正在激活服务..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo ">>> 配置防火墙 (开放端口 $PORT)..."
sudo ufw allow $PORT/tcp || true

# --- 6. 部署结果总结 ---
IP_ADDR=$(curl -s ifconfig.me || echo "SERVER_IP")
echo "------------------------------------------------"
echo "✅ 部署成功！"
echo "🌐 访问地址: http://$IP_ADDR:$PORT"
echo "📊 服务状态: sudo systemctl status $SERVICE_NAME"
echo "------------------------------------------------"
