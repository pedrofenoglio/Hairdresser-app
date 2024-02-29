class Product:
    def __init__(self, product_name, quantity, unit_price):
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price

    def to_csv_row(self):
        return [self.product_name, str(self.quantity), str(self.unit_price)]
