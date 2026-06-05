import urllib.request
import json
import ssl

def test_api():
    url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=25.43&longitude=119.01&current=china_aqi"
    print(f"Testing URL: {url}")
    try:
        # Ignore SSL errors just in case
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(url, context=ctx, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                print("Success! Data received:")
                print(json.dumps(data, indent=2))
            else:
                print(f"Failed with status: {response.status}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
