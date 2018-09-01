#include <Servo.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);

#define XPOS 0
#define YPOS 1
#define DELTAY 2

#define LOGO16_GLCD_HEIGHT 16 
#define LOGO16_GLCD_WIDTH  16 
static const unsigned char PROGMEM logo16_glcd_bmp[] =
{ B00000000, B11000000,
  B00000001, B11000000,
  B00000001, B11000000,
  B00000011, B11100000,
  B11110011, B11100000,
  B11111110, B11111000,
  B01111110, B11111111,
  B00110011, B10011111,
  B00011111, B11111100,
  B00001101, B01110000,
  B00011011, B10100000,
  B00111111, B11100000,
  B00111111, B11110000,
  B01111100, B11110000,
  B01110000, B01110000,
  B00000000, B00110000 };

#if (SSD1306_LCDHEIGHT != 64)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif

Servo servo_left;
Servo servo_center;
Servo servo_right;

int left_zero = 65;
int center_zero = 90;
int right_zero = 55;

short MAX_ROTATION = 30;
float SCREEN_FRACTION = -1;
int SERIAL_INPUT = -1;
int NUM_BYTES = -1;
int SCREEN_COUNTER = 0;
int one = -1;
int two = -1;

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  
  Serial.begin(9600);

   move_servo(servo_left, left_zero);
  move_servo(servo_center, center_zero);
  move_servo(servo_right, right_zero);
  
  servo_left.attach(10);
  servo_center.attach(11);
  servo_right.attach(12);
  
  display.display();
  
  delay(2000);

  display.clearDisplay();

  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(10,10);
}

void loop() {

  // input is an integer 0 -> 100, which corresponds to the percentage across the screen (from the left) that the largest pedestrian is
  // input is -1 if there is no pedestrian seen.

  if (Serial.available()) {

    read_serial_data();
    
    SCREEN_FRACTION = float(SERIAL_INPUT) / 100;
    display_pos();
    adjust_servos();
  }
}

void read_serial_data() {
  // we will ALWAYS read in a 3 digit number, n, 0 <= n <= 100.  e.g. 001, 014, 100
  SERIAL_INPUT = 0;
  NUM_BYTES = 0;
  int multi = 100;
  
  while(Serial.available() > 0) {
    delay(5);
    int this_input = Serial.read() - '0';
    SERIAL_INPUT += this_input * multi;
    multi /= 10;
    NUM_BYTES++;
  }
}

void adjust_servos() {
  adjust_servo_left();
  adjust_servo_center();
  adjust_servo_right();
}

void adjust_servo_left() {
  if (SCREEN_FRACTION < .5) {
    move_servo(servo_left, left_zero + (int)(round(MAX_ROTATION * (1 - 2 * SCREEN_FRACTION))));
  } else 
    move_servo(servo_left, left_zero);
}

void adjust_servo_center() {
  if (SCREEN_FRACTION <= .5) {
    move_servo(servo_center, center_zero - (int)(round(MAX_ROTATION * 2 * SCREEN_FRACTION)));
  } else {
    move_servo(servo_center, center_zero - (int)(round(MAX_ROTATION * (1 - 2 * (SCREEN_FRACTION - .5)))));
  }
}

void adjust_servo_right() {
  if (SCREEN_FRACTION > .5) {
    move_servo(servo_right, right_zero - (int)(round(MAX_ROTATION * 2 * (SCREEN_FRACTION - .5))));
  } else
    move_servo(servo_right, right_zero);
}

void move_servo(Servo s1, int pos) {
  s1.write(pos);
}

void display_pos() {
  display.clearDisplay();
  display.setCursor(0,0);
  display.drawPixel(int(128 * SCREEN_FRACTION), 32, WHITE);
  display.print(SERIAL_INPUT);
  display.display();
}

