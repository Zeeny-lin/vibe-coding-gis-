import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

api_key = os.getenv('DEEPSEEK_API_KEY')
print(f"API Key: {api_key[:10]}...{api_key[-5:]}" if api_key else "API Key not found!")

client = OpenAI(
    api_key=api_key,
    base_url='https://api.siliconflow.cn/v1'
)

try:
    response = client.chat.completions.create(
        model='deepseek-ai/DeepSeek-V3',
        messages=[{'role': 'user', 'content': '你好'}],
        max_tokens=50
    )
    print("Success!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
