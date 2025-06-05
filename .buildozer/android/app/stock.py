import sqlite3
import os


def create_db(path):
    with DB_Wrapper(path) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                stock REAL DEFAULT 0.0,
                quantity_per_stock INTEGER DEFAULT 0,
                quantity_units TEXT DEFAULT 'g',
                price REAL DEFAULT 0.0
            );
        """)

        db.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS ingredients_fts USING fts5(
                name,
                content='ingredients',
                content_rowid='id'
            );
        """)

        # Used to keep both the main table and search table in sync!
        db.execute("""
            -- After INSERT
            CREATE TRIGGER IF NOT EXISTS ingredients_ai AFTER INSERT ON ingredients BEGIN
              INSERT INTO ingredients_fts(rowid, name) VALUES (new.id, new.name);
            END;""")

        db.execute("""
            -- After UPDATE
            CREATE TRIGGER IF NOT EXISTS ingredients_au AFTER UPDATE ON ingredients BEGIN
              UPDATE ingredients_fts SET name = new.name WHERE rowid = new.id;
            END;""")

        db.execute("""
            -- After DELETE
            CREATE TRIGGER IF NOT EXISTS ingredients_ad AFTER DELETE ON ingredients BEGIN
              DELETE FROM ingredients_fts WHERE rowid = old.id;
            END;""")

        db.commit()


class DB_Wrapper:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def execute(self, query: str, params: None | tuple | list = None):
        if params is None:
            params = ()

        self.cursor.execute(query, params)

    def commit(self):
        self.conn.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()


class StockManager:
    def __init__(self, path):
        self.path = path

        if not os.path.exists(self.path):
            create_db(self.path)


    def get_db(self):
        return DB_Wrapper(self.path)


    def search_ingredient(self, name):
        with self.get_db() as db:
            db.execute("""
                SELECT ingredients.*, bm25(ingredients_fts) AS rank
                FROM ingredients_fts
                JOIN ingredients ON ingredients_fts.rowid = ingredients.id
                WHERE ingredients_fts MATCH ?
                ORDER BY rank
                LIMIT 5;
                """, (f'{name}*',))

            return [result[:-1] for result in db.fetchall()]

    def get_ingredient(self, name):
        with self.get_db() as db:
            db.execute("SELECT * FROM ingredients WHERE name = ? LIMIT 1", (name,))
            return db.fetchone()

    def add_ingredient(self, name, price, stock=0, amount_per_stock=1, measurement="g"):
        with self.get_db() as db:
            db.execute("""
                INSERT INTO ingredients (name, price, stock, quantity_per_stock, quantity_units)
                VALUES (?, ?, ?, ?, ?)
            """, (name, price, stock, amount_per_stock, measurement))

            db.commit()

    def update_ingredient(self, name: str, price: None | float = None, stock: None | int = None, current_stock_quantity: None | int = 1):
        fields = []
        values = []

        if price is not None:
            fields.append("price = ?")
            values.append(price)

        if stock is not None:
            fields.append("stock = ?")
            values.append(stock)

        if current_stock_quantity is not None:
            fields.append("quantity_per_stock = ?")
            values.append(current_stock_quantity)

        if not fields:
            return

        values.append(name)  # For the WHERE clause

        query = f"""
                UPDATE ingredients
                SET {', '.join(fields)}
                WHERE name = ?
            """

        with self.get_db() as db:
            db.execute(query, values)
            db.commit()

    def change_stock(self, name, stock):  # Can be +ve or -ve
        with self.get_db() as db:
            db.execute("""
                UPDATE ingredients
                SET stock = stock + ?
                WHERE name = ?
            """, (stock, name))

            db.commit()

if __name__ == "__main__":
    mgr = StockManager("ingredients.db")
    #print(mgr.search_ingredient("Egg"))

