import cv2
import time
import serial
import google.generativeai as genai
import os
import json
from google.cloud import vision

# 設定 Gemini API 
GEMINI_API_KEY = "金鑰" # 根據實際金鑰替換
genai.configure(api_key=GEMINI_API_KEY)
# 設定 Cloud Vision API 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "金鑰.json" # 根據實際金鑰替換
vision_client = vision.ImageAnnotatorClient()


# 設定 Arduino COM 埠
try:
    ser = serial.Serial('COM7', 9600, timeout=1) # 根據實際 COM 埠替換
    time.sleep(2)  # 等待 Arduino 重啟
    print("已連接 Arduino")
except Exception as e:
    print(f"無法連接 Arduino：{e}")
    exit()

snap_processed = False  # 防止重複處理同一個 SNAP 訊號

while True:

    # 接收到訊號
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print(f"接收到：{line}")
        if line == "SNAP" and not snap_processed:
            snap_processed = True

            cap = cv2.VideoCapture('http://[DroidCamIP]/mjpegfeed') # 根據實際DroidCam手機端的IP地址替換
            print("鏡頭是否正常 ？ {}".format(cap.isOpened()))
            time.sleep(0.5)  # 穩定一下畫面
            ret, frame = cap.read() 
            cap.release()
            if ret:
                cv2.imwrite("snapshot.jpg", frame)
                print("已拍照並儲存為 snapshot.jpg")
            else:
                print("拍照失敗")
                snap_processed = False
                continue

            time.sleep(1.0)
            # 載入圖片檔案
            image_path = "./snapshot.jpg"
            with open(image_path, "rb") as image_file:
                content = image_file.read()
            image = vision.Image(content=content)

            # 呼叫 Vision API 的標籤偵測
            response = vision_client.label_detection(image=image)

            # 錯誤處理
            if response.error.message:
                print(f"錯誤：{response.error.message}")
                snap_processed = False
                continue

            # 擷取標籤資訊並轉為 JSON 格式
            labels = response.label_annotations
            label_data = []
            for label in labels:
                label_data.append({
                    "description": label.description,
                    "score": label.score,
                    "topicality": label.topicality
                })
            vision_json = json.dumps(label_data, indent=2)
            print("Cloud Vision 判斷結果：\n", vision_json)

            # 建立提示給 Gemini 分析垃圾類別
            prompt = (
                "The following is the analysis result from the Vision API, showing various labels with scores and topicality.\n"
                "Please tell me whether this is most likely general waste or recyclable waste.\n\n"
                "If label have Tissue Paper answer general"
                "If not recycle answer general"
                f"{vision_json}\n"
                "Please answer with either 'general' or 'recyclable' only."
            )

            # 使用 Gemini 進行分類推論
            model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
            gemini_response = model.generate_content(prompt)

            # 顯示結果
            print("Gemini 判斷結果：", gemini_response.text.strip())

            ###############################################################################

            # 判斷並準備傳送給 Arduino 的訊號
            if "recyclable" in gemini_response.text.strip().lower():
                signal = 'R'
            elif "general" in gemini_response.text.strip().lower():
                signal = 'G'
            else:
                signal = 'U'  # 無法判斷

            # 傳送至 Arduino
            try:
                time.sleep(2)  # 等待 Arduino 重啟
                ser.write(signal.encode())
                print(f"已傳送分類訊號給 Arduino：{signal}")
                time.sleep(1)
            except Exception as e:
                print(f"傳送至 Arduino 發生錯誤：{e}")

            snap_processed = False  # 重設以接收下一次 SNAP