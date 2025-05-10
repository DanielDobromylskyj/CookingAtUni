import json

import stock


class Recipes:
    def __init__(self, recipes_path, stock_path):
        self.path = recipes_path

        self.recipes = json.load(open(recipes_path))
        self.stock = stock.StockManager(stock_path)


