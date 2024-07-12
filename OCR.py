import cv2
import pytesseract
import os
import time
from pygame import mixer
from gtts import gTTS

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\jadit\Downloads\5.3.4 source code\tesseract-ocr-tesseract-bc059ec\tesseract.exe'

mytext = 'Welcome'
language = 'en'

mixer.init()

def SendDataCommand(cmd):
    # Implement your custom code to send data via serial port
    pass

time.sleep(2)

cap = cv2.VideoCapture(1)
cv2.namedWindow("test")

img_counter = 0
ii = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break
    
    cv2.imshow("test", frame)
    
    k = cv2.waitKey(1)
    if k == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k == 32:
        # SPACE pressed
        print("Frame captured!!")
        img_name = "opencv_frame.jpeg"
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        
        try:
            result = pytesseract.image_to_string(img_name)
            print(result)
            SendDataCommand(result)

            myobj = gTTS(text=result, lang=language, slow=False)
            myobj.save("welcome" + str(ii) + ".mp3")
            mixer.music.load("welcome" + str(ii) + ".mp3")
            mixer.music.play()
            ii += 1
            while mixer.music.get_busy():  # wait for music to finish playing
                time.sleep(1)
        except Exception as e:
            print("Error during OCR processing:", e)

cap.release()
cv2.destroyAllWindows()
