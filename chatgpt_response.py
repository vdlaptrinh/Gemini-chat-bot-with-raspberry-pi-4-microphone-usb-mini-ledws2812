import time
import subprocess, os
import logging
import random
from openai import OpenAI
from text_to_speech import text_to_speech


# Enter your Assistant ID here.
ASSISTANT_ID = ""

# Make sure your API key is set as an environment variable.
client = OpenAI(api_key="")
# Set up logging
logging.basicConfig(level=logging.INFO)
filename = "respond.mp3"
def play(filename):
  #playsound.playsound(filename)
  subprocess.call(["ffplay", "-nodisp", "-autoexit", filename])
  os.remove(filename)

def chatgpt_response(input_text):
    #print(f"{Lib.GREEN_COLOR} Đây là văn bản text truyền vào: {input_text} {Lib.RESET_COLOR}")
    
    # Tạo một thread với thông điệp của người dùng
    try:
        thread = client.beta.threads.create(
            messages=[{
                "role": "user",
                "content": input_text,
            }]
        )
    except Exception as e:
        logging.error(f"Lỗi khi tạo thread: {e}")
        return "Có lỗi xảy ra khi tạo thread. Vui lòng thử lại sau."

    # Tạo và gửi run cho assistant
    try:
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    except Exception as e:
        logging.error(f"Lỗi khi tạo run: {e}")
        return "Có lỗi xảy ra khi tạo run. Vui lòng thử lại sau."
    
    # Chờ cho đến khi run hoàn thành (với cơ chế backoff)
    max_retries = 30
    retries = 0
    while run.status != "completed" and retries < max_retries:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        except Exception as e:
            logging.error(f"Lỗi khi truy vấn trạng thái run: {e}")
            retries += 1
            backoff_time = random.uniform(1, 3) * (2 ** retries)  # Exponential backoff
            logging.info(f"Đang thử lại sau {backoff_time:.2f} giây...")
            time.sleep(backoff_time)
            continue
        
        retries += 1
        if retries == 10:
            #led.rainbow_cycle(0.001)
            speech = "Bạn chờ ma ma 1 tí nhé"
            text_to_speech(speech, filename)
            play(filename)
        logging.info(f"🏃 Trạng thái run: {run.status}")
        if retries >= max_retries:
            logging.error("Không thể hoàn thành run sau nhiều lần thử.")
            return "Quá trình yêu cầu mất quá nhiều thời gian. Vui lòng thử lại sau."
    
    # Khi run hoàn thành, lấy câu trả lời từ thread
    try:
        message_response = client.beta.threads.messages.list(thread_id=thread.id)
        messages = message_response.data
        latest_message = messages[0]
        answer_text = latest_message.content[0].text.value
    except Exception as e:
        logging.error(f"Lỗi khi lấy phản hồi: {e}")
        return "Có lỗi khi lấy phản hồi. Vui lòng thử lại sau."
    
    return answer_text

