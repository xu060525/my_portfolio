#!/bin/bash

# --- 配置区 ---
# 你的项目文件夹名字 (请确认是否正确)
PROJECT_DIR="/home/XiQiao/my_portfolio"
# 你的虚拟环境名字 (PA默认通常是 .virtualenvs/你的项目名)
# 如果你不确定，可以在 PA Console 输入 `workon` 看看名字
VENV_NAME="venv"

echo "🚀 开始部署..."

# 1. 进入项目目录
cd $PROJECT_DIR || exit
echo "📂 已进入项目目录: $PWD"

# 2. 拉取最新代码
echo "⬇️ 正在拉取 Git 代码..."
git pull origin main

# 3. 激活虚拟环境 (PA 特有的 source 方式)
echo "🐍 激活虚拟环境..."
source /home/XiQiao/.virtualenvs/$VENV_NAME/bin/activate

# 4. 安装依赖 (如果 requirements.txt 变了)
echo "📦 检查依赖更新..."
pip install -r requirements.txt

# 5. 数据库迁移
echo "🗄️ 执行数据库迁移..."
# 显式指定生产环境配置，防止报错
export DJANGO_SETTINGS_MODULE=my_portfolio.settings.production
python manage.py migrate

# 6. 静态文件
echo "🎨 收集静态文件..."
python manage.py collectstatic --noinput

# 7. 创建缓存表 (保险起见，反正已存在的不报错)
python manage.py createcachetable 2>/dev/null

# 8. 触碰 WSGI 文件以重启 (PA 的黑科技)
# 在 PA 上，只要修改(touch)了 wsgi.py 文件，Web 进程就会自动 Reload
# 注意：你需要确认你的 wsgi.py 的准确路径！
# 通常在 /var/www/你的用户名_pythonanywhere_com_wsgi.py
WSGI_FILE="/var/www/xiqiao_pythonanywhere_com_wsgi.py"

if [ -f "$WSGI_FILE" ]; then
    echo "🔄 正在重启 Web 服务..."
    touch "$WSGI_FILE"
    echo "✅ 部署完成！"
else
    echo "⚠️ 警告: 找不到 WSGI 文件，无法自动 Reload。请手动去 Web 页面点击 Reload。"
    echo "预期路径: $WSGI_FILE"
fi