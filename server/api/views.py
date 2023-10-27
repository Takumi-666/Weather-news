import requests
from api import OPENWEATHER_API_KEY
from django.http import JsonResponse

def get_weather(request):
    # OpenWeather APIキーを設定
    api_key = 'OPENWEATHER_API_KEY'

    # 天気情報を取得したい都市をリストで指定
    cities = ['Sapporo','Niigata', 'Tokyo', 'Osaka','Fukuoka']

    # 必要な情報を格納するリストを初期化
    weather_info = []

    for city in cities:
        # 3時間刻みの6日間の天気予報を取得するためのクエリパラメータを設定、lang=ja を追加して、日本語のデータを取得
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=40&appid={api_key}&units=metric&lang=ja'
        forecast_response = requests.get(url)
        forecast_data = forecast_response.json()

        # 各日の天気情報から必要な情報を抽出
        daily_weather_data = {}
        for data_point in forecast_data['list']:
            date = data_point['dt']  # 日付（UNIXタイムスタンプ）
            date_str = data_point['dt_txt']  # 日付文字列
            max_temp = data_point['main']['temp_max']  # 最高気温
            min_temp = data_point['main']['temp_min']  # 最低気温
            wind_speed = data_point['wind']['speed']  # 風速
            weather_state = data_point['weather'][0]['description']  # 天候
            humidity = data_point['main']['humidity']  # 湿度
            icon_code = data_point['weather'][0]['icon']  # 天気アイコン

            # 日ごとの情報を格納する辞書を初期化
            if date_str.split()[0] not in daily_weather_data:
                daily_weather_data[date_str.split()[0]] = {
                    'date': date,
                    'max_temp': max_temp,
                    'min_temp': min_temp,
                    'wind_speed': wind_speed,
                    'weather_state': weather_state,
                    'humidity': humidity,
                    'icon_code': icon_code,
                    'city': city,  
                }
            else:
                # 日ごとの情報を更新
                daily_weather_data[date_str.split()[0]]['max_temp'] = max(max_temp, daily_weather_data[date_str.split()[0]]['max_temp'])
                daily_weather_data[date_str.split()[0]]['min_temp'] = min(min_temp, daily_weather_data[date_str.split()[0]]['min_temp'])
                daily_weather_data[date_str.split()[0]]['wind_speed'] = max(wind_speed, daily_weather_data[date_str.split()[0]]['wind_speed'])
                daily_weather_data[date_str.split()[0]]['weather_state'] = weather_state
                daily_weather_data[date_str.split()[0]]['humidity'] = max(humidity, daily_weather_data[date_str.split()[0]]['humidity'])
                daily_weather_data[date_str.split()[0]]['icon_code'] = icon_code

        # 日ごとの情報をリストに追加
        for date_str, data in daily_weather_data.items():
            weather_info.append(data)

    return JsonResponse(weather_info, safe=False)
