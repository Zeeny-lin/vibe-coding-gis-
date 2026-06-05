import urllib.request
import json
import ssl

def test_realtime_logic():
    print("Testing Air Quality API...")
    try:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        
        url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=25.43&longitude=119.01&current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone&timezone=Asia%2FShanghai"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                print("Air Quality Data Success:", data['current'])
            else:
                print("Air Quality HTTP", response.status)
    except Exception as e:
        print("Air Quality Failed:", e)

    print("\nTesting Weather API...")
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=25.43&longitude=119.01&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=Asia%2FShanghai&forecast_days=3"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                print("Weather Data Success:", data['current'])
            else:
                print("Weather HTTP", response.status)
    except Exception as e:
        print("Weather Failed:", e)

if __name__ == "__main__":
    test_realtime_logic()
