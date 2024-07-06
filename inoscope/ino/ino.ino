const int pwmPin = 9;  // Pino PWM
const int numSamples = 100;  // Número de amostras por ciclo
const int amplitude = 250;  // Amplitude da senoide (750 - 512)
const int center = 512;  // Valor central (zero)
const float pi = 3.14159;
const int frequency = 600000;  // Frequência desejada em Hz

void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValueA0 = random(0,1023);
  int sensorValueA1 = 512;
for (int i = 0; i < numSamples; i++) {
    // Calcula o valor da senoide
    float angle = (2 * pi / numSamples) * i;
    int sineValue = int(amplitude * sin(angle) + center);
  Serial.print(sineValue);
  Serial.print(",");
  Serial.println(sensorValueA1);
}
  delay(1);
}
