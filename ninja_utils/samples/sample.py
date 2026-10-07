import time
from ninja_utils import get_logger, NonBlockingKeyboard

def main():
    """
    Demonstrates the usage of the ninja_utils library.
    """
    # Initialize the logger
    logger = get_logger(__name__)
    logger.info("Logger initialized.")
    logger.info("Press any key to see it detected. Press 'q' to quit.")

    # Use the non-blocking keyboard
    with NonBlockingKeyboard() as nkb:
        while True:
            if nkb.kbhit():
                key = nkb.getch()
                logger.info(f"Key pressed: {key}")
                if key == 'q':
                    logger.warning("Quit key 'q' pressed. Exiting.")
                    break
            
            # Do other work here
            print(".", end="", flush=True)
            time.sleep(0.1)
    
    print("\nExited.")

if __name__ == "__main__":
    main()

