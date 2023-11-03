import tkinter as tk
import pyautogui
import keyboard
import easyocr
from googletrans import Translator
import config

# Initialize the EasyOCR reader
reader = easyocr.Reader([config.FROM_LANGUAGE])

# Create the main Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window

window_active = 0


# Translation function
def translate_text(text):
    try:
        translator = Translator()
        translated = translator.translate(
            text, src=config.FROM_LANGUAGE, dest=config.TO_LANGUAGE
        )
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return "Nothing to translate"


# Create a list to store OCR results and their coordinates
overlay_data = []
overlays = []


# Function to add OCR results to the list
def add_overlay_data(text, original_text, coordinates):
    overlay_data.append((text, original_text, coordinates))


# Function to display all overlays at once
def display_overlays():
    global window_active
    for text, original_text, coordinates in overlay_data:
        display_overlay(text, original_text, coordinates)
    overlay_data.clear()  # Clear the list after displaying
    window_active = 2


# Allow the user to toggle between the original and translated text
def toggle_text(label, original_text, text):
    if label["text"] == original_text:
        label["text"] = text
    else:
        label["text"] = original_text


# Create a function to display the overlay
def display_overlay(text, original_text, coordinates):
    try:
        overlay = tk.Toplevel(root)
        overlay.attributes("-topmost", True)  # Make overlay stay on top
        overlay.overrideredirect(True)  # Remove window borders

        # Extract position and size from the coordinates
        x_coords = [int(coord[0]) for coord in coordinates]
        y_coords = [int(coord[1]) for coord in coordinates]
        x_position = min(x_coords)
        y_position = min(y_coords)
        width = max(x_coords) - x_position
        height = max(y_coords) - y_position

        overlay.geometry(
            f"{width}x{height}+{x_position}+{y_position}"
        )  # Set the position of the overlay

        label = tk.Label(
            overlay, text=text, font=("Helvetica", 24), bg="black", fg="white"
        )
        label.pack()
        label.original_text = (
            original_text  # Store the original Japanese text in the label
        )
        label.original_coordinates = (
            width,
            height,
        )  # Store the original coordinates in the label
        label.bind("<Button-1>", lambda event: toggle_text(label, original_text, text))
        overlays.append(overlay)
    except Exception as e:
        print(f"Error displaying overlay: {e}, {coordinates}")


# Function to perform OCR
def ocr():
    # Capture a screenshot and save it
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")

    # Perform OCR on the saved screenshot
    extracted_text = reader.readtext("screenshot.png")

    # Extract the prompt from the OCR results
    for result in extracted_text:
        if result[2] < 0.03:
            continue
        trans = translate_text(result[1])
        add_overlay_data(trans, result[1], result[0])

    # Display all collected overlays at once
    display_overlays()


def ai_icon():
    display_overlay("Loading", None, [(0, 0), (200, 50)])


def kill_overlay():
    global window_active
    for overlay in overlays:
        overlay.destroy()
    overlays.clear()  # Clear the list after displaying
    window_active = 0


def ocr_controller():
    global window_active
    if window_active == 0:
        window_active = 1
        ai_icon()
        ocr()
        overlays.pop(0).destroy()
    elif window_active == 2:
        kill_overlay()


keyboard.add_hotkey(config.ACTIVE_KEY, ocr_controller)

print("Script is ready")
print(f"Press {config.ACTIVE_KEY} to start OCR, press again will close it")
print("Click on the overlay to toggle between original and translated text")
print("Press Ctrl+C to exit")

root.mainloop()
