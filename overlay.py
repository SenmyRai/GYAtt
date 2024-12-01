from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtCore import QTimer
import sys
import random
import os  # For listing files in a directory
import glob  

# Get the directory where the script or executable is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the folder where images are stored, relative to the current directory
folder_path = os.path.join(current_dir, "memes")  # Folder named 'images' in the same directory as the program

# Use glob to find all jpg, png, jpeg files in the folder
images = glob.glob(os.path.join(folder_path, "*.jpg")) + \
         glob.glob(os.path.join(folder_path, "*.jpeg")) + \
         glob.glob(os.path.join(folder_path, "*.png"))

#REMOVE LATER. THIS MAKES IT DISAPPEAR ON TOUCH. ONLY FOR DEBUGGING
"""class KeyPressLabel(QLabel):
    def keyPressEvent(self, event):
        QApplication.quit()"""

def show_overlay():
    app = QApplication(sys.argv)
    
    label = QLabel() #IF REMOVED ABOVE, PUT QLabel() HERE
    random_image = random.choice(images)
    pixmap = QPixmap(random_image)
    label.setPixmap(pixmap)
    label.setAttribute(Qt.WA_TranslucentBackground)
    label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
    label.setWindowOpacity(0.0)  # Start fully transparent
    label.show()
    
    # Create a fade-in animation
    animation = QPropertyAnimation(label, b"windowOpacity")
    animation.setDuration(2000)  # 2 seconds
    animation.setStartValue(0.0)  # Start transparent
    animation.setEndValue(0.8)  # End with 80% opacity
    animation.start()
    
    # Set a timer to quit the application after 7 seconds automatically
    QTimer.singleShot(7000, app.quit) # 7000 milliseconds = 7 seconds
    sys.exit(app.exec_())

if __name__ == "__main__":
    show_overlay()
