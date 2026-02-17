#include <FastLED.h>

#define LED_PIN 5
#define NUM_LEDS 50
#define LED_TYPE WS2811
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];
uint8_t buffer[NUM_LEDS * 3];  // store full frame
int index = 0;

void setup() {
    Serial.begin(115200);
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
    FastLED.clear();
    FastLED.show();
}

void loop() {
    while (Serial.available() > 0) {
        buffer[index++] = Serial.read();
        if (index >= NUM_LEDS * 3) {
            // full frame received, update LEDs
            for (int i = 0; i < NUM_LEDS; i++) {
                leds[i] = CRGB(buffer[i*3+1], buffer[i*3], buffer[i*3+2]);
            }
            FastLED.show();
            index = 0;  // reset for next frame
        }
    }
}
