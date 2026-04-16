import sys
import os
import cv2 # Computer Vision for Authentication
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import QThread, Qt, QTimer, QTime, QDate

# --- 1. Background Logic Thread ---
class Jarv_Logic(QThread):
    def run(self):
        # Background mein voice engine (main.py) start karna
        # Make sure main.py is in the same folder
        os.system("python main.py")

# --- 2. GUI Window Class ---
class JarvisUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window Setup
        self.setWindowTitle("JARVIS v2.0 - Biometric Access")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: black;")

        # --- HUD: Clock & Date ---
        self.time_label = QLabel(self)
        self.time_label.setGeometry(30, 30, 250, 50)
        self.time_label.setStyleSheet("color: #00e5ff; font-family: Courier; font-size: 35px; font-weight: bold;")
        
        self.date_label = QLabel(self)
        self.date_label.setGeometry(35, 80, 300, 30)
        self.date_label.setStyleSheet("color: white; font-family: Courier; font-size: 16px;")

        timer = QTimer(self)
        timer.timeout.connect(self.updateHUD)
        timer.start(1000)

        # Arc Reactor GIF
        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(200, 50, 400, 400)
        self.movie = QMovie("jarvis.gif") 
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        # Status Label (Lock Status)
        self.status_label = QLabel("SYSTEM: LOCKED (BIOMETRIC REQUIRED)", self)
        self.status_label.setGeometry(0, 450, 800, 50)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #ff4444; font-family: Courier; font-size: 20px; font-weight: bold;")

        # Command Log Label
        self.log_label = QLabel("Waiting for Shivam Sir to verify identity...", self)
        self.log_label.setGeometry(0, 490, 800, 30)
        self.log_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.log_label.setStyleSheet("color: #aaaaaa; font-family: Courier; font-size: 14px; font-style: italic;")

        # Verification Button
        self.start_btn = QPushButton("VERIFY IDENTITY", self)
        self.start_btn.setGeometry(300, 530, 200, 40)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #00e5ff;
                border: 2px solid #00e5ff;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00e5ff;
                color: black;
            }
        """)
        self.start_btn.clicked.connect(self.authenticate_user)

        # Thread instance
        self.logic_thread = Jarv_Logic()

    def updateHUD(self):
        self.time_label.setText(QTime.currentTime().toString("hh:mm:ss"))
        self.date_label.setText(QDate.currentDate().toString("ddd, dd MMM yyyy"))

    # --- Face Recognition Authentication ---
    def authenticate_user(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Check if trainer file exists
        if not os.path.exists('trainer/trainer.yml'):
            QMessageBox.critical(self, "Error", "Sir, training data missing hai. Please run face_train.py first!")
            return

        recognizer.read('trainer/trainer.yml')
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        cam = cv2.VideoCapture(0)
        
        self.log_label.setText("Scanning... Face match dhoond raha hoon.")
        verified = False

        # Scan for 30 frames for a precise match
        for _ in range(40): 
            ret, img = cam.read()
            if not ret: break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)

            for (x,y,w,h) in faces:
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                
                # Confidence score < 60 means Shivam Sir is found!
                if (confidence < 60): 
                    verified = True
                    break
            if verified: break

        cam.release()
        cv2.destroyAllWindows()

        if verified:
            self.start_jarvis()
        else:
            self.status_label.setText("ACCESS DENIED!")
            self.status_label.setStyleSheet("color: #ff0000; font-family: Courier; font-size: 20px; font-weight: bold;")
            self.log_label.setText("Identity mismatch. System locked for safety.")
            QMessageBox.warning(self, "Security Alert", "Identity Verification Failed, Shivam Sir!")

    def start_jarvis(self):
        # 1. Startup Sound Play
        try:
            if os.path.exists("startup_sound.mp3"):
                # Using 'start' command for Windows
                os.system("start startup_sound.mp3") 
        except:
            pass

        # 2. Update UI status to Access Granted
        self.status_label.setText("ACCESS GRANTED: WELCOME SHIVAM SIR")
        self.status_label.setStyleSheet("color: #00e5ff; font-family: Courier; font-size: 20px; font-weight: bold;")
        self.log_label.setText("All systems functional. I am online, Sir.")
        
        # 3. Final Button State
        self.start_btn.setEnabled(False)
        self.start_btn.setText("AUTHENTICATED")
        self.start_btn.setStyleSheet("color: #00e5ff; border: 2px solid #00e5ff; border-radius: 10px;")
        
        # 4. Start Background Voice Logic (main.py)
        self.logic_thread.start()

# --- 3. App Launch ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = JarvisUI()
    ui.show()
    sys.exit(app.exec())