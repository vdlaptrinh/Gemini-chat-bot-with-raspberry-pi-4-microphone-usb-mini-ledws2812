from gpiozero import Button
import time

# Cấu hình các chân GPIO cho các nút nhấn
BUTTONS = [5, 25, 6, 26]  # Các chân GPIO cho các nút nhấn

# Hàm xử lý khi nút nhấn
def button_pressed(button):
    if button == 5:
        print("Nút 5 đã được nhấn")
    if button == 25:
        print("Nút 25 đã được nhấn")
    if button == 6:
        print("Nút 6 đã được nhấn")
    if button == 26:
        print("Nút 26 đã được nhấn")
# Khởi tạo và lắng nghe sự kiện cho các nút nhấn
def setup_buttons():
    buttons = {}
    for button in BUTTONS:
        btn = Button(button)  # Khởi tạo nút nhấn
        btn.when_pressed = lambda b=button: button_pressed(b)  # Gắn callback khi nút nhấn
        buttons[button] = btn
    return buttons

def main():
    # Khởi tạo các nút
    buttons = setup_buttons()
    
    print("Chương trình đang chạy, nhấn nút để kiểm tra.")
    
    try:
        while True:
            time.sleep(1)  # Để chương trình không kết thúc ngay lập tức
    except KeyboardInterrupt:
        print("Chương trình kết thúc.")

if __name__ == "__main__":
    main()
