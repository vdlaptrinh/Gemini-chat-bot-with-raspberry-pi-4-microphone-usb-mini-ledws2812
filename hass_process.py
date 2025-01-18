import requests
from text_to_speech import text_to_speech

# Định nghĩa IP của Home Assistant và Long Token
from config import HASS_IP
from config import LONG_TOKEN



def print_all_entities():
    url = f"{HASS_IP}/api/states"
    headers = {
        "Authorization": f"Bearer {LONG_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        entities = response.json()
        for entity in entities:
            print(f"Entity ID: {entity['entity_id']}, Area: {entity.get('attributes', {}).get('area_id', 'Không có')}, Friendly Name: {entity.get('attributes', {}).get('friendly_name', 'Không có')}")
    else:
        print(f"Lỗi khi lấy danh sách thiết bị: {response.status_code}")
        
# Hàm tìm kiếm ID của thiết bị dựa vào tên
def get_entity_id(ten_thiet_bi):
    url = f"{HASS_IP}/api/states"
    headers = {
        "Authorization": f"Bearer {LONG_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        for entity in response.json():
            #if ten_thiet_bi.lower() in entity["attributes"].get("friendly_name", "").lower():
            #   return entity["entity_id"]
            if (entity["entity_id"].startswith("switch.") or entity["entity_id"].startswith("light.")) and \
                ten_thiet_bi.lower() in entity["attributes"].get("friendly_name", "").lower():
                return entity["entity_id"]
    else:
        print(f"Lỗi khi lấy danh sách thiết bị: {response.status_code}")
    return None

def hass_process(data):
    answer_text = "Lỗi HASS"
    if "thực thi" in data or "thực hiện" in data or "kích hoạt" in data:
        # Tách tên kịch bản
        #words = data.split()
        #scene_name = " ".join(word for word in words if word not in ["thực thi", "thực hiện", "kịch bản"])
        scene_name = data.replace("thực thi", "").replace("thực hiện", "").replace("kịch bản", "").replace("kích hoạt", "").strip()
        if scene_name:
            #print(f"đã kích hoạt kịch bản: {scene_name}")
            answer_text = active(scene_name)
        else:
            print("Không xác định được kịch bản để thực thi.")
            answer_text = "Không xác định được kịch bản để thực thi."
    elif "bật" in data or "tắt" in data or "Tắt" in data:
        # Tách tên thiết bị và hành động
        words = data.split()
        action = "turn_on" if "bật" in data else "turn_off"
        ten_thiet_bi = " ".join(word for word in words if word not in ["bật", "tắt", "Tắt"])
        if ten_thiet_bi:
            #print(f"Thực hiện hành động {action} trên thiết bị: {ten_thiet_bi}")
            answer_text = hass_process_device(ten_thiet_bi, action)
        else:
            print("Không xác định được thiết bị để bật/tắt.")
            answer_text = "Không xác định được thiết bị để bật/tắt."
    else:
        print("Dữ liệu không hợp lệ. Vui lòng nhập lệnh phù hợp.")
        answer_text = "Dữ liệu không hợp lệ. Vui lòng nhập lệnh phù hợp."
    # Chuyển văn bản thành giọng nói
    #text_to_speech(answer_text, "vi")  # Đảm bảo text là chuỗi
    return answer_text
# Cập nhật hàm hass_process_device để không bị trùng tên
def hass_process_device(ten_thiet_bi, action="toggle"):
    entity_id = get_entity_id(ten_thiet_bi)
    if not entity_id:
        print(f"Không tìm thấy thiết bị có tên: {ten_thiet_bi}")
        answer_text = f"Không tìm thấy thiết bị có tên: {ten_thiet_bi}"
        return answer_text

    # Định nghĩa URL và payload
    url = f"{HASS_IP}/api/services/homeassistant/{action}"
    headers = {
        "Authorization": f"Bearer {LONG_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"entity_id": entity_id}

    # Gửi yêu cầu bật/tắt
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code in (200, 202):
        #print(f"đã '{action}' {ten_thiet_bi}")
        # Tạo answer_text dựa trên hành động
        if action == "turn_on":
            answer_text = f"Đã bật {ten_thiet_bi}"
        else:
            answer_text = f"Đã tắt {ten_thiet_bi}"
        return answer_text
    else:
        print(f"Lỗi khi thực hiện '{action}': {response.status_code}, {response.text}")
        answer_text = f"Lỗi khi thực hiện '{action}': {response.status_code}, {response.text}"
        return answer_text
# Hàm lấy danh sách tất cả kịch bản (scenes)
def get_all_scenes():
    url = f"{HASS_IP}/api/states"
    headers = {
        "Authorization": f"Bearer {LONG_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        scenes = []
        for entity in response.json():
            if entity["entity_id"].startswith("scene."):
                scenes.append({
                    "entity_id": entity["entity_id"],
                    "friendly_name": entity.get("attributes", {}).get("friendly_name", "Không có tên")
                })
        return scenes
    else:
        print(f"Lỗi khi gọi API: {response.status_code}")
        return []
# Hàm kích hoạt kịch bản
def active(scene_name):
    # Lấy danh sách các kịch bản
    scenes = get_all_scenes()
    #print(scenes)
    #print(scene_name)
    # Tìm scene dựa trên tên
    for scene in scenes:
        if scene_name.lower() in scene["friendly_name"].lower():
            scene_id = scene["entity_id"]
            url = f"{HASS_IP}/api/services/scene/turn_on"
            headers = {
                "Authorization": f"Bearer {LONG_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {"entity_id": scene_id}

            # Gửi yêu cầu kích hoạt
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code in (200, 202):
                #print(f"đã kích hoạt thành công kịch bản: {scene_name}")
                answer_text = f"đã kích hoạt thành công kịch bản: {scene_name}"
                return answer_text
            else:
                print(f"Lỗi khi kích hoạt kịch bản: {response.status_code}, {response.text}")
                answer_text = f"Lỗi khi kích hoạt kịch bản: {response.status_code}, {response.text}"
                return answer_text
    print(f"Không tìm thấy kịch bản nào có tên: {scene_name}")
    answer_text = f"Không tìm thấy kịch bản nào có tên: {scene_name}"
if __name__ == "__main__":
    while True:
        data = input("Nhập lệnh (bật/tắt hoặc thực thi/thực hiện): ")
        if data.lower() in ["thoát", "exit"]:
            print("Thoát chương trình.")
            break
        hass_process(data)