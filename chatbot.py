# 1. detect wake word,
# 2. prompt for question, 
# 3. pass query to OpenAi and 
# 4. speak response

import waitForWakeWord
from datetime import datetime
#import callOpenai
#import openai
#from gtts import gTTS
#import playsound
import subprocess, os, re
from config import gemini_key
from config import my_city
from speech_to_text import recognize_speech
#from stt_gg_cloud_v1 import stt_process
from text_to_speech import text_to_speech
#from pixels import Pixels
from ws281x import Led
import google.generativeai as genai
from chatgpt_response import chatgpt_response
from yt_dlp_play_m3u8 import play_m3u8
from hass_process import hass_process
from get_weather import get_weather

"""
def speak(text, filename):
  tts = gTTS(text=text, lang="en")
  tts.save(filename)
"""
#led = Led()

# Cấu hình Generative AI
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")
# Hàm sinh phản hồi từ Generative AI
def generate_ai_response(data):
    response = model.generate_content(data)
    return response.text
def extract_song_name(text):
    match = re.search(r"(mở nhạc|mở bài hát)\s+(.*)", text, re.IGNORECASE)
    if match:
        return match.group(2).strip()
    return 'Mộng hoa sim'
def play(filename):
  #playsound.playsound(filename)
  subprocess.call(["ffplay", "-nodisp", "-autoexit", filename])
  os.remove(filename)

def main():
    #openai.api_key =  keys.key['OPEN_AI_KEY']
    filename = "respond.mp3"
    loi=0
    led = Led()
    obj_music = {"bài hát", "nhạc"}
    obj_hass = {"kịch bản", "thực hiện", "thực thi", "quạt","đèn"}
    obj_weather = {"thời tiết","có mưa không"}
    """
    def Gspeak(speech, filename):
        speak(speech, filename)
        play(filename)
        return
    """
    #pixels = Pixels()
   
    #led.set_state('SPEAK')
    #led.colorWipe(Color(0,0,0))
    #pixels.speak()
    led.rainbow_cycle(0.001)
    speech = "Xin chào, mời bạn đánh thức và ra khẩu lệnh cho tôi"
    text_to_speech(speech, filename)
    play(filename)
    led.set_color((0, 0, 0))
    #pixels.off()
    #led.set_state('OFF')
    #led._off()
    #Gspeak(speech, filename)

    

    while True:
        #led.set_state('OFF')
        #led._off()
        success = waitForWakeWord.wait()
        if not success:
            break  # Nếu không kích hoạt, thoát chương trình
        while success:
            #Gspeak("Ask me a question or say quit", filename)
            #pixels.wakeup()
            led.set_color((0, 255, 0))
            #led.set_state('WAKEUP')
            #led.colorWipe(Color(0,0,0))
            #speech = "dạ ma ma đây"
            #text_to_speech(speech, filename)
            #play(filename)
            subprocess.call(["ffplay", "-nodisp", "-autoexit", 'sounds/ding.mp3'])
            led.set_color((0, 0, 0))
            #text_to_speech("Xin chào", filename)
            #play(filename)
            query = recognize_speech()
            #query = stt_process()
            led.set_color((0, 0, 255))
            #led.set_state('THINK')
            #led.colorWipe(Color(0,0,0))
            #pixels.think()
            try:
                if query == 'Chào bạn':
                    success = False
                    led.rainbow_cycle(0.001)
                    #pixels.speak()
                    #led.set_state('SPEAK')
                    #led.colorWipe(Color(0,0,0))
                    text_to_speech("Chào bạn nhé. Cần điều khiển thiết bị hay mở bài hát, bạn cứ gọi và ra lệnh cho tôi nhé.", filename)
                    play(filename)
                elif 'tăng âm lượng' in query:
                    subprocess.run(["amixer", "sset", "Master", "5%+"])
                    answer_text = "đã tăng âm lượng thêm 5%"
                    led.rainbow_cycle(0.001)
                    text_to_speech(answer_text, filename)
                    play(filename)
            
                elif 'giảm âm lượng' in query:
                    subprocess.run(["amixer", "sset", "Master", "5%-"])
                    answer_text = "đã giảm âm lượng thêm 5%"
                    led.rainbow_cycle(0.001)
                    text_to_speech(answer_text, filename)
                    play(filename)
                    
                elif 'Mấy giờ' in query or 'mấy giờ' in query:
                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%H:%M")
                    answer_text = f"Bây giờ là: {formatted_time}"
                    led.rainbow_cycle(0.001)
                    text_to_speech(answer_text, filename)
                    play(filename)    
                elif any(item in query for item in obj_music):
                    song_name = extract_song_name(query)
                    led.rainbow_cycle(0.001)
                    play_m3u8(song_name)
                    success = False
                    #handle_music_and_lights(song_name, pixels)
                    
                elif any(item in query for item in obj_hass):
                    answer_text = hass_process(query)
                    led.rainbow_cycle(0.001)
                    #led.colorWipe(Color(0,0,0))
                    #pixels.speak()
                    text_to_speech(answer_text, filename)
                    play(filename)
                elif any(item in query for item in obj_weather):
                    answer_text = get_weather(my_city)
                    led.rainbow_cycle(0.001)
                    #led.colorWipe(Color(0,0,0))
                    #pixels.speak()
                    text_to_speech(answer_text, filename)
                    play(filename)
                else:
                    #Gspeak("I think you said " + str(query) + ". Asking chat g p t", filename)
                    #response = callOpenai.openai_create(query)
                    result = generate_ai_response(query)
                    #result = chatgpt_response(query)
                    print("GPT:", result)
                    #led.set_state('SPEAK')
                    led.rainbow_cycle(0.001)
                    #led.colorWipe(Color(0,0,0))
                    #pixels.speak()
                    text_to_speech(result, filename)
                    play(filename)

            except Exception as e:
                print(f"Lỗi xử lý: {e}")
                answer_text = 'Không nhận dạng được câu lệnh'
                #led.set_state('SPEAK')
                led.rainbow_cycle(0.001)
                #led.colorWipe(Color(0,0,0))
                #pixels.speak()
                text_to_speech(answer_text, filename)
                play(filename)
                loi=loi+1
                if(loi==2): 
                    loi=0
                    success = False
            #led.set_state('OFF')
            #led._off()
            #pixels.off()
            subprocess.call(["ffplay", "-nodisp", "-autoexit", "sounds/dong.mp3"])
            #pixels.off() 
            led.set_color((0, 0, 0))
            #led.set_state('OFF')
            #led._off()
            print("End trò chuyện")

    
if __name__ == "__main__":
    main()