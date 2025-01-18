import time
import board
import neopixel

class Led():    
    def __init__(self):
        # Chọn chân pin kết nối với Data In của NeoPixel
        self.pixel_pin = board.D10
        self.num_pixels = 12
        self.ORDER = neopixel.GRB

        # Khởi tạo đối tượng NeoPixel
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER)

    def wheel(self, pos):
        # Input giá trị từ 0 đến 255 để lấy giá trị màu
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if self.ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def set_color(self, color):
        self.pixels.fill(color)
        self.pixels.show()

# Main function
if __name__ == '__main__':
    led = Led()  # Tạo đối tượng Led

    # Set màu đỏ
    led.set_color((255, 0, 0))  # Nếu sử dụng RGBW, thay thành (255, 0, 0, 0)
    time.sleep(1)

    # Set màu xanh lá
    led.set_color((0, 255, 0))  # Nếu sử dụng RGBW, thay thành (0, 255, 0, 0)
    time.sleep(1)

    # Set màu xanh dương
    led.set_color((0, 0, 255))  # Nếu sử dụng RGBW, thay thành (0, 0, 255, 0)
    time.sleep(1)

    # Hiệu ứng cầu vồng
    led.rainbow_cycle(0.001)  # Chạy vòng cầu vồng với độ trễ 1ms

    # Tắt đèn
    led.set_color((0, 0, 0))  # Nếu sử dụng RGBW, thay thành (0, 0, 0, 0)
    time.sleep(1)
