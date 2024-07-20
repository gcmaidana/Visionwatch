import random
import pytesseract
import cv2
import numpy as np
import re
from PIL import Image

# To-do: att the end when im done, dont write an image ifn ot necessar,y just less efficeint program

ocr_strings = ["VICTORY", "VICTORY!" "DRAW", "DEFEAT"]

# Crop configurations
# OpenCV coordinates (0,0) start at top left. 
# X-axis will go from left to right
# Y-axis will go from top to bottom
# I used GIMP to manually figure out my start/end points
# x = my start point coordinate
# width = my end point coordinate - my start point coordinate
# Same logic applies to y and height
# This is for 1920x1080, feel free to manually tweak if you have different monitor resolution
# Final note, while you should try to avoid noise because it messes with OCR, cropping too small
# will lead to no text detection, so be careful
x = 690
y = 260 
width = 570 
height = 370


class ScreenshotManager:
    def __init__(self):
        self.debug_mode = True # This is for manually testing screenshots, turn off when running live
        pytesseract.pytesseract.tesseract_cmd = r'F:\Tesseract-OCR\tesseract.exe'  # Update this path to where-ever yours is

    def capture_and_process_screenshot(self):

        if self.debug_mode:


            # Load images
            victory_image = cv2.imread("debug/manual/permanent/victory.JPG")
            draw_image = cv2.imread("debug/manual/permanent/draw.JPG")  
            defeat_image = cv2.imread("debug/manual/permanent/defeat.JPG")
            cv2.imshow("victory image", victory_image)
            cv2.waitKey(0)
            cv2.imshow("draw image", draw_image)
            cv2.waitKey(0)
            cv2.imshow("defeat image", defeat_image)
            cv2.waitKey(0)

            # Crop images
            cropped_vic = self.crop(victory_image, "debug/manual/victory/croppedVICTORY.JPG")
            cropped_draw = self.crop(draw_image, "debug/manual/draw/croppedDRAW.JPG")
            cropped_def = self.crop(defeat_image, "debug/manual/defeat/croppedDEFEAT.JPG")
            

            
            # Invert images
            self.invert_image(cropped_vic, "debug/manual/victory/invertedVICTORY.jpg")
            self.invert_image(cropped_draw, "debug/manual/draw/invertedDRAW.jpg")
            self.invert_image(cropped_def, "debug/manual/defeat/invertedDEFEAT.jpg")


            # Binarization     
            # Convert to greyscale first
            grey_vic = self.convert_img_to_greyscale(cropped_vic, "debug/manual/victory/greyscaleVICTORY.jpg")
            grey_draw = self.convert_img_to_greyscale(cropped_draw, "debug/manual/draw/greyscaleDRAW.jpg")
            grey_defeat = self.convert_img_to_greyscale(cropped_def, "debug/manual/defeat/greyscaleDEFEAT.jpg")
            
            # Now bianarize, invert, and detect text (we invert again so our text is black on white background, I had more success with this)
            bw_vic = self.binarize_image(grey_vic, "debug/manual/victory/vic_bw_image.jpg")
            bw_vic = self.invert_image(bw_vic, "debug/manual/victory/invertedVICTORY.jpg") 
            ocr_result = pytesseract.image_to_string(bw_vic)
            ans = self.process_conditions(ocr_result)
            print("Binarized victory image text: ", ans)
            print()

            bw_draw = self.binarize_image(grey_draw, "debug/manual/draw/draw_bw_image.jpg")
            bw_draw = self.invert_image(bw_draw, "debug/manual/draw/invertedDRAW.jpg")
            ocr_result = pytesseract.image_to_string(bw_draw)
            ans = self.process_conditions(ocr_result)
            print("Binarized draw image text: ", ans)
            print()

            bw_def = self.binarize_image(grey_defeat, "debug/manual/defeat/def_bw_image.jpg") 
            bw_def = self.invert_image(bw_def, "debug/manual/defeat/invertedDEFEAT.jpg")
            ocr_result = pytesseract.image_to_string(bw_def)
            ans = self.process_conditions(ocr_result)
            print("Binarized defeat image text: ", ans) 
            print()



        return;
        '''
         else:
            screenshot = self.capture_screenshot()
            os.makedirs("debug/images", exist_ok=True)
            cv2.imwrite(f"debug/images/OGimage{self.count}.png", screenshot)
            print("Original screenshot saved!")

            # Crop the screenshot (adjust these values as needed)
            height, width = screenshot.shape[:2]
            x = int(width * 0.25)
            y = int(height * 0.33)
            crop_width = int(width * 0.5)
            crop_height = int(height * 0.33)
            cropped_screenshot = screenshot[y:y+crop_height, x:x+crop_width]

            cv2.imwrite(f"debug/images/crop{self.count}.png", cropped_screenshot)
            print("Cropped screenshot saved!")

            # Convert to grayscale
            gray_screenshot = cv2.cvtColor(cropped_screenshot, cv2.COLOR_BGR2GRAY)

            cv2.imwrite(f"debug/images/grayscale{self.count}.png", gray_screenshot)
            print("Grayscale screenshot saved!")

            # Perform OCR
            pytesseract.image_to_string(gray_screenshot, config='--psm 7 -c tessedit_char_whitelist=DRAWVICTORYDEFEAT')
            print(f"Detected text: {text.strip()}")

            return text.strip()
        
        '''
        
    def capture_screenshot(self):
        # Was gonna use pillow for screenshot, now ill just pyautogui

        image = pyautogui.screenshot(region=(0,0,1920,1080))
        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV_FULL)
    
    def crop(self, img, save_path):
        cropped_img = img[y:y+height, x:x+width]
        cv2.imwrite(save_path, cropped_img)
        cv2.imshow("cropped image", cropped_img)
        cv2.waitKey(0)
        return cropped_img


    def invert_image(self, img, save_path):
        inverted_img = cv2.bitwise_not(img)
        cv2.imwrite(save_path, inverted_img)
        cv2.imshow("inverted image", inverted_img)
        cv2.waitKey(0)
        return inverted_img
    
    def convert_img_to_greyscale(self, img, save_path):
        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(save_path, grey_img)
        cv2.imshow("greyscale image", grey_img)
        cv2.waitKey(0)
        return grey_img


    def binarize_image(self, img, save_path): 
        # Black and white processing
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=3)
        img = cv2.GaussianBlur(img, (5,5), 0)
        cv2.imwrite(save_path, img)
        cv2.imshow("thresh img", img)
        cv2.waitKey(0)
        return img
     
    def process_conditions(self, txt):
        print("OCR detected: ", txt, end='') # Text already has \n

        if txt in ocr_strings:
            return txt
        
        # Cases wher we have something like "0RAW" or "VICTO" e.g. incomplete words due to imperfect OCR detection
        elif re.search('[VICO]', txt, re.I):
                return "VICTORY" 
        elif re.search('[A]', txt, re.I):
                return "DRAW"
        elif re.search('[EF]', txt, re.I):
            return "DEFEAT"
        else:
            return "NONE" 

