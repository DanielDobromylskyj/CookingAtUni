import threading
import random
import time
import os
import recipes
import stock
import requests
import traceback

from kivy.app import App


class Loader:
    def __init__(self, paths: dict):
        self.paths = paths
        self.path = ""

        self.silly_quotes = [
            "Walking The Fish...",
            "Finding Fire Extinguisher...",
            "Warning Fire Department...",
            "Do You Read These?",
            "Kneading time to load...",
            "Syncing spices...",
            "Rendering ramen...",
            "Doing Nothing...",
            "Counting invisible calories...",
            "Negotiating peace with the oven...",
            "Waiting for the timer to beep...",
            "Checking if microwaves dream...",
            "Testing if the spoon is level...",
        ]

        self.waiting = False
        self.has_loaded = False

        self.loading = "Finding Files..."
        self.current_loading = 0
        self.max_loading = 0

        self.recipies = []

    def set_local_path(self, app):
        self.path = app.user_data_dir

    def get_loaded_data(self):
        return self.recipies

    def update_text(self):
        if self.max_loading > 0:
            text = f"{self.loading} ({self.current_loading}/{self.max_loading})"
        else:
            text = f"{self.loading}"

        self.waiting = False
        return text


    def wait(self):
        self.waiting = True

        while self.waiting:
            time.sleep(0.2)

    @staticmethod
    def get_file(url, local_name):
        response = requests.get(url)
        response.raise_for_status()  # will raise error if download failed

        with open(local_name, 'wb') as f:
            f.write(response.content)


    def path_check(self):
        if not os.path.exists(os.path.join(self.path, self.paths["recipes"])):
            self.loading = "Downloading recipies..."

            self.get_file(
                "https://raw.githubusercontent.com/DanielDobromylskyj/CookingAtUni/refs/heads/master/recipes.json",
                os.path.join(self.path, self.paths["recipes"])
            )


    def load_recipies(self):
        self.loading = "Loading Recipies..."
        self.current_loading = 0
        self.max_loading = 0

        recipes_manager = recipes.Recipes(os.path.join(self.path, self.paths["recipes"]), os.path.join(self.path, self.paths["stock"]))

        self.max_loading = len(recipes_manager.recipes)

        needed_attrs = [("Servings", int), ("TimeToCookInMins", int), ("Ingredients", list), ("Description", str), ("HowToMake", str), ("isGlutenFree", bool)]
        for name in recipes_manager.recipes:
            recipe = recipes_manager.recipes[name]
            for attr in needed_attrs:
                if attr[0] in recipe and type(recipe[attr[0]]) is attr[1]:
                    pass  # good value
                else:
                    print(f"[WARNING] Validation Failed On Recipe '{name}'")

            self.current_loading += 1




    def set_silly_quote_time(self):
        self.loading = random.choice(self.silly_quotes)
        self.max_loading = 0
        self.current_loading = 0

        time.sleep(1)

    def __load(self):
        try:
            self.wait()
            self.path_check()
            self.wait()
            self.load_recipies()
            self.wait()
            self.set_silly_quote_time()
            self.wait()
            self.has_loaded = True
        except Exception as e:
            self.loading = f"Failed to load\n{traceback.format_exc()}"
            self.max_loading = 0
            self.current_loading = 0

            raise


    def load(self):
        threading.Thread(target=self.__load).start()
