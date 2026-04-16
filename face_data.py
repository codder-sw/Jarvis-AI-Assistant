import cv2
import os

# Camera open karein
cam = cv2.VideoCapture(0)
cam.set(3, 640) # window width
cam.set(4, 480) # window height

# Face detection algorithm (Haar Cascade)
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Folder for images
if not os.path.exists('samples'):
    os.makedirs('samples')

print("\n [INFO] Camera starting. Look at the camera and wait...")
count = 0

while(True):
    ret, img = cam.read()
    if not ret:
        break
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Photo save karein (Gray format mein kyunki training easy hoti hai)
        cv2.imwrite(f"samples/User.1.{count}.jpg", gray[y:y+h,x:x+w])
        cv2.imshow('JARVIS Face Scanning...', img)

    k = cv2.waitKey(100) & 0xff
    if k == 27: # 'ESC' to stop
        break
    elif count >= 100: # 100 photos kafi hain
         break

print(f"\n [INFO] Successfully captured {count} samples. Closing camera.")
cam.release()
cv2.destroyAllWindows()