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

    def braq(self):
        screenshot = self.screenshot()
        locations = list()
        for scale in np.arange(0.5, 1.5, 0.05):  # scale from 80% to 120%
            randint = random.randint(0, 200)
            scaled_image = game.scale_image("cache/detect_braq.png", scale)
            cv2.imwrite(f"cache/temp_braq{randint}.png", scaled_image)
            location = pyautogui.locate(f"cache/temp_braq{randint}.png", screenshot, grayscale=True, confidence=0.7)
            if location is not None:
                locations.append(location)

        if locations:
            for location in locations:
                center_x = self.window.left + location.left + location.width / 2
                center_y = self.window.top + location.top + location.height / 2
                pyautogui.click(center_x, center_y)
                time.sleep(0.25)
        else:
            print("Braq image not found on screen.")


    def skip(self, location):
        # click on the center of location relative to self
        center_x = self.window.left + location.left - location.width / 2
        center_y = self.window.top + location.top - location.height / 4
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
            location = pyautogui.locateOnScreen(temp_file,minSearchTime=0.2, grayscale=True, confidence=0.73)
            os.remove(temp_file)  # remove the temporary file
            if location is not None:
                return location
        return None


def string_to_int(string):
    num = re.findall(r'[0-9]+', string)
    if not num:
        return None
    return int(''.join(num))






# Get all window titles
all_windows = gw.getAllTitles()

# Print all window titles
for i, title in enumerate(all_windows):
    print(f"{i}: {title}")

# Ask the user to choose a window
chosen_index = int(input("Enter the number of the window you want to use: "))

# Get the chosen window
bluestacks_windows = gw.getWindowsWithTitle(all_windows[chosen_index])[0]

if bluestacks_windows:
    game = GameManipulator(bluestacks_windows)

    print("Fenêtre BlueStacks trouvée")

    while True:

        if keyboard.is_pressed('F'):
            print("F détecté, on quitte le programme")
            break

        # Afficher les informations du jeu
        print_game_info(game)

        go_location = game.locate("cache/go_button2.png")

        if go_location is not None: 
            print("GO détecté")
            game.skip(go_location)
            continue

        
        # Detection de recuperer
        image_location = game.locate("cache/detect_recup.PNG")
        if image_location is not None:
            print("Recuperer détecté")
            game.skip(image_location)
            continue

        image_location2 = game.locate("cache/detect_recup2.PNG")
        if image_location2 is not None:
            print("Recuperer2 détecté")
            game.skip(image_location2)
            continue
            
        # Détection des braquages
        image_location = game.locate("cache/detect_braq.png")
        if image_location is not None:
            print("Braquage détecté")
            game.braq()
            continue
        # Détection des assauts
        image_location = game.locate("cache/detect_assaut.PNG")
        if image_location is not None:
            print("Assaut détecté")
            game.assaut()
            continue

        else:
            print("Rien de détecté, on clique sur le plateau")
            game.skip_card_button()
            time.sleep(0.1)
            continue


else:
    print("Pas de fenêtre BlueStacks trouvée")
