import yt_dlp
import subprocess, os
from text_to_speech import text_to_speech
filename = "respond.mp3"

def play(filename):
  #playsound.playsound(filename)
  subprocess.call(["ffplay", "-nodisp", "-autoexit", filename])
  os.remove(filename)

def play_m3u8(song_name):
    # Tìm kiếm bài hát trên YouTube
    search_query = f"ytsearch:{song_name}"
    # Cấu hình yt-dlp để lấy âm thanh tốt nhất
    ydl_opts = {
        'format': 'bestaudio/best',  # Chọn định dạng âm thanh tốt nhất
        'noplaylist': True,  # Không tải playlist
        'quiet': True,  # Không in ra quá nhiều thông tin
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Tìm kiếm video và trích xuất thông tin
        try:
            info = ydl.extract_info(search_query, download=False)
            
            # Kiểm tra nếu có video trong 'entries'
            if 'entries' in info and len(info['entries']) > 0:
                video_info = info['entries'][0]
                
                # Lọc các định dạng âm thanh (không phải video)
                audio_formats = [f for f in video_info['formats'] if 'audio' in f['format']]
                
                # Kiểm tra nếu có định dạng âm thanh
                if audio_formats:
                    # Chọn URL của định dạng âm thanh tốt nhất
                    audio_url = audio_formats[0]['url']
                    #print(f"Tìm thấy video: {video_info['title']} - Tải xuống từ URL: {audio_url}")
                    #print(f"Tìm thấy video: {video_info['title']}")
                    text_to_speech(video_info['title'],filename)
                    play(filename)
                else:
                    text_to_speech("Không tìm thấy định dạng âm thanh",filename)
                    #print("Không tìm thấy định dạng âm thanh cho video này.")
                    play(filename)
                    return
            else:
                text_to_speech("Không tìm thấy bài này trong kết quả tìm kiếm.",filename)
                play(filename)
                #print("Không tìm thấy bài này trong kết quả tìm kiếm.")
                return
        except Exception as e:
            print(f"Lỗi khi trích xuất thông tin: {e}")
            text_to_speech(f"Lỗi khi trích xuất thông tin: {e}",filename)
            play(filename)
            return
    print("Đang phát bài hát...")
    subprocess.call(["ffplay", "-nodisp", "-autoexit", audio_url])
    return
if __name__ == "__main__":
    song_name = input("Nhập tên bài hát: ")
    play_m3u8(song_name)
