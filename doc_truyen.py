from bs4 import BeautifulSoup
import re
import datetime
import json
import requests
#import certifi
import urllib3
import random
# Tắt cảnh báo không an toàn
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from src.text_to_speech import text_to_speech

url1 = "https://dailuu.wordpress.com/2024/12/28/23-mau-chuyen-ngan-va-nhung-bai-hoc-cuoc-doi-rut-ra-tu-do.html"
    
    
def doc_truyen():
    answer_text='Không có câu trả lời cho tình huống này' #Giá trị Default cho câu trả lời
    try:
        # Gửi yêu cầu GET đến trang web
        #print("DOC TRUYEN")
        response = requests.get(url1, verify=False)
        content = ""
        story_datas = []
        print(response.status_code)
        if response.status_code == 200:
            #print(response.content)
            soup=BeautifulSoup(response.content,'html.parser')
            #print(soup)
            for x in range(1, 24):
                item = "truyen" + str(x)
                story_datas.append(item)  
                
            idname= random.choice(story_datas)
            content=soup.find('div', id=idname)
            answer_text=content.text.strip()
            #print(answer_text)
            #player2.play_and_wait(tts_process(answer_text,False))
    except:            
        answer_text = 'Lỗi xử lý thông tin'                                    
    print(answer_text)
    if answer_text:
        text_to_speech(answer_text, "vi")
    else:
        text_to_speech("Không tìm thấy thông tin", "vi")


if __name__ == '__main__':
    doc_truyen()