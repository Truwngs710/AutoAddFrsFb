import random
import cv2
import numpy as np
import os
import pyautogui
import time


def find_image_on_screen(template_path, threshold=0.9):
    # Load the template image
    template = cv2.imread(template_path, 0)

    # Get the screen image
    screenshot = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Match the template with the screen image
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    # Get the coordinates of the matched region
    coordinates = list(zip(*locations[::-1]))

    # Calculate the center position of the bounding box
    centers = []
    for loc in coordinates:
        w, h = template.shape[::-1]
        center_x = loc[0] + w // 2
        center_y = loc[1] + h // 2
        centers.append((center_x, center_y))

    return centers[1::2]

def auto_click_on_centers(centers):
    for center in centers:
        # Move the mouse to the center position
        pyautogui.moveTo(center[0], center[1])

        # Click at the center position
        pyautogui.click()

        time.sleep(random.choice([0.2,0.3,0.4,0.5]))

# Example usage
folder_path = 'C:\\Users\\User2\\Desktop\\Py\\Auto add friends\\image'
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

def auto_click_add():
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        centers = find_image_on_screen(image_path)

        if centers:
            print(f"Position: {centers}")
            auto_click_on_centers(centers)
        else:
            print(f"Image '{image_file}' not found.")

def detect_image(template_path, threshold=0.9):
    # Load the template image
    template = cv2.imread(template_path, 0)

    # Get the screen image
    screenshot = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Match the template with the screen image
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    # Get the coordinates of the first matched region
    if len(locations[0]) > 0:
        x, y = locations[1][0], locations[0][0]
        center_x = x + template.shape[1] // 2
        center_y = y + template.shape[0] // 2
        center_position = (center_x, center_y)
        is_image_found = True
    else:
        center_position = None
        is_image_found = False

    return is_image_found, center_position

def detect_ok_btn():
    # Example usage
    template_path = 'C:\\Users\\User2\\Desktop\\Py\\Auto add friends\\ok.png'
    is_image_found, image_positions = detect_image(template_path)

    if is_image_found:
        print(f"OK Button: {image_positions}")
        pyautogui.moveTo(image_positions[0], image_positions[1])
        pyautogui.click()
        pyautogui.scroll(800)
        time.sleep(0.8)
        auto_click_add()
    else:
        print("No OK button!!!")
        pyautogui.scroll(800)
        time.sleep(0.8)
        auto_click_add()

    
while True:
    detect_ok_btn()
    time.sleep(5)
