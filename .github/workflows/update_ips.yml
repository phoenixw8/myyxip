# 工作流名称
name: Auto Update Cloudflare IPs

# 触发条件
on:
  schedule:
    - cron: '0 * * * *'  # 每小时的第0分钟运行
  workflow_dispatch:     # 允许手动触发

jobs:
  build:
    runs-on: ubuntu-latest
    
    # --- 关键：赋予工作流写入仓库的权限 ---
    permissions:
      contents: write

    steps:
      - name: 检出代码 (Checkout repository)
        uses: actions/checkout@v4

      - name: 设置 Python 环境 (Set up Python)
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'

      - name: 安装依赖 (Install dependencies)
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: 运行 IP 更新脚本 (Run IP updater script)
        run: python update_ips.py

      - name: 提交并推送更改 (Commit and push changes)
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          # 下面这行很重要：只有在文件有实际变化时才执行 commit
          git diff --staged --quiet || git commit -m "CI: Auto-update Cloudflare IPs"
          git push
