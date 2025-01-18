from bs4 import BeautifulSoup
import random
import requests
import urllib3
import json
from src.text_to_speech import text_to_speech

# Tắt cảnh báo không an toàn HTTPS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Đọc tệp JSON chứa từ khóa
files = ['object.json']
data = {}
for file in files:
    with open('/home/pi/Personal-AI-Assistant/object.json', encoding='utf-8') as json_file:
        data[file] = json.load(json_file)
obj_data = data.get('object.json', {})
obj_ong_ba = [p['value'] for p in obj_data['ong_ba']]
obj_bo_me = [p['value'] for p in obj_data['bo_me']]
obj_gia_dinh = [p['value'] for p in obj_data['gia_dinh']]
obj_vo_chong = [p['value'] for p in obj_data['vo_chong']]
obj_ban_than = [p['value'] for p in obj_data['ban_than']]
obj_nguoi_yeu = [p['value'] for p in obj_data['nguoi_yeu']]
obj_sep = [p['value'] for p in obj_data['sep']]
obj_dong_nghiep = [p['value'] for p in obj_data['dong_nghiep']]
obj_thay_co = [p['value'] for p in obj_data['thay_co']]


url1 = "https://dailuu.wordpress.com/2024/12/28/nhung-cau-chuc-tet-hay-ngan-gon.html"

def chuc_tet(data):
    answer_text = 'Không có câu trả lời cho tình huống này'  # Giá trị mặc định
    try:
        response = requests.get(url1, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            if any(item in data for item in obj_ong_ba):
                p_tags = soup.select(".ong_ba p")
            elif any(item in data for item in obj_bo_me):
                p_tags = soup.select(".bo_me p")
            elif any(item in data for item in obj_gia_dinh):
                p_tags = soup.select(".gia_dinh p")
            elif any(item in data for item in obj_vo_chong):
                p_tags = soup.select(".vo_chong p")
            elif any(item in data for item in obj_ban_than):
                p_tags = soup.select(".ban_than p")
            elif any(item in data for item in obj_nguoi_yeu):
                p_tags = soup.select(".nguoi_yeu p")
            elif any(item in data for item in obj_sep):
                p_tags = soup.select(".sep p")
            elif any(item in data for item in obj_dong_nghiep):
                p_tags = soup.select(".dong_nghiep p")
            elif any(item in data for item in obj_thay_co):
                p_tags = soup.select(".thay_co p")       
            else: 
                answer_text = "Không tìm thấy đoạn văn phù hợp trong nội dung."
            
            p_contents = [p.text.strip() for p in p_tags]
            
            if p_contents:
                random_p_contents = random.sample(p_contents, min(2, len(p_contents)))
                answer_text = "\n".join(random_p_contents)
            else:
                answer_text = "Không tìm thấy đoạn văn phù hợp trong nội dung."
            
        else:
                answer_text = f"Lỗi tải nội dung: Mã lỗi {response.status_code}"
    
    except Exception as e:
        answer_text = f"Lỗi xử lý thông tin: {e}"
    
    print(answer_text)
    
    # Chuyển văn bản thành giọng nói
    text_to_speech(str(answer_text), "vi")  # Đảm bảo text là chuỗi

if __name__ == '__main__':
    chuc_tet('Bố mẹ')
