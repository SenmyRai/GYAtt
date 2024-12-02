from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, QTimer
import sys
import random
import os
import glob

running_overlay = False
# Get the directory where the script or executable is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the folder where images are stored, relative to the current directory
folder_path = os.path.join(current_dir, "memes")

# Use glob to find all jpg, png, jpeg, gif, webp files in the folder
images = glob.glob(os.path.join(folder_path, "*.jpg")) + \
         glob.glob(os.path.join(folder_path, "*.jpeg")) + \
         glob.glob(os.path.join(folder_path, "*.jfif")) + \
         glob.glob(os.path.join(folder_path, "*.GIF")) + \
         glob.glob(os.path.join(folder_path, "*.webp")) + \
         glob.glob(os.path.join(folder_path, "*.png"))

def clear_overlay():
    global running_overlay
    running_overlay = False
    print("Overlay cleared and image generation stopped.")
    # Quit the QApplication to stop the event loop
    QApplication.quit()

def show_overlay_in_main_thread():
    """Start the overlay in the main thread."""
    global running_overlay
    if running_overlay:  # If overlay is already running, don't start it again
        return

    running_overlay = True
    app = QApplication([])  # Ensure QApplication is created in the main thread
    show_overlay(app)

def show_overlay(app):
    global running_overlay
    
    if not running_overlay:
        return  
    
    labels = []  # List to hold labels for each image
    
 
    screen_width = app.primaryScreen().size().width()  
    screen_height = app.primaryScreen().size().height() 

    image_width = 200
    image_height = 200

    max_x = screen_width // image_width
    max_y = screen_height // image_height
    

    def show_image(index):
        if index >= max_x * max_y:
            return  
        
        label = QLabel()  # Create a label for each image
        random_image = random.choice(images)
        

        print(f"Showing image: {os.path.basename(random_image)}")
        
  
        if random_image.lower().endswith(('.gif', '.webp')):
            movie = QMovie(random_image)
            label.setMovie(movie)
            movie.start()  # Start the animation
        else:
            pixmap = QPixmap(random_image)
            label.setPixmap(pixmap)  # Set as static image
        
        # Set label properties
        label.setAttribute(Qt.WA_TranslucentBackground)
        label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        label.setWindowOpacity(0.8)  # Keep the opacity at 80%
        label.show()
        
        # Randomize the position within screen bounds
        max_x_pos = screen_width - image_width  
        max_y_pos = screen_height - image_height 
        
        random_x = random.randint(0, max_x_pos)
        random_y = random.randint(0, max_y_pos)
        
        label.move(random_x, random_y)  
        
        # Add the label to the list
        labels.append(label)

      
        if running_overlay:
            QTimer.singleShot(1000, lambda: show_image(index + 1))  


    show_image(0)
    
    app.exec_()  
