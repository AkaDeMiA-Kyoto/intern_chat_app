#define MotorL_Pin 3
#define MotorR_Pin 11

#define SensorL_Pin A0
#define SensorR_Pin A1

#define ThresholdL 500
#define ThresholdR 500

int move_mode=0;

//PIDパラメータ
float Kp = 0.6;
float Ki = 0.0;
float Kd = 0.4;

//PID制御用の変数
float integral = 0;
float lastError = 0;


void setup() {
  // put your setup code here, to run once:

  pinMode(MotorL_Pin, OUTPUT);
  pinMode(MotorR_Pin, OUTPUT);

  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:

  int v_sensorL, v_sensorR;
  int v_motorL, v_motorR;
  boolean is_sensorL_on_track;
  boolean is_sensorR_on_track;

  v_sensorL=analogRead(SensorL_Pin);
  v_sensorR=analogRead(SensorR_Pin);

  //エラーの計算（センサの差をエラーとして使用）
  float error = v_sensorL-v_sensorR;

  //PID制御の計算
  integral += error;
  float derivative = error - lastError;
  float pid = Kp * error + Ki * integral + Kd * derivative;
  lastError = error;

  //Serial.println(v_sensorL);
  //delay(10);

  is_sensorL_on_track=(v_sensorL>ThresholdL);
  is_sensorR_on_track=(v_sensorR>ThresholdR);


  if(is_sensorL_on_track && is_sensorR_on_track){
    //両センサとも白
    move_mode=0;
  }
  
  else if(!is_sensorL_on_track && is_sensorR_on_track){
    //左センサは黒、右センサは白
      move_mode=1;

  }
  else if(is_sensorL_on_track && !is_sensorR_on_track){
    //左センサは白、右センサは黒
      move_mode=2;
  }
  else{
      move_mode=3;
    }

  Serial.println(move_mode);
  switch(move_mode){
    case 0:
      v_motorL=100;
      v_motorR=100;
      break;
    case1:
      v_motorL = constrain(100-pid/10, 0, 255);
      v_motorR = constrain(100+pid/10, 0, 255);
      break;
    case 2:
      v_motorL = constrain(100-pid/10, 0, 255);
      v_motorR = constrain(100+pid, 0, 255);
      break;
    case 3:
      v_motorL=0;
      v_motorR=0;
      break;
  }

  analogWrite(MotorL_Pin, v_motorL);
  analogWrite(MotorR_Pin, v_motorR);

  delay(10);

  
}
