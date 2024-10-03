import mss
import numpy as np
import cv2
import time
import pygetwindow as gw
import pytesseract
import os

#hi

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'A:\MyTest_Software\tesseract.exe'  # Adjust path as necessary

# Function to capture and process the screen
def capture_and_process():
    with mss.mss() as sct:
        # Capture the screen
        monitor = sct.monitors[1]  # 1 indicates the primary monitor
        screenshot = sct.grab(monitor)

        # Convert the raw image to a NumPy array
        img = np.array(screenshot)

        # Define the regions of interest (ROIs)
        rois = {
            'game_field': (25, 100, 1910, 1020),  # Coordinates for the game field
            'score': (200, 90, 150, 120),      # Coordinates for the score
            'timer': (102, 88, 100, 60),     # Coordinates for the timer
            'HOME_Player_Name': (110, 970, 420, 70),  # Coordinates for HOME player names
            'AWAY_Player_Name': (1400, 970, 420, 70),  # Coordinates for AWAY player names
            'minimap': (825, 860, 270, 170)  # Coordinates for mini-map
        }

        # Create a folder to save the ROIs
        for name, (x, y, w, h) in rois.items():
            os.makedirs(f"ROIs/{name}", exist_ok=True)  # Create a folder for each ROI

        # Initialize an empty dictionary to hold ROIs and their extracted data
        roi_data = {}

        # Display and save each ROI
        for name, (x, y, w, h) in rois.items():
            roi = img[y:y+h, x:x+w]

        # Convert ROI to grayscale if applicable
        if name in ['score', 'timer', 'HOME_Player_Name', 'AWAY_Player_Name']:
            roi_processed = convert_to_grayscale(roi, name)
            roi = roi_processed

            # Get the current timestamp for unique filenames
            timestamp = time.strftime("%H%M%S")  # Format: HHMMSS
            cv2.imwrite(f"ROIs/{name}/{name}_{timestamp}_{int(time.time() * 1000)}.jpg", roi)  # Save the ROI with a timestamp and milliseconds

            cv2.imshow(f"{name} ROI", roi)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return roi_data

def convert_to_grayscale(roi, name):
    """Convert specified ROIs to grayscale."""
    if name in ['score', 'timer', 'HOME_Player_Name', 'AWAY_Player_Name']:
        return cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return roi


# Main loop to check the active window
def main():
    while True:
        # Get the active window
        active_window = gw.getActiveWindow()
        
        # Check if the active window is PES 2021
        if active_window and "eFootball" in active_window.title:
            print("PES 2021 is in focus. Starting screen capture and processing.")
            while True:  # Start a loop to take screenshots every second
                roi_data = capture_and_process()
                print("Captured data:", roi_data)  # Print captured data for debugging
                time.sleep(3)  # Wait for 1 second before taking the next screenshot
        else:
            print("Waiting for PES 2021 to be in focus...")
            time.sleep(2)  # Wait for 2 seconds before checking again

if __name__ == "__main__":
    main()
