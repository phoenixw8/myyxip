import requests
import re
import json
from collections import OrderedDict

# --- 配置 ---
SOURCE_URL = "https://api.uouin.com/cloudflare.html"
OUTPUT_FILE = "cloudflare_ips.txt"
# 使用免费的 IP-API 进行地理位置查询
GEO_API_URL = "http://ip-api.com/json/"

def get_geo_info(ip):
    """根据IP地址查询国家和国家代码"""
    try:
        response = requests.get(f"{GEO_API_URL}{ip}?lang=zh-CN&fields=country,countryCode")
        response.raise_for_status()
        data = response.json()
        if data.get('countryCode') and data.get('country'):
            return data['countryCode'], data['country']
    except requests.exceptions.RequestException as e:
        print(f"Error querying geo info for {ip}: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON for {ip}")
    return None, None

def country_code_to_flag(code):
    """将两位国家代码转换为国旗 emoji"""
    if not code or len(code) != 2:
        return "❓"
    return "".join(chr(ord(char) - ord('A') + 0x1F1E6) for char in code.upper())

def main():
    """主函数"""
    print("Starting IP collection process...")
    
    try:
        print(f"Fetching IPs from {SOURCE_URL}...")
        response = requests.get(SOURCE_URL, timeout=15)
        response.raise_for_status()
        content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch source URL: {e}")
        return

    ipv4_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ips = ipv4_pattern.findall(content)
    unique_ips = list(OrderedDict.fromkeys(ips))
    
    if not unique_ips:
        print("No IPs found. Exiting.")
        return
        
    print(f"Found {len(unique_ips)} unique IPs. Now fetching geo information...")
    
    formatted_lines = []
    for i, ip in enumerate(unique_ips, 1):
        country_code, country_name = get_geo_info(ip)
        if country_code and country_name:
            flag = country_code_to_flag(country_code)
            line = f"{ip}#{flag} {country_name}"
            print(f"({i}/{len(unique_ips)}) Processed: {line}")
            formatted_lines.append(line)
        else:
            line = f"{ip}#❓ 未知"
            print(f"({i}/{len(unique_ips)}) Failed to get geo for {ip}. Using default.")
            formatted_lines.append(line)

    print(f"Writing {len(formatted_lines)} lines to {OUTPUT_FILE}...")
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(formatted_lines))
        print("Process completed successfully!")
    except IOError as e:
        print(f"Failed to write to file: {e}")

if __name__ == "__main__":
    main()
