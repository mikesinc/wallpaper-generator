import ctypes
import os
import urllib.request
import praw
from PIL import Image

user32 = ctypes.windll.user32

def getScreensize():
    try:
        user32 = ctypes.windll.user32
        screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
        return screensize
    except:
        print("Something went wrong obtaining screen size.")
        exit()

#Source Image from /r/wallpaper
def getImage():
    directory = os.getcwd() + "/.wallpaper"
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = directory + "/" + "daily_wallpaper" + ".png"
    screensize = getScreensize()
    try:
        reddit = praw.Reddit('bot1', user_agent='Wallpaper Extraction (by /u/reqr)')
        wallpaper_url = list(reddit.subreddit("wallpapers").top(time_filter='day'))[0].url
        urllib.request.urlretrieve(wallpaper_url, filepath)
        #Resize to screen and save over yesterday's image
        Image.open(filepath).resize(screensize).save(filepath)
        return filepath
    except:
        print("Something went wrong downloading the image")
        exit()

#Set Wallpaper
try:
    wallpaper = getImage()
    user32.SystemParametersInfoW(20, 0, wallpaper, 0)
except:
    print("Something went wrong setting your wallpaper.")
    exit()