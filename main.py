import time
from OBSLogger import OBSLogger 
from ScreenshotManager import ScreenshotManager

def main():
    record_path = "record.txt"
    logger = OBSLogger.get_instance(record_path)
    sm = ScreenshotManager()

    print(f"Initial record: Wins: {logger.get_num_wins()}, Losses: {logger.get_num_losses()}, Draws: {logger.get_num_draws()}")
    print()

    while True:
        result = sm.capture_and_process_screenshot()

        if "VICTORY" in result:
            logger.add_win()
            print("Victory detected!")
        elif "DEFEAT" in result:
            logger.add_loss()
            print("Defeat detected!")
        elif "DRAW" in result:
            logger.add_draw()
            print("Draw detected!")

        print(f"Current record: Wins: {logger.get_num_wins()}, Losses: {logger.get_num_losses()}, Draws: {logger.get_num_draws()}")
        
        time.sleep(1.5)  # Adjust this value as needed to not detect a recently triggered condition more than once

if __name__ == "__main__":
    main()