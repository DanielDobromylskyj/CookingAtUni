import threading
import random
import time


class Loader:
    def __init__(self):
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


    def load_recipies(self):
        self.loading = "Loading Recipies..."

    def set_silly_quote_time(self):
        self.loading = random.choice(self.silly_quotes)
        self.max_loading = 0
        self.current_loading = 0

        time.sleep(1)

    def __load(self):
        self.wait()
        self.load_recipies()
        self.wait()
        self.set_silly_quote_time()
        self.wait()

        self.has_loaded = True


    def load(self):
        threading.Thread(target=self.__load).start()
