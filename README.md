# 智慧垃圾桶 Smart Trash Can

本專題為一個智慧型垃圾分類系統，透過影像辨識與雲端 AI 模型，自動判斷垃圾類型並控制正確桶蓋開啟，實現資源回收自動化，降低人力成本與錯誤率。

## 系統架構簡介

本系統由感測端、通訊端、控制端與雲端平台組成：

- **感測端**：Arduino Uno + 超音波感測器，用於偵測是否投擲垃圾。
- **通訊端**：Arduino 透過 USB 與電腦通訊，傳遞啟動與分類訊號。
- **控制端**：Arduino 控制舵機馬達，依據分類結果傾斜桶蓋。
- **攝影端**：DroidCam 將手機影像即時傳送至電腦。
- **電腦端**：使用 Google Cloud Vision API + Gemini API 進行影像辨識與垃圾分類推論。

## 環境需求

- Windows 10 作業系統
- [Arduino IDE](https://www.arduino.cc/en/software)（需安裝 `Servo` 函式庫）
- Python 3.10 以上
- 手機安裝 [DroidCam](https://www.dev47apps.com/)
- 已啟用之 Google Cloud Vision API 與 Gemini API 金鑰

### Python 套件需求

請使用以下指令安裝所需套件：

```bash
pip install opencv-python
pip install google-generativeai
pip install google-cloud-vision
pip install pyserial
```

## 測試成果

- 成功辨識衛生紙與寶特瓶，並對應正確垃圾桶。
- 系統可連續進行分類，準確率穩定。
- 測試結果顯示系統分類反應快速，無明顯延遲。

## 未來展望

- 導入本地 AI 模型進行即時分類，減少雲端依賴。
- 開發獨立應用程式整合影像拍攝與辨識。
- 擴增分類種類（如金屬、紙類、玻璃），提升應用場域。
- 增加垃圾量偵測與滿桶通知功能，增強智慧管理能力。