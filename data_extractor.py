import string

import pyautogui
from pytesseract import pytesseract
import time


time.sleep(5)

title_bounding_box_raw = (539, 200, 1517, 326)
servings_bounding_box_raw = (530, 337, 1523, 420)
ingredient_bounding_box_raw = (527, 425, 852, 940)
recipe_bounding_box_raw = (862, 421, 1549, 955)

title_bounding_box = (title_bounding_box_raw[0], title_bounding_box_raw[1], title_bounding_box_raw[2] - title_bounding_box_raw[0], title_bounding_box_raw[3] - title_bounding_box_raw[1])
servings_bounding_box = (servings_bounding_box_raw[0], servings_bounding_box_raw[1], servings_bounding_box_raw[2] - servings_bounding_box_raw[0], servings_bounding_box_raw[3] - servings_bounding_box_raw[1])
ingredient_bounding_box = (ingredient_bounding_box_raw[0], ingredient_bounding_box_raw[1], ingredient_bounding_box_raw[2] - ingredient_bounding_box_raw[0], ingredient_bounding_box_raw[3] - ingredient_bounding_box_raw[1])
recipe_bounding_box = (recipe_bounding_box_raw[0], recipe_bounding_box_raw[1], recipe_bounding_box_raw[2] - recipe_bounding_box_raw[0], recipe_bounding_box_raw[3] - recipe_bounding_box_raw[1])


def extract_servings(text):
    text = text.lower()

    if "serv" not in text:
        return 0

    read = ""

    for i, char in enumerate(list(text)):
        read += char

        if read.endswith("serves "):
            serving_index = i
            break

    else:
        print("[Servings] Couldn't find servings in text after passing \"serv\" test")
        return 0

    min_servings = text[serving_index+1]

    if len(text) > serving_index+3 and text[serving_index+3] == "-":
        try:
            max_servings = text[serving_index+5]
            return round((int(min_servings) + int(max_servings)) / 2)
        except:
            return min_servings

    return min_servings


def clean_title(text):
    text = text.replace("\n", " ")

    for i in range(2):
        if text[0] == " ":
            text = text[1:]

        if text[-1] == " ":
            text = text[:-1]

        if text[0] == "|":
            text = text[1:]

        if text[-1] == "|":
            text = text[:-1]

        if text[0] in string.ascii_lowercase or text[0] == "é":
            text = text[1:]

        if text[0] == " ":
            text = text[1:]

        if text[-1] == " ":
            text = text[:-1]

    return text


def capture_recipie():
    title_screenshot = pyautogui.screenshot(region=title_bounding_box)
    title = pytesseract.image_to_string(title_screenshot)

    servings_screenshot = pyautogui.screenshot(region=servings_bounding_box)
    servings_text = pytesseract.image_to_string(servings_screenshot)

    ingredient_screenshot = pyautogui.screenshot(region=ingredient_bounding_box)
    ingredient_text = pytesseract.image_to_string(ingredient_screenshot)

    recipe_screenshot = pyautogui.screenshot(region=recipe_bounding_box)
    recipe = pytesseract.image_to_string(recipe_screenshot)

    return {
        "title": clean_title(title),
        "servings": extract_servings(servings_text),
        "ingredients_text_raw": ingredient_text,
        "recipe_text": recipe
    }


def capture_all_recipes(areas):
    current_page = 1
    recipes = []

    for area in areas:
        if type(area) is int:
            target_page = area
            go_for_x_pages = 0
        else:
            target_page = area[0]
            go_for_x_pages = area[1] - area[0]

        for i in range(target_page - current_page):
            pyautogui.press('down')
            current_page += 1
            time.sleep(0.1)

        for offset in range(go_for_x_pages + 1):
            recipes.append(
                capture_recipie()
            )

            pyautogui.press('down')
            current_page += 1

    return recipes


if __name__ == "__main__":
    import json
    recipie_areas = [(13, 14), (16, 19), (21, 24), 26, (28, 29), (31, 34), (36, 38), (40, 41), (43, 45), (47, 49), (51, 53), (55, 57), (59, 61), (63, 65), (67, 69), (71, 74), (76, 78), (80, 83), (85, 88), (90, 94), (96, 98), (100, 102), (104, 107), (109, 113), (116, 120), (122, 125), (127, 131), (133, 135), (137, 141), (143, 147), (149, 153), (158, 161), (163, 166), (168, 173), (176, 179)]  # not complete

    recipies = capture_all_recipes(recipie_areas)
    
    json.dump(recipies, fp=open("data/dump.json", "w"))


    # todo - Make chatgpt clean up the ingredients list

