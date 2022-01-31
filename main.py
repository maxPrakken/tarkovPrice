# https://tarkov-market.com/dev/api
import os
import sys
import subprocess
import time
import numpy as np
import cv2
import pyautogui
import glob
from sys import platform

class MyImage:
    img = None
    name = ''

    def __init__(self, name):
        # print(name)
        self.name = name
        self.img = cv2.imread(name)


def trim_string(str):  # cuts off the slash and extention from filename
    l = len(str)
    sub1 = str[:l - 4]
    sub2 = sub1.split('/')
    return sub2[2]


def has_image(haystack, needle):
    haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
    needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
    w, h = needle.shape[::-1]
    res = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)

    y, x = np.unravel_index(res.argmax(), res.shape)
    return x, y

    threshold = 0.90
    loc = np.where(res >= threshold)
    try:
        assert loc[0][0] > 0
        assert loc[1][0] > 0
        return loc[1][0], loc[0][0]
    except:
        return -1, -1


def get_images(images, mode):
    filenames = []
    if mode == 'none':
        # get all from the items directory
        folder_names = os.listdir("items/.")
        folders = []

        for fname in folder_names:
            # check if object is folder
            if os.path.isdir(os.path.join(os.path.abspath("items/"), fname)):
                folders.append(fname)

        # if folders is not empty put all names of items in list
        if folders:
            for folder in folders:  # iterrate through folders and get items
                ilocation = "items/" + folder + "/*.png"
                tempnames = [img for img in glob.glob(ilocation)]
                filenames.append(tempnames)  # filenames is a list of lists with filenames

    else:
        for item in os.listdir("items/" + mode + "/"):
            ilocation = "items/" + mode + "/*.png"
            tempnames = [img for img in glob.glob(ilocation)]
            filenames.append(tempnames)

    # make a list of item screenshots
    for cat in filenames:
        for img in cat:
            myImage = MyImage(img)
            images.append(myImage)

# if run by itsself and not from other file
if __name__ == "__main__":
    apikey = open("apikey.txt", "r").read()
    apikey = apikey.rstrip() #strip newlines from apikey

    mode = input('Search for type: \n')
    if mode == "": # input something to search only that catagory
        mode = 'none' # go through all catagories

    # take screenshot
    # screenshot = pyautogui.screenshot()

    # pyautogui takes PIL(pillow) and RGB needs to convert to
    # numpy array and BGR so we can write to disk

    # screenshot = cv2.cvtColor(np.array(screenshot),
    # cv2.COLOR_RGB2BGR)
    images = []
    get_images(images, mode)

    screenshot = cv2.imread("screenshots/screenshot.png")

    # cv2.imwrite("screenshot.jpg", screenshot)

    for img in images:
        mi = MyImage(img.name)
        x, y = has_image(screenshot, mi.img)

        if x >= 0 and y >= 0:
            trmstr = trim_string(img.name)

            # print("found " + img.name)
            command = 'curl -H x-api-key:' + apikey + ' https://tarkov-market.com/api/v1/item?q=' + trmstr
            print(command)
            # captures output into res and converts to str due to text=true

            res = None

            basefirst = None
            basesecond = None
            pricefirst = None
            pricesecond = None
            namefirst = None
            namesecond = None

            # checks for OS, linux or windows. just for development
            if platform == "linux" or platform == "linux2":
                res = os.popen(command).read()

                # base indexes
                basefirst = res.index("basePrice")
                basesecond = res.find(',', basefirst)

                pricefirst = res.index("price")
                pricesecond = res.find(',', pricefirst)

                traderfirst = res.index("traderPrice")
                tradersecond = res.find(',', traderfirst)

                namefirst = res.index("name")
                namesecond = res.find(',', namefirst)

                print('\n' + res[namefirst:namesecond])
                print(res[basefirst:basesecond])
                print(res[pricefirst:pricesecond])
                print(res[traderfirst:tradersecond])
                print('\n========================================\n')

            # if running on windows
            elif platform == "win32":
                res = subprocess.run(command, capture_output=True, text=True)

                # base indexes
                basefirst = res.stdout.index("basePrice")
                basesecond = res.stdout.find(',', basefirst)

                pricefirst = res.stdout.index("price")
                pricesecond = res.stdout.find(',', pricefirst)

                traderfirst = res.stdout.index("traderPrice")
                tradersecond = res.stdout.find(',', traderfirst)

                namefirst = res.stdout.index("name")
                namesecond = res.stdout.find(',', namefirst)

                print('\n' + res.stdout[namefirst:namesecond])
                print(res.stdout[basefirst:basesecond])
                print(res.stdout[pricefirst:pricesecond])
                print(res.stdout[traderfirst:tradersecond])
                print('\n========================================\n')

        #    w, h, _ = img.shape
        #    cv2.rectangle(screenshot, (x, y), (x+h, y+w), (255, 0, 0), 2)

        else:
            print("Not found")

    # cv2.imshow("Found the item at (%d,%d)" % (x, y), screenshot)
    cv2.waitKey(0xFFFF)

else:
    print(quit)
    quit()
