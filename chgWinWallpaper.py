#! python3

import ctypes, os, winreg, sys
from winreg import *

def chgWallpaper(imgPath):
    print('New Desktop Wallpaper image:\n' + imgPath)
    SetDesktopWallpaper = 20
    UpdateIniFile = 0x01
    SendWinIniChange = 0x02
    ctypes.windll.user32.SystemParametersInfoW(SetDesktopWallpaper, 0, imgPath, UpdateIniFile | SendWinIniChange)

def getRegValue(regValue):
    subKeys = r"Control Panel\Desktop"
    regKey = OpenKey(ConnectRegistry(None,HKEY_CURRENT_USER), subKeys)
    print('Getting registry Value from Key:\n%s  ...' % subKeys)
    for i in range(1024):
        try:
            val=QueryValueEx(regKey, regValue)
            return val
        except EnvironmentError:
            break

# Function to match file number from registry path to file number in local wallpaper folder 'D:\xkcd'
def getNewImgPath(regImgNmbr):
    for file in os.listdir('filepath\\xkcd'): # "filepath" is a placeholder for your file path
        imgNmbr = (file[:file.find(' ')]).strip()
        imgNmbr = int(imgNmbr)
        if regImgNmbr == imgNmbr:
            newImgPath = os.path.join("filepath\\xkcd\\" + file) # "filepath" is a placeholder for your file path
            return newImgPath
        else:
            pass


# Call getRegValue function and pass it 'WallPaper' value to get 'WallPaper' value DATA (file path) from registry
regImgPath = getRegValue('WallPaper')
print('\nWallPaper registry Value image path:\n' + regImgPath[0] +'\n')

# Get basename of [0] index which is path for 'WallPaper'
regImgBase = (os.path.basename(regImgPath[0]))
# Get file number (string) from path
regImgBaseNmbr = (regImgBase[:regImgBase.find(' ')]).strip()

# Convert file number (string) to integer, if filename does not start with a number, catch error and end script
try:
    regImgBaseNmbr = int(regImgBaseNmbr)
except ValueError:
    print('INVALID FILENAME')
    sys.exit()
    
# Add 1 to file number
regImgNmbr = regImgBaseNmbr + 1

# Call getNewImgPath function and pass it 'regImgNmbr' value (which added 1 to regImgBaseNmbr)
newImgPath = getNewImgPath(regImgNmbr)

# Call 'chgWallpaper' function and pass it new image path ('newImgPath') to change Wallpaper
if newImgPath != None:
    chgWallpaper(newImgPath)
else:
    print('New image path not found')
