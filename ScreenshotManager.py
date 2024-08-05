"""
@author: Gean Maidana Dollanarte
"""

import pytesseract
import cv2
import numpy as np
import pyautogui
import Levenshtein

# Outcomes we want (in-game "victory" has an exclamation point, but if we get a perfect match without the exclamation point, we'll take it!)
ocr_strings = ["VICTORY", "DEFEAT", "VICTORY!"] 

# The Levenshtein distance - how close we want our imperfect output to be to any given word in ocr_strings
l_distance = 4 

# Crop configurations:
# 1. OpenCV coordinate (0,0) starts at top left. 
# 2. X-axis will go from left to right
# 3. Y-axis will go from top to bottom
# 4. I used GIMP to manually figure out my start/end points for cropping
#    x = my start point coordinate
#    width = my end point coordinate - my start point coordinate
#    Same logic applies to y and height
# 5. Coordinates are for 1920x1080, feel free to manually tweak if you have different monitor resolution
# 6. On a final note, while you should try to avoid noise because it messes with OCR, cropping too small
#    will lead to no text detection, so be careful with cropping too small if you mess with these numbers

# Live program coordinates (e.g. debug_mode = False)
x = 690
y = 330 
width = 570 
height = 370

# Testing coordinates for pre-determined images in debug_mode
# They differ from live program coordinates because my manual screenshots aren't perfectly 1920x1080 since I took
# manual screenshots with Gyazo
# x = 690
# y = 260 
# width = 570 
# height = 370

# This
class ScreenshotManager:
    """
    Holds functionality for taking screenshot, pre-processing screenshot with OpenCV, and detecting text from the
    pre-processed screenshot using Tesseract 
    """

    def __init__(self):
        """
        Variables for whether to manually test screenshots or run the program live (e.g. not in debug mode)
        """
        

        # To run program live and still write (save) screenshots, set debug_mode = True, and in the if condition, change to "if not self.debug_mode"
        self.debug_mode = False 

        # Displays images when running the program, not necessary for live running or when not debugging image detection
        self.display_images = False 

        # Update this path to where-ever yours is
        # Tesseract-OCR files are from UB-Mannheim (University of Mannheim)
        pytesseract.pytesseract.tesseract_cmd = r'F:\Tesseract-OCR\tesseract.exe'  

    def capture_and_process_screenshot(self):

        # This is for manually testing with a pre-determined screenshot
        # I wouldn't waste too much time tweaking any functions to preprocess and perfectly detect a pre-determined image 
        # because one bad pre-determined image can inadvertently force you to change a good OCR pre-processing method
        
        if self.debug_mode:

            # Load image and display it
            victory_image = cv2.imread("debug/manual/permanent/victory.JPG")  
            if self.display_images:           
                cv2.imshow("victory image", victory_image)
                cv2.waitKey(0)

            # Crop image
            cropped_vic = self.crop(victory_image, "debug/manual/victory/croppedVICTORY.JPG")
                     
            # Invert image
            self.invert_image(cropped_vic, "debug/manual/victory/invertedVICTORY.jpg")
                
            # Convert to greyscale 
            grey_vic = self.convert_img_to_greyscale(cropped_vic, "debug/manual/victory/greyscaleVICTORY.jpg")
            
            # Binarize
            bw_vic = self.binarize_image(grey_vic, "debug/manual/victory/vic_bw_image.jpg")

            # Invert (We invert again so our text is black on white background, I had more success with this pre-processing method)
            bw_vic = self.invert_image(bw_vic, "debug/manual/victory/invertedVICTORY.jpg") 

            ocr_result = pytesseract.image_to_string(bw_vic)
            ans = self.process_conditions(ocr_result)
            print("Binarized victory image text: ", ans)
            print()

            return ans
            
        
        else:
            # The called function as well as the crop configuration variables are perfected for 1920x1080 resolution
            screenshot = self.capture_screenshot("debug/manual/live/OriginalSCREENSHOT.JPG")

            # Preprocess screenshot by cropping, inverting, greyscaling, binarizing, and inverting again
            cropped_img = self.crop(screenshot, "debug/manual/live/croppedSCREENSHOT.JPG")

            self.invert_image(cropped_img, "debug/manual/live/inverted1SCREENSHOT.jpg")

            grey_img = self.convert_img_to_greyscale(cropped_img, "debug/manual/live/greyscaleSCREENSHOT.jpg")

            bw_img = self.binarize_image(grey_img, "debug/manual/live/bianarized_image.jpg")

            bw_img = self.invert_image(bw_img, "debug/manual/live/invertedAfterBianarizeVICTORY.jpg") 

            ocr_result = pytesseract.image_to_string(bw_img)
            ans = self.process_conditions(ocr_result)

            return ans
        
        
    def capture_screenshot(self, save_path):
        image = pyautogui.screenshot(region=(0, 0, 1920, 1080))
        image = cv2.cvtColor(np.array(image),cv2.COLOR_BGR2HSV_FULL)
        if self.debug_mode:
            cv2.imwrite(save_path, image)
        return image
    
    def crop(self, img, save_path):
        cropped_img = img[y:y+height, x:x+width]
        if self.debug_mode:
            cv2.imwrite(save_path, cropped_img)
        if self.display_images:
            cv2.imshow("cropped image", cropped_img)
            cv2.waitKey(0)
        return cropped_img

    '''
    Refer to my "victory" image folder that I used to test these functions on a pre-determined screenshot
    in order to see what effect these functions and my pre-processing method has on a screenshot
    '''
    def invert_image(self, img, save_path):
        inverted_img = cv2.bitwise_not(img)
        if self.debug_mode:
            cv2.imwrite(save_path, inverted_img)
        if self.display_images:
            cv2.imshow("inverted image", inverted_img)
            cv2.waitKey(0)
        return inverted_img
    
    def convert_img_to_greyscale(self, img, save_path):
        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.debug_mode:
            cv2.imwrite(save_path, grey_img)
        if self.display_images:
            cv2.imshow("greyscale image", grey_img)
            cv2.waitKey(0)
        return grey_img


    def binarize_image(self, img, save_path): 
        # Black and white processing
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=3)
        img = cv2.GaussianBlur(img, (5,5), 0)
        if self.debug_mode:
            cv2.imwrite(save_path, img)
        if self.display_images:
            cv2.imshow("thresh img", img)
            cv2.waitKey(0)
        return img
     
    def process_conditions(self, txt):
        print("OCR detected: ", txt, end='') # Text already has \n

        if txt in ocr_strings:
            return txt
        
        # Use Levenshtein distance for better matching
        txt = txt.strip().upper()

        # We will splice because we don't need to include both "VICTORY" and "VICTORY!"
        # The reason we have both is because in-game, the victory screen has an exclamation point (defeat does not, however)
        for word in ocr_strings[0:2]: 
            if Levenshtein.distance(txt, word) <= l_distance:
                return word

        return "NONE"

