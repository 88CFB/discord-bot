import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# 从 .env 文件加载环境变量
load_dotenv(dotenv_path='secret.env')

# Shopee 登录 URL
login_url = "https://shopee.tw/hsu6666"

# 从环境变量中获取用户名和密码
username = os.getenv('SHOPEE_USERNAME')
password = os.getenv('SHOPEE_PASSWORD')

print(f"Username: {username}, Password: {password}")
# Headers 和 Cookies（如果有的话）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    # 添加更多必要的 Headers
}

# 登录表单数据
login_data = {
    "username": username,
    "password": password,
    "captcha": ""  # 如果有验证码，可能需要额外处理
}

# 开始一个 session
session = requests.Session()

# 发送 POST 请求进行登录
response = session.post(login_url, headers=headers, json=login_data)

# 检查响应状态码
print(f"Response status code: {response.status_code}")

# 打印响应内容以调试
print("Response content:", response.text)

# 尝试解析 JSON 响应
try:
    response_json = response.json()
    print("JSON response:", response_json)
except requests.exceptions.JSONDecodeError:
    print("响应不是有效的 JSON 数据")

# 检查响应状态
if response.status_code == 200:
    print("登录成功")
    # 访问一些需要登录才能访问的页面来验证是否成功
    profile_url = login_url
    profile_response = session.get(profile_url, headers=headers)

    if profile_response.status_code == 200:
        print("成功访问受保护页面")
        print(profile_response.json())  # 打印用户信息或其他内容
    else:
        print("访问受保护页面失败")
else:
    print("登录失败")
    print(response.json())  # 打印错误信息

