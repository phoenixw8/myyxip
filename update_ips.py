# 工作流名称
name: Auto Update Cloudflare IPs

# 触发条件
on:
  schedule:
    - cron: '0 * * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    # --- 关键修改：在这里添加权限 ---
    permissions:
      contents: write
    # -----------------------------------

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Run IP updater script
        run: python update_ips.py

      - name: Commit and push changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git diff --staged --quiet || git commit -m "CI: Auto-update Cloudflare IPs"
          git push
