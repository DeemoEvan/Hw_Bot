import google.generativeai as genai
import os

# 1. 設定你的 API Key
genai.configure(api_key="AIzaSyB6_6T3EMIkS6MTvNvyogVPmFkIcnvl2dA")

# 2. 初始化模型 (目前建議使用 gemini-1.5-flash 或 gemini-1.5-pro)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 生成內容
response = model.generate_content("你好！請用一句話自我介紹。")

print(response.text)