#include <Servo.h> 
const int trigPin = 12;
const int echoPin = 11;
Servo myservo;  // 定義舵機對象
long duration;
float distance;
bool canSerialWrite;
void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  myservo.attach(9);  // 設置舵機控制腳位
  canSerialWrite = true;
}

void loop() {
  if(canSerialWrite){
    // 發送超音波脈衝
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    // 讀取回音時間
    duration = pulseIn(echoPin, HIGH);

    // 計算距離（公分）
    distance = duration * 0.034 / 2;

    // 檢查是否在 10~20 cm 範圍內
    if (distance >= 10 && distance <= 20) {
      Serial.println("SNAP");  // 傳送 SNAP 訊號 to python
      canSerialWrite = false;
      delay(1000); // 延遲1秒
    }
  }
  
  //接收到訊號
  if (Serial.available()) {
    char signal = Serial.read();
    Serial.print("接收到分類訊號：");
    Serial.println(signal);

    if (signal == 'G') {
      Serial.println("分類為：一般垃圾，開啟一般垃圾桶");
      myservo.write(45);
      delay(500);
      myservo.write(90);
    } else if (signal == 'R') {
      Serial.println("分類為：資源回收，開啟資源回收桶");
      myservo.write(135);
      delay(500);
      myservo.write(90);
    } else {
      Serial.println("收到未知訊號，無法處理");
    }
    canSerialWrite = true;
  }

  delay(200);  // 每200毫秒檢查一次
} 
