import mss
import numpy as np
import cv2
import time
import pygetwindow as gw
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'A:\MyTest_Software\tesseract.exe'  # Adjust path as necessary

# Function to capture ROI's
def capture():
    with mss.mss() as sct:
        # Capture the screen
        monitor = sct.monitors[1]  # 1 indicates the primary monitor
        screenshot = sct.grab(monitor)

        # Convert the raw image to a NumPy array
        img = np.array(screenshot)

        rois = {
            'game_field': (25, 100, 1910, 1020),  # Coordinates for the game field
            'minimap': (825, 860, 270, 170)  # Coordinates for mini-map
        }

        rois_ocr = {
            'score': (200, 90, 150, 120),      # Coordinates for the score
            'timer': (102, 88, 100, 60),     # Coordinates for the timer
            'HOME_Player_Name': (110, 970, 420, 70),  # Coordinates for HOME player names
            'AWAY_Player_Name': (1400, 970, 420, 70),  # Coordinates for AWAY player names
        }

        return img, rois, rois_ocr

#function to process roi's
def process_rois(img, rois, rois_ocr):
    roi_data = {}

    # Process regular ROIs
    for name, (x, y, w, h) in rois.items():
        roi = img[y:y+h, x:x+w]
        roi_data[name] = roi

    # Process OCR ROIs
    for name, (x, y, w, h) in rois_ocr.items():
        roi = img[y:y+h, x:x+w]
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(roi_gray, lang='eng', config='--psm 7')
        roi_data[name] = text.strip()

    return roi_data

# Function to generate commentary based on the processed ROI data
def generate_commentary(roi_data):
    commentary = ""

    if 'score' in roi_data:
        commentary += f"Current score: {roi_data['score']}. "

    if 'timer' in roi_data:
        commentary += f"Match time: {roi_data['timer']}. "

    if 'HOME_Player_Name' in roi_data:
        commentary += f"Home player: {roi_data['HOME_Player_Name']}. "

    if 'AWAY_Player_Name' in roi_data:
        commentary += f"Away player: {roi_data['AWAY_Player_Name']}. "

    return commentary


def main():
    while True:
        # Get the active window
        active_window = gw.getActiveWindow()

        # Check if the active window is PES 2021
        if active_window and "eFootball" in active_window.title:
            print("PES 2021 is in focus. Starting screen capture and processing.")
            while True:  # Start a loop to take screenshots every second
                # Capture the screen and ROIs
                img, rois, rois_ocr = capture()

                # Process the ROIs
                roi_data = process_rois(img, rois, rois_ocr)

                # Generate commentary based on the processed ROI data
                commentary = generate_commentary(roi_data)

                print("Commentary:", commentary)  # Print the generated commentary
                time.sleep(3)  # Wait for 1 second before taking the next screenshot
        else:
            print("Waiting for PES 2021 to be in focus...")
            time.sleep(2)  # Wait for 2 seconds before checking again

if __name__ == "__main__":
    main()
