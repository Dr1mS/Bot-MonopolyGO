import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import pytesseract
import re
import random
import time
import os
import time
import keyboard

# Fonction pour effacer la console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fonction pour afficher les informations du jeu
def print_game_info(game):
    clear_console()
    img_np = game.screenshot()
    print("Argent:")
    print(game.get_money(img_np))
    print("Dés:")
    print(game.get_dice(img_np))


def string_to_int(string):
    num = re.findall(r'[0-9]+', string)
    if not num:
        return None
    return int(''.join(num))



class GameManipulator:
    def __init__(self, window):
        self.window = window

    def screenshot(self):
        x, y, width, height = self.window.left, self.window.top, self.window.width, self.window.height
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot.save('cache/screenshot.png')
        return np.array(screenshot)

    def get_money(self, img_np):
        # La nouvelle position en haut au milieu de l'écran
        # Les valeurs doivent être ajustées pour cibler la zone exacte où se trouve la "box" de l'argent
        posX = (img_np.shape[1] // 2) - 20  # Centre X de l'écran
        posY = 70  # Haut de l'écran
        width = 250  # Largeur de la zone à capturer (à ajuster)
        height = 50  # Hauteur de la zone à capturer (à ajuster)

        # Rogner l'image à la zone spécifiée
        rogne = img_np[posY:posY+height, posX-width//2:posX+width//2]

        #Enregistrer l'image pour débogage si nécessaire
        cv2.imwrite('cache/rogne.png', rogne)

        # Utiliser pytesseract pour reconnaître le texte
        text = pytesseract.image_to_string(rogne, config='--psm 6')

        # Convertir le texte en un entier et le retourner
        if not text:
            return 0
        return string_to_int(text)




    def get_dice(self, img_np):
        # Déterminer la largeur et la hauteur de la capture d'écran
        screen_width = img_np.shape[1]
        screen_height = img_np.shape[0]

        # Position en bas de l'écran, les valeurs doivent être ajustées pour cibler la zone exacte
        # où se trouve le nombre de dés
        width = 200  # Largeur de la zone à capturer (à ajuster selon la taille de l'affichage des dés)
        height = 100  # Hauteur de la zone à capturer (à ajuster selon la taille de l'affichage des dés)

        # Pour positionner le rectangle de rognage en bas de l'écran, on ajuste posX et posY
        posX = (screen_width // 2) - (width // 2)  # Centre X de l'écran moins la moitié de la largeur de rognage
        posY = screen_height - height - 10  # Bas de l'écran moins la hauteur de rognage et une marge

        # Rogner l'image à la zone spécifiée pour obtenir uniquement le nombre de dés
        rogne = img_np[posY:posY+height, posX:posX+width]

        # Utiliser pytesseract pour reconnaître le texte
        text = pytesseract.image_to_string(rogne, config='--psm 6')

        #split text to get only the number before the /
        text = text.split('/')
        text = text[0]

        if not text:
            return None
        return string_to_int(text)

    def assaut(self):
        locations = list(pyautogui.locateAllOnScreen('cache/assaut2.png', grayscale=True, confidence=0.5))
        if locations:
            # click on the center of a random assaut detected
            location = random.choice(locations)
            pyautogui.click(pyautogui.center(location))
            
        else:
            print("Assaut image not found on screen.")

    def braq(self, images):
        #shuffle images list order
        random.shuffle(images)
        #max 15 clicks
        for image in images[:15]:
            # click on the center of a random braq detected
            pyautogui.click(pyautogui.center(image))
            time.sleep(0.1)




    def skip(self, location):
        # click on the center of location relative to self
        center_x = self.window.left + location.left + location.width / 2
        center_y = self.window.top + location.top + location.height / 4
        pyautogui.click(center_x, center_y)

    def skip_card_button(self):
        absolute_x = self.window.centerx
        absolute_y = self.window.centery + self.window.height / 3
        pyautogui.click(absolute_x, absolute_y)

    def roll_dice(self):
        location = pyautogui.locateOnScreen('cache/go_button.png', confidence=0.8)
        if location:
            pyautogui.click(pyautogui.center(location))
        else:
            print("Dice image not found on screen.")

    def auto_roll(self, location):
        if location:
            print("Dice Autorolled.")
            pyautogui.moveTo(pyautogui.center(location))
            # stay click for 1.2 seconds
            pyautogui.mouseDown()
            time.sleep(1.2)
            pyautogui.mouseUp()
        else:
            self.roll_dice()

    
    

 

    def scale_image(self, image, scale):
        image = cv2.imread(image)
        width = int(image.shape[1] * scale)
        height = int(image.shape[0] * scale)
        dim = (width, height)
        return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    def locate(self, image):
        for scale in np.arange(0.5, 1.3, 0.1):  # scale from 50% to 130% with a step of 10%
            scaled_image = self.scale_image(image, scale)
            temp_file = f"cache/temp.png"
            cv2.imwrite(temp_file, scaled_image)
            location = pyautogui.locateOnScreen(image=temp_file, grayscale=True, confidence=0.8, minSearchTime=0.05)
            try:
                os.remove(temp_file)  # remove the temporary file
            except PermissionError:
                time.sleep(1)
                os.remove(temp_file)  # remove the temporary file
                pass
            if location is not None:
                return location
        return None
    
    #locate all images on screen and return a list of locations
    def locateAll(self, image):
        locations = list(pyautogui.locateAllOnScreen(image, grayscale=True, confidence=0.8))
        if locations:
            return locations
        else:
            return None




#START OF THE PROGRAM

# Get all window titles
all_windows = gw.getAllTitles()

# Print all window titles
for i, title in enumerate(all_windows):
    print(f"{i}: {title}")

# Ask the user to choose a window
chosen_index = int(input("Enter the number of the window you want to use: "))

# Get the chosen window
game_windows = gw.getWindowsWithTitle(all_windows[chosen_index])[0]

if game_windows:
    game = GameManipulator(game_windows)

    print("Fenêtre game trouvée")

    lastevent = None

    while True:

        if keyboard.is_pressed('F'):
            print("F détecté, on quitte le programme")
            break
        
        # Afficher les informations du jeu
        if lastevent is not None:
            print(lastevent)
        print_game_info(game)

        go_location = game.locate("cache/go_button.png")

        if go_location is not None: 
            lastevent = "GO détecté"
            game.auto_roll(go_location)
            continue

        # Detection de recuperer
        image_location = game.locate("cache/detect_recup.PNG")
        if image_location is not None:
            lastevent ="Recuperer détecté"
            game.skip(image_location)
            continue
            
        # Détection des braquages
        image_locations = game.locateAll("cache/detect_braq.PNG")
        if image_locations is not None:
            lastevent ="Braquage détecté"
            game.braq(image_locations)
            continue

        # Détection des assauts
        image_location = game.locate("cache/detect_assaut2.PNG")
        if image_location is not None:
            lastevent ="Assaut détecté2"
            game.assaut()
            continue

        else:
            plastevent ="Rien de détecté"
            time.sleep(0.2)
            continue
else:
    print("Pas de fenêtre trouvée")
