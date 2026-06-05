import os
import requests
import time

# 目标目录
TARGET_DIR = os.path.join(os.path.dirname(__file__), '../frontend/src/assets/city-cards')
os.makedirs(TARGET_DIR, exist_ok=True)

# 使用更稳定的Wikimedia图片源 (2024年可用链接)
# 使用更稳定的 Unsplash 图片源 (避免 Wikimedia 429 错误)
IMAGES = [
    # 湄洲岛 - 妈祖像 (使用海岛/寺庙替代)
    ("https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?auto=format&fit=crop&q=80&w=800", "meizhou_island.jpg"),
    
    # 广化寺 - 释迦文佛塔 (使用佛塔替代)
    ("https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&q=80&w=800", "guanghua_temple.jpg"),
    
    # 妈祖巡安 - 台湾进香团 (使用传统节日/灯笼替代)
    ("https://images.unsplash.com/photo-1515165592879-1d698095ebf3?auto=format&fit=crop&q=80&w=800", "mazu_culture.jpg"),
    
    # 城市夜景
    ("https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&q=80&w=1200", "city_night.jpg")
]

def download_images():
    print(f"Start downloading {len(IMAGES)} images...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for url, filename in IMAGES:
        save_path = os.path.join(TARGET_DIR, filename)
        # 如果文件已存在且大小正常(>1KB)，跳过
        if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
            print(f"   [Exists] {filename}")
            continue
            
        try:
            print(f"   Downloading: {filename} from {url[:40]}...")
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"   [OK] {filename}")
            else:
                print(f"   [FAIL] {filename} Status: {response.status_code}")
                
        except Exception as e:
            print(f"   [ERROR] {filename}: {e}")
            
    print("\nDownload task processing finished.")

if __name__ == '__main__':
    download_images()
