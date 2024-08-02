"""
@author: Gean Maidana Dollanarte
"""

import time
from OBSLogger import OBSLogger 
from ScreenshotManager import ScreenshotManager

def main():
    '''
    This main() function just loops and calls the appropriate object functions to take screenshots and retrieve the text,
    as well as add to and update the record when we detect a win or a loss from the screenshot
    '''
    record_path = "record.txt"
    logger = OBSLogger.get_instance(record_path)
    sm = ScreenshotManager()

    print(f"Initial record: Wins: {logger.get_num_wins()}, Losses: {logger.get_num_losses()}")
    print()

    while True:
        result = sm.capture_and_process_screenshot()

        if "VICTORY" in result:
            print("Victory detected! Sleeping timer for 5 minutes.")
            logger.add_win()
            print(f"Current record: Wins: {logger.get_num_wins()}, Losses: {logger.get_num_losses()}")
            time.sleep(300) # 300s = 5 mins

        elif "DEFEAT" in result:
            print("Defeat detected! Sleeping timer for 5 minutes")
            logger.add_loss()
            print(f"Current record: Wins: {logger.get_num_wins()}, Losses: {logger.get_num_losses()}")
            time.sleep(300) # 300s = 5 mins  

            
        else:
            print("No condition detected!")

        time.sleep(0.2) # Take screenshots every 0.2s, adjust as needed.

if __name__ == "__main__":
    main()