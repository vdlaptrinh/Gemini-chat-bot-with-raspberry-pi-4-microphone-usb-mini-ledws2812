# Voice-chatbot-Pi-4-Microphone-USB-mini-Led-ws2812
Project Trợ lý ảo Tiếng Việt (giống như google home, alexa, maika...)
- Cần điền api key vào file config.py: picovoive, gemini, HASS IP, LONG TOKEN, my_city, openweather
- Từ khoá đánh thức: picovoice
- Hỏi sau khi nghe ding
- Chào bạn, Mấy giờ rồi
- Tăng âm lượng, giảm âm lượng
- Bật/Tắt đèn xxx, Bật/Tắt quạt xxx, Thực hiện + tên kịch bản
- Mở bài hát + tên bài hát, Mở nhạc + ...
- Thời tiết hôm nay/ Hôm nay có mưa không
- Các Câu hỏi khác sẽ được chuyển đến gemini
- Sau khi phát câu trả lời sẽ nghe dong
- Chế độ hội thoại được bật: cứ hỏi liên tục không cần đánh thức tới khi bạn nói "Chào bạn" hoặc 2 lần loa không nghe gì
- Led có 3 hiệu ứng: wakeup, think, speak và off
- Wakeup: Picovoice
- STT: GG CLOUD V1 hoặc V2 hoặc GG FREE
- TTS: EDGE-TTS

#Phần cứng sử dụng: Raspberry pi4, Microphone USB mini, Loa (AUX), Led WS2812

#Button
- Chương trình có 4 nút nhấn: + - wakeup stop
- tương ứng GPIO 6 26 5 25
- Trong lúc loa đang phát tiếng, có thể bấm nút stop để ngừng
- nút + tăng âm lượng
- nút - giảm âm lượng
- nút wakeup để gọi bot, sau khi nghe ding có thể ra lệnh

#pip list
pi@pi4202412:~ $ pip list
Package                                  Version
---------------------------------------- --------------
Adafruit-Blinka                          8.50.0
adafruit-circuitpython-busdevice         5.2.10
adafruit-circuitpython-connectionmanager 3.1.2
adafruit-circuitpython-neopixel          6.3.13
adafruit-circuitpython-pixelbuf          2.0.6
adafruit-circuitpython-requests          4.1.8
adafruit-circuitpython-typing            1.11.2
Adafruit-PlatformDetect                  3.76.1
Adafruit-PureIO                          1.1.11
aiofiles                                 24.1.0
aiohttp                                  3.8.4
aiosignal                                1.3.2
annotated-types                          0.7.0
anyio                                    4.8.0
async-timeout                            4.0.3
attrs                                    24.3.0
beautifulsoup4                           4.12.3
binho-host-adapter                       0.1.6
blinker                                  1.9.0
cachetools                               5.5.0
certifi                                  2024.12.14
chardet                                  5.1.0
charset-normalizer                       3.0.1
click                                    8.1.8
coloredlogs                              15.0.1
distro                                   1.8.0
edge-tts                                 7.0.0
Flask                                    3.1.0
flatbuffers                              20181003210633
frozenlist                               1.5.0
fuzzywuzzy                               0.18.0
google-ai-generativelanguage             0.6.10
google-api-core                          2.24.0
google-api-python-client                 2.156.0
google-auth                              2.37.0
google-auth-httplib2                     0.2.0
google-cloud                             0.34.0
google-cloud-speech                      2.29.0
google-cloud-texttospeech                2.23.0
google-generativeai                      0.8.3
googleapis-common-protos                 1.66.0
grpcio                                   1.68.1
grpcio-status                            1.68.1
gTTS                                     2.5.4
h11                                      0.14.0
h2                                       4.1.0
hpack                                    4.0.0
httpcore                                 1.0.7
httplib2                                 0.22.0
httpx                                    0.28.1
humanfriendly                            10.0
Hypercorn                                0.17.3
hyperframe                               6.0.1
idna                                     3.3
itsdangerous                             2.2.0
Jinja2                                   3.1.5
jiter                                    0.8.2
joblib                                   1.4.2
Levenshtein                              0.26.1
MarkupSafe                               3.0.2
mock                                     5.1.0
mpmath                                   1.3.0
multidict                                6.1.0
nose                                     1.3.7
numpy                                    1.26.4
onnxruntime                              1.20.1
openai                                   1.59.7
openwakeword                             0.6.0
packaging                                24.2
pathlib2                                 2.3.7.post1
pip                                      23.0.1
priority                                 2.0.0
propcache                                0.2.1
proto-plus                               1.25.0
protobuf                                 5.29.2
pvporcupine                              3.0.3
pyasn1                                   0.6.1
pyasn1_modules                           0.4.1
PyAudio                                  0.2.13
pycryptodomex                            3.11.0
pydantic                                 2.10.4
pydantic_core                            2.27.2
pydub                                    0.25.1
pyftdi                                   0.56.0
pyparsing                                3.2.0
pyserial                                 3.5
pysine                                   0.9.2
python-apt                               2.6.0
python-Levenshtein                       0.26.1
pyusb                                    1.3.1
Quart                                    0.20.0
RapidFuzz                                3.11.0
requests                                 2.28.1
RPi.GPIO                                 0.7.1
rpi-ws281x                               5.0.0
rsa                                      4.9
scikit-learn                             1.6.0
scipy                                    1.14.1
setuptools                               66.1.1
six                                      1.16.0
smbus2                                   0.4.2
sniffio                                  1.3.1
soupsieve                                2.6
SpeechRecognition                        3.12.0
spidev                                   3.5
srt                                      3.5.3
ssh-import-id                            5.10
sympy                                    1.13.3
sysv-ipc                                 1.1.0
tabulate                                 0.9.0
termcolor                                2.5.0
tflite-runtime                           2.14.0
threadpoolctl                            3.5.0
toml                                     0.10.2
tqdm                                     4.67.1
typing_extensions                        4.12.2
uritemplate                              4.1.1
urllib3                                  1.26.12
Werkzeug                                 3.1.3
wheel                                    0.38.4
wsproto                                  1.2.0
yarl                                     1.18.3
yt-dlp                                   2024.12.13


