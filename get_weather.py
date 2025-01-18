import requests
from config import openweather_api_key


def get_weather(city):
    # Địa chỉ API của OpenWeather (API cho thời tiết hiện tại)
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Tham số yêu cầu
    params = {
        'q': city,  # Tên thành phố/quận huyện
        'appid': openweather_api_key,  # API key
        'units': 'metric',  # Đơn vị đo nhiệt độ (metric: độ C)
        'lang': 'vi'  # Ngôn ngữ tiếng Việt
    }
    
    # Gửi yêu cầu GET tới OpenWeather API
    response = requests.get(base_url, params=params)
    
    # Kiểm tra kết quả trả về
    if response.status_code == 200:
        data = response.json()  # Chuyển đổi dữ liệu JSON thành dictionary
        # Các thông tin cần thiết
        city_name = data['name']
        weather_description = data['weather'][0]['description']  # Mô tả thời tiết
        temperature = data['main']['temp']  # Nhiệt độ hiện tại
        pressure = data['main']['pressure']  # Áp suất khí quyển
        humidity = data['main']['humidity']  # Độ ẩm
        cloudiness = data['clouds']['all']  # Mây (tỉ lệ %)
        wind_speed = data['wind']['speed']  # Tốc độ gió

        weather_report = (
            f"Thời tiết tại {city}: "
            f"Nhiệt độ: {temperature}°C, "
            f"{weather_description}. "
            f"Độ ẩm: {humidity}%, "
            f"Áp suất: {pressure} hPa, "
            f"Tỉ lệ mây: {cloudiness}%, "
            f"Tốc độ gió: {wind_speed} m/s. "
        )
        #print(weather_report)
        return weather_report
    else:
        print("Không thể lấy thông tin thời tiết. Vui lòng kiểm tra lại tên thành phố/quận huyện.")
        return "Không thể lấy thông tin thời tiết. Vui lòng kiểm tra lại tên thành phố/quận huyện."


def main():
    # Nhập API key của bạn tại đây

    
    # Nhập tên thành phố/quận huyện từ người dùng
    city = input("Nhập tên thành phố/quận huyện bạn muốn tra cứu thời tiết: ")
    
    # Gọi hàm lấy thông tin thời tiết
    get_weather(city)

if __name__ == "__main__":
    main()
