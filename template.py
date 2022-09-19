""" Template for Project 1: Morse code """
import time
from GPIOSimulator_v1 import *

# Creating an object of the GPIOSimulator class
GPIO = GPIOSimulator()

MORSE_CODE = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
              '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n',
              '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u',
              '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z', '.----': '1',
              '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
              '---..': '8', '----.': '9', '-----': '0'}
# Global variables 
T = 1
dot = T
dash = 2*T
medium_pause = 4*T
long_pause = 7*T

class MorseDecoder():
    """ Morse code class """

    def __init__(self):
        """ initialize your class """
        self.current_symbol = ""
        self.current_word = ""
        self.current_message = ""

    def decoding_loop(self):
        """ the main decoding loop """
        # Default states
        prev_state = 0
        start_pause_time = 0
        
        done = False
        while done != True:
            # Getting a new state from the button
            current_state = GPIO.input(PIN_BTN)
            
            # If the state has changed
            if current_state != prev_state:
                
                # Case 1 - Button down
                if prev_state == 0:
                    start_hold_time = time.time()
                    #print("Hold time started")
                    
                    if start_pause_time != 0: # Valid for all iteration except the first because pause_time has not started yet
                        end_pause_time = time.time()
                        pause_time = end_pause_time - start_pause_time
                        print("Pause time is: " + str(pause_time))

                        # Medium pause - if pause is between 3s and 6s
                        if pause_time > medium_pause*0.75 and pause_time < medium_pause*1.5:
                            self.process_signal('medium pause')

                        # Long pause - if pause is between 6s and 10.5s
                        elif pause_time > medium_pause*1.5 and pause_time <long_pause*1.5:
                            self.process_signal('long pause')
                        
                        # Finished with message - if pause is longer than 14s - need to press down button to end
                        elif pause_time > 1.5*long_pause:
                            #self.process_signal('long pause')
                            self.show_message()
                            done = True
                
                # Case 2 - Button up
                else:
                    start_pause_time = time.time()
                    end_hold_time = time.time()
                    hold_duration = end_hold_time - start_hold_time
                    print("The hold duration time is:" + str(hold_duration))
                    
                    # Dot - Time is between 0.25s and 1.25s
                    if hold_duration >=0.25*dot and hold_duration < 1.25*dot:
                        print('.')
                        # Making the blue LED blink
                        GPIO.output(PIN_BLUE_LED, GPIO.HIGH)
                        GPIO.output(PIN_BLUE_LED, GPIO.LOW)
                        self.process_signal('.')
        
                    # Dash - Time > 2
                    elif hold_duration > dash:
                        print('-')
                        # Making alle the red LEDs blink
                        GPIO.output(PIN_RED_LED_0, GPIO.HIGH)
                        GPIO.output(PIN_RED_LED_1, GPIO.HIGH)
                        GPIO.output(PIN_RED_LED_2, GPIO.HIGH)
                        GPIO.output(PIN_RED_LED_0, GPIO.LOW)
                        GPIO.output(PIN_RED_LED_1, GPIO.LOW)
                        GPIO.output(PIN_RED_LED_2, GPIO.LOW)
                        self.process_signal('-')
            
            # Making sure the previous state gets saved
            prev_state = current_state
            
            # Making the while loop not run too many times
            time.sleep(0.1)      
        
    def process_signal(self, signal):
        """ handle the signals using corresponding functions """
        if signal == '.' or signal == '-':
            self.update_current_symbol(signal)
        
        # Medium pause -> Find letter
        elif signal == 'medium pause':
            self.handle_symbol_end()
        
        # Long pause -> End word
        elif signal == 'long pause':
            self.handle_word_end()

    def update_current_symbol(self, signal):
        """ append the signal to current symbol code """
        self.current_symbol = self.current_symbol + signal
        print("The current symbol is: " + self.current_symbol)

    def handle_symbol_end(self):
        """ process when a symbol ending appears """
        symbol= self.current_symbol
        if symbol != "":
            letter = MORSE_CODE[symbol]
            print("Finished with symbol and the symbol is : "+ letter)
            self.current_word = self.current_word + letter
            print("You have the following letters: " + self.current_word)
            self.current_symbol = ""
        else:
            print("Empty string registered")
    
    def handle_word_end(self):
        self.handle_symbol_end()
        print("Finished with word and the current word is: "+ self.current_word)
        self.current_message = self.current_message + self.current_word + " "
        self.current_word = ""

    def show_message(self):
        """ print the decoded message """
        print("The message is: " + self.current_message)

def main():
    """ the main function """
    try:
        # Setting ut the pins and their default states
        GPIO.setup(PIN_BTN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(PIN_RED_LED_0, GPIO.OUT, GPIO.LOW)
        GPIO.setup(PIN_RED_LED_1, GPIO.OUT, GPIO.LOW)
        GPIO.setup(PIN_RED_LED_2, GPIO.OUT, GPIO.LOW)
        GPIO.setup(PIN_BLUE_LED, GPIO.OUT, GPIO.LOW)
        
        # Creating an object
        morse_decoder = MorseDecoder()
        morse_decoder.decoding_loop()
    
    except KeyboardInterrupt:
        print("Keyboard interrupt; quit the program.")
    
    finally:
        GPIO.cleanup()


main()
