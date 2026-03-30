void setup() {
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < 6; i++) {
    int raw = analogRead(i);               // A0~A5
    float voltage = raw * (15.0 / 1023.0);  // 換算成電壓
    Serial.print(voltage, 2);              // 保留兩位小數
    if (i < 5) Serial.print(",");          // 用逗號分隔
  }
  Serial.println();  // 每行結尾換行
  delay(1000);       // 每秒送一次
}
