import mysql.connector
import datetime
import babel.numbers


class Service:
    def __init__(self, service_name, total_price, date, quantity, employee, payment_method):
        self.service_name = service_name
        self.total_price = total_price
        # Assuming date is already a datetime.date object
        self.date = date
        self.quantity = quantity
        self.employee = employee
        self.payment_method = payment_method

    @staticmethod
    def filter_by_date_range_and_employee(services, start_date, end_date, performer):
        return [service for service in services if start_date <= service.date <= end_date and service.performer == performer]

    @staticmethod
    def filter_by_date_range(services, start_date, end_date):
        return [service for service in services if start_date <= service.date <= end_date]



    @staticmethod
    def filter_by_date(services, target_date):
        target_date = datetime.datetime.strptime(target_date, '%Y-%m-%d').date()
        return [service for service in services if service.date == target_date]



    @staticmethod
    def calculate_total(services):
        return sum(service.total_price for service in services)

    @staticmethod
    def calculate_daily_expenses(services, day):
        cash_expenses = 0
        transfer_expenses = 0
        total_cash_amount = 0
        total_transfer_amount = 0

        for service in services:
            if service.date == day:
                if service.is_expense():
                    if service.payment_method == "Efectivo":
                        cash_expenses += 1
                        total_cash_amount += service.total_price
                    elif service.payment_method == "Transferencia":
                        transfer_expenses += 1
                        total_transfer_amount += service.total_price

        return cash_expenses, transfer_expenses, total_cash_amount, total_transfer_amount

    def is_expense(self):
        return self.total_price < 0

    @classmethod
    def write_to_db(cls, data):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="R0mafenoglio",
            database="lake"
        )
        cursor = connection.cursor()

        query = "INSERT INTO Services (ServiceType, Performer, Quantity, TotalPrice, Date, PaymentMethod) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, data)

        connection.commit()
        connection.close()

    @classmethod
    def read_from_db(cls):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="R0mafenoglio",
            database="lake"
        )
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Services")
        services_data = cursor.fetchall()

        connection.close()

        return services_data

    def calculate_total_income(services):
        return sum(service.total_price for service in services)

    def __str__(self):
        return f"Service(name={self.service_name}, performer={self.performer}, quantity={self.quantity}, " \
        f"total_price={self.total_price}, date={self.date}, payment_method={self.payment_method})"