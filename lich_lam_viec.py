from bs4 import BeautifulSoup
import re
import datetime
import json
import requests
#import certifi
import urllib3
# Tắt cảnh báo không an toàn
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from src.text_to_speech import text_to_speech

url = "https://dttt.caothang.edu.vn/lich-cong-tac-tuan.html"
    
# Đọc tệp JSON chứa từ khóa
files = ['object.json']
data = {}
for file in files:
    with open('/home/pi/Personal-AI-Assistant/object.json', encoding='utf-8') as json_file:
        data[file] = json.load(json_file)
obj_data = data.get('object.json', {})
obj_monday = [p['value'] for p in obj_data['monday']] #Khai báo keyword dạng Object, đã định nghĩa trong object.json ở đây
obj_tuesday = [p['value'] for p in obj_data['tuesday']] #Khai báo keyword dạng Object, đã định nghĩa trong object.json ở đây
obj_wednesday = [p['value'] for p in obj_data['wednesday']] #Khai báo keyword dạng Object, đã định nghĩa trong object.json ở đây
obj_thursday  = [p['value'] for p in obj_data['thursday']] #Khai báo keyword dạng Object, đã định nghĩa trong object.json ở đây
obj_friday  = [p['value'] for p in obj_data['friday']] #Khai báo keyword dạng Object, đã định nghĩa trong object.json ở đây
obj_saturday  = [p['value'] for p in obj_data['saturday']] #Khai báo keyword dạng Object, đã định nghĩa trong object.json ở đây
obj_sunday  = [p['value'] for p in obj_data['sunday']] #Khai báo keyword dạng Object, đã định nghĩa trong object.json ở đây
obj_luuy = [p['value'] for p in obj_data['luuy']]


def split_into_chunks(text):
    data = []
    if text:
        words = text.split()
        for i in range(len(words) - 1):
            data.append(" ".join(words[i:i+2]))
            if i + 2 < len(words):
                data.append(" ".join(words[i:i+3]))
    return data
    
def lich_lam_viec(text):
    answer_text='Không có câu trả lời cho tình huống này' #Giá trị Default cho câu trả lời
    try:
        # Gửi yêu cầu GET đến trang web
        response = requests.get(url, verify=False)
        # Kiểm tra xem yêu cầu có thành công không (status code 200 là thành công)
        #print(data)
        if response.status_code == 200:
            # Sử dụng BeautifulSoup để phân tích cú pháp HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            # Tạo một biến để lưu trữ toàn bộ nội dung
            full_content = ""
            # Lấy Tiêu đề
            title = soup.title.text.strip()
            #print(title)
            # Lấy Tiêu đề bài viết
            title1 = soup.find('h3', class_ = 'title')
            #print(title1.get_text())
            # Lấy Nội dung chú ý:
            luuy = soup.find('p', class_ = 'luuy')
            #print(answer_text)
            # Lấy Nội dung từ thẻ <td>
            td_tags = soup.find_all('td')
            #print(td_tags)
            for td_tag in td_tags:
                p_tags = td_tag.find_all('p')
                for p_tag in p_tags:
                    full_content += f"{p_tag.text.strip()}\n"
                    full_content=full_content.replace('TP:', 'Thành phần:')
            #print(full_content) 
            data = split_into_chunks(text)
            if any(item in data for item in obj_monday):
                #print("Xử lý thứ 2")
                thu_hai = re.search(r'THỨ HAI(.*?)THỨ BA', full_content, re.DOTALL)
                answer_text = thu_hai.group(1).strip()
                #print(answer_text)
            elif any(item in data for item in obj_tuesday):
                #print("Xử lý thứ 3")
                thu_ba = re.search(r'THỨ BA(.*?)THỨ TƯ', full_content, re.DOTALL)
                answer_text = thu_ba.group(1).strip()
                #print(answer_text)
            elif any(item in data for item in obj_wednesday):
                #print("Xử lý thứ 4")
                thu_tu = re.search(r'THỨ TƯ(.*?)THỨ NĂM', full_content, re.DOTALL)
                answer_text = thu_tu.group(1).strip()
                #print(answer_text)
            elif any(item in data for item in obj_thursday):
                #print("Xử lý thứ 5")
                thu_nam = re.search(r'THỨ NĂM(.*?)THỨ SÁU', full_content, re.DOTALL)
                answer_text = thu_nam.group(1).strip() 
                #print(answer_text)       
            elif any(item in data for item in obj_friday):
                #print("Xử lý thứ 6")
                thu_sau = re.search(r'THỨ SÁU(.*?)THỨ BẢY', full_content, re.DOTALL)
                answer_text = thu_sau.group(1).strip()
                #print(answer_text)        
            elif any(item in data for item in obj_saturday):
                #print("Xử lý thứ 7")
                thu_bay = re.search(r'THỨ BẢY(.*?)CHỦ NHẬT', full_content, re.DOTALL)
                answer_text = thu_bay.group(1).strip()
                #print(answer_text)        
            elif any(item in data for item in obj_sunday):
                #print("Xử lý thứ CN")
                chu_nhat = re.search(r'CHỦ NHẬT(.*?)$', full_content, re.DOTALL)
                answer_text = chu_nhat.group(1).strip()   
                #print(answer_text)
            elif any(item in data for item in obj_luuy):
                #print("Xử lý luu y")
                answer_text = title1.get_text()+'\n' + luuy.get_text()
                #print(answer_text)
            else:
                # Lấy ngày hôm nay
                #print("Lấy ngày hôm nay")
                ngay_hom_nay = datetime.datetime.now()
                # Lấy số thứ tự của ngày trong tuần (0 là thứ hai, 6 là chủ nhật)
                so_thu_tu_ngay = ngay_hom_nay.weekday()
                #print(so_thu_tu_ngay)
                # Chuyển đổi số thứ tự sang tên của ngày trong tuần
                ten_ngay = ['THỨ HAI', 'THỨ BA', 'THỨ TƯ', 'THỨ NĂM', 'THỨ SÁU', 'THỨ BẢY', 'CHỦ NHẬT']
                ten_thu = ten_ngay[so_thu_tu_ngay]
                if ten_thu =='THỨ HAI':
                    thu_hai = re.search(r'THỨ HAI(.*?)THỨ BA', full_content, re.DOTALL)
                    answer_text = thu_hai.group(1).strip()
                elif ten_thu =='THỨ BA':
                    thu_ba = re.search(r'THỨ BA(.*?)THỨ TƯ', full_content, re.DOTALL)
                    answer_text = thu_ba.group(1).strip()
                elif ten_thu =='THỨ TƯ':
                    thu_tu = re.search(r'THỨ TƯ(.*?)THỨ NĂM', full_content, re.DOTALL)
                    answer_text = thu_tu.group(1).strip()
                elif ten_thu =='THỨ NĂM':
                    thu_nam = re.search(r'THỨ NĂM(.*?)THỨ SÁU', full_content, re.DOTALL)
                    answer_text = thu_nam.group(1).strip()
                    #print(answer_text)
                elif ten_thu =='THỨ SÁU':
                    thu_sau = re.search(r'THỨ SÁU(.*?)THỨ BẢY', full_content, re.DOTALL)
                    answer_text = thu_sau.group(1).strip()        
                elif ten_thu =='THỨ BẢY':
                    thu_bay = re.search(r'THỨ BẢY(.*?)CHỦ NHẬT', full_content, re.DOTALL)
                    answer_text = thu_bay.group(1).strip()
                    #print(answer_text)
                elif ten_thu=='CHỦ NHẬT':
                    chu_nhat = re.search(r'CHỦ NHẬT(.*?)$', full_content, re.DOTALL)
                    answer_text = chu_nhat.group(1).strip()                                            
    except:            
        answer_text = 'Lỗi xử lý thông tin'
    #print(answer_text)
    if answer_text:
        text_to_speech(answer_text, "vi")
    else:
        text_to_speech("Không tìm thấy thông tin", "vi")
#player2.play_and_wait(tts_process(answer_text,False)) #False - Phát câu trả lời TTS ko cache lại nội dung, True - Có cache lại để cho lần sau

if __name__ == '__main__':
    lich_lam_viec("lịch làm việc thứ 3")