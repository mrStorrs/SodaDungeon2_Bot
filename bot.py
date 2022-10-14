# https://www.classicgame.com/game/Whack+a+Mole

#imports
from re import template
import cv2
import pyautogui
import os
import numpy as np
from time import sleep

os.chdir(os.path.dirname(os.path.abspath(__file__)))


#could set a "last action to move back if no new aciton is found."
actions = {
    "enterInn": False,
    "partyStand": False,
    "partyHire" : False,  
    "partyHired" : False,  
    "dungeon" : False,  
    "arrow" : False,  
    "go" : False,  
    "go2" : False,  
    "sky" : False,  
    "exit" : False,  
    "exitContinue" : False,  
    "exitYes" : False,  
    "exit2" : False,  
}

#No cooldown time
pyautogui.PAUSE = 0

class Image:
  def __init__(self, imagePath):
    self.match = cv2.imread(imagePath)
    self.match_gray = cv2.cvtColor(self.match, cv2.COLOR_RGB2GRAY)
    self.w, self.h = self.match_gray.shape[::-1]
    self.loot_index = 0


#turn these to objects. 
#template and dimensions
match_inn = Image("imgs/inn.png")
match_partyStand = Image("imgs/partyStand.png")
match_partyHire = Image("imgs/partyHire.png")
match_partyHired = Image("imgs/partyHired.png")
match_Dungeon = Image("imgs/dungeon.png")
match_Arrow = Image("imgs/arrow.png")
match_Go = Image("imgs/go.png")
match_Go2 = Image("imgs/go2.png")
match_Sky = Image("imgs/sky.png")
match_exit = Image("imgs/exit.png")
match_exitYes = Image("imgs/exitYes.png")
match_exitContinue = Image("imgs/exitContinue.png")

# game window dimensions
x, y, w, h = 5, 30, 1920, 1083

#wait
sleep(2)

#functions
def findLocationToClick(template, image_gray, screen, key):
        result = cv2.matchTemplate(
            image_gray,
            template.match_gray,
            cv2.TM_CCOEFF_NORMED
        )

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        #threshold
        if max_val >= 0.9:
            sleep(0.1)

            if key is "sky":
                pyautogui.press('Escape')
            if key is "exit":
                actions["exitContinue"] = True

            if key is not "sky":
                pyautogui.click(
                    x = max_loc[0] + x, #screen x
                    y = max_loc[1] + y  #screen y
                )

            screen = cv2.rectangle(
                img = screen,
                pt1 = max_loc,
                pt2 = (
                    max_loc[0] + template.w, # = pt2 x 
                    max_loc[1] + template.h # = pt2 y
                ),
                color = (0,0,255),
                thickness = -1 #fill the rectangle
            )
            ##todo put an action in here that checks to make sure the 
            #screen has moved on before  
            actions[key] = True

            if key is "partyHired":
                pyautogui.press('Escape')
                sleep(0.5) 
                pyautogui.press('Escape')

            if key is "exit2": #reset keys
                pyautogui.screenshot("imgsLoot/" + str(template.loot_index) + ".png", (x, y, w, h))
                template.loot_index += 1
                for key in actions:
                    actions[key] = False

        elif key is "exit":
            pyautogui.press('Escape')
            sleep(0.2)
            findLocationToClick(match_exitContinue, image_gray, screen, "exitContinue")

#main
while True:

    #screenshot
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    # screen = cv2.imread(screen)
    print ("#--------------------------#")

    # while True:

        #show what the computer sees
    image_mini = cv2.resize(
        src = screen,
        dsize = (450,350) #must be integer, not float
    )
    cv2.imshow("vision", image_mini)
    cv2.waitKey(10)

    image_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

    for key in actions:
        print (key + " : " + str(actions[key]))

        if not actions[key]:
            if key is "enterInn":
                findLocationToClick(match_inn, image_gray, screen, key)
            if key is "partyStand":
                findLocationToClick(match_partyStand, image_gray, screen, key)
            if key is "partyHire":
                # sleep(0.2)
                findLocationToClick(match_partyHire, image_gray, screen, key)
            if key is "partyHired":
                findLocationToClick(match_partyHired, image_gray, screen, key)
            if key is "dungeon":
                findLocationToClick(match_Dungeon, image_gray, screen, key)
            if key is "arrow":
                findLocationToClick(match_Arrow, image_gray, screen, key)
            if key is "go":
                findLocationToClick(match_Go, image_gray, screen, key)
            if key is "go2":
                findLocationToClick(match_Go2, image_gray, screen, key)
            if key is "sky":
                findLocationToClick(match_Sky, image_gray, screen, key)
            if key is "exit":
                findLocationToClick(match_exit, image_gray, screen, key)
            if key is "exitYes":
                findLocationToClick(match_exitYes, image_gray, screen, key)
            if key is "exit2":
                # sleep(1)
                findLocationToClick(match_exit, image_gray, screen, key)
                #reset keys to start over
            break







