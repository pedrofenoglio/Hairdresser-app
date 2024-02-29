import mysql.connector
import babel.numbers
from product import Product

class CSVManager:
    @staticmethod
    def write_to_db(data, table_name):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="R0mafenoglio",
            database="lake"
        )
        cursor = connection.cursor()

        query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s']*len(data))})"
        cursor.execute(query, data)

        connection.commit()
        connection.close()

    @staticmethod
    def read_from_db(table_name):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="R0mafenoglio",
            database="lake"
        )
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()

        connection.close()

        return data

    @staticmethod
    def write_products_to_db(products):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="R0mafenoglio",
            database="lake"
        )
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS Products (ProductName VARCHAR(255), Quantity INT, UnitPrice FLOAT)")

        for product in products:
            data = (product.product_name, product.quantity, product.unit_price)
            query = "INSERT INTO Products (ProductName, Quantity, UnitPrice) VALUES (%s, %s, %s)"
            cursor.execute(query, data)

        connection.commit()
        connection.close()

    @staticmethod
    def read_products_from_db():
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="R0mafenoglio",
            database="lake"
        )
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Products")
        data = cursor.fetchall()

        connection.close()

        return [Product(row[0], int(row[1]), float(row[2])) for row in data]


