#import threading
from bot import bot
import os
from dotenv import load_dotenv

load_dotenv()

print("launching...")
if __name__ == "__main__":
    bot.run(os.getenv("FLICKO_YAM_TOKEN"))
