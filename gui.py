# gui.py
import mysql.connector
from tkinter import Label, Button, StringVar, OptionMenu, Spinbox, ttk, simpledialog, Tk, Text, END, Toplevel, messagebox, Entry
from service import Service
from product import Product
from tkcalendar import Calendar, DateEntry
import os
from day_manager import DayManager
from decimal import Decimal
import babel.numbers

class DateRangeDialog:


    def __init__(self, master):
        self.master = master
        self.top = Toplevel(master)
        self.top.title("Seleccionar Rango de Fechas")

        # Create DateEntry widgets for start and end dates
        Label(self.top, text="Fecha de Inicio:").pack()
        self.start_date = DateEntry(self.top, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.start_date.pack(padx=10, pady=5)

        Label(self.top, text="Fecha de Fin:").pack()
        self.end_date = DateEntry(self.top, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.end_date.pack(padx=10, pady=5)

        Button(self.top, text="Seleccionar Fechas", command=self.ok).pack(pady=10)

        self.selected_dates = None

    def ok(self):
        start_date = self.start_date.get_date().strftime('%Y-%m-%d')
        end_date = self.end_date.get_date().strftime('%Y-%m-%d')
        self.selected_dates = (start_date, end_date)
        self.top.destroy()

class Product:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price


class App:


    def select_date(self):
        date_range_dialog = DateRangeDialog(self.master)
        self.master.wait_window(date_range_dialog.top)
        if date_range_dialog.selected_dates:
            self.selected_date = date_range_dialog.selected_dates[0]


    def __init__(self, master):
        self.master = master
        master.title("Lake Software")

            # Create a connection to the MySQL database
        try:
            # Database connection
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="R0mafenoglio",
                database="lake"
            )
        except Exception as e:
            print(f"Database connection error: {e}")

            # Create a cursor for executing queries
        self.db_cursor = self.db_connection.cursor()




        # Variables para los campos de entrada
        self.service_var = StringVar()
        self.performer_var = StringVar()
        self.quantity_var = StringVar()
        self.price_var = StringVar()
        self.date_var = DayManager.get_current_day()
        self.payment_method_var = StringVar()

        # Opciones para los servicios, los realizadores y los métodos de pago
        service_options = ["Corte", "Corte y barba", "Barba", "Gasto"]
        performer_options = ["Emi", "Lucho", "Rodri"]
        payment_options = ["Efectivo", "Transferencia"]

        # En el método __init__ de la clase App, después de crear el Combobox para los servicios:
        self.service_combobox = ttk.Combobox(master, textvariable=self.service_var, values=service_options)
        self.service_combobox.grid(row=0, column=1)

        # Después de esto, agrega el nuevo servicio "Gasto" al Combobox:
        new_service = "Gasto"
        current_values = self.service_combobox['values']

        # Verificar si el nuevo servicio ya está en la lista
        if new_service not in current_values:
            # Agregar el nuevo servicio a la lista de valores
            updated_values = current_values + (new_service,)
            self.service_combobox['values'] = updated_values

        # Refrescar la interfaz de usuario para aplicar los cambios
        master.update_idletasks()

        # Etiquetas y campos de entrada
        Label(master, text="Servicio").grid(row=0, column=0)
        ttk.Combobox(master, textvariable=self.performer_var, values=performer_options).grid(row=1, column=1)
        
        Label(master, text="Realizado por:").grid(row=1, column=0)
        ttk.Combobox(master, textvariable=self.performer_var, values=performer_options).grid(row=1, column=1)

        Label(master, text="Cantidad:").grid(row=2, column=0)
        Spinbox(master, from_=1, to=10, textvariable=self.quantity_var).grid(row=2, column=1)

        Label(master, text="Precio:").grid(row=3, column=0)
        Spinbox(master, from_=0, to=1000, increment=0.01, textvariable=self.price_var).grid(row=3, column=1)

        Label(master, text="Fecha:").grid(row=4, column=0)
        Label(master, text=self.date_var).grid(row=4, column=1)

        Label(master, text="Método de Pago:").grid(row=5, column=0)
        ttk.Combobox(master, textvariable=self.payment_method_var, values=payment_options).grid(row=5, column=1)

        # Botones para agregar el servicio y guardar en CSV
        Button(master, text="Agregar Servicio", command=self.add_service).grid(row=6, column=0, columnspan=2)

        # Botones para estadísticas
        Button(master, text="Ver servicios por empleado", command=self.show_employee_services).grid(row=8, column=0, columnspan=2)
        Button(master, text="Calcular ingresos por empleado", command=self.calculate_income).grid(row=9, column=0, columnspan=2)
        Button(master, text="Arqueo de caja", command=self.show_cash_report).grid(row=11, column=0, columnspan=2)

        # Botón para ver gastos
        Button(master, text="Ver Gastos", command=self.show_expenses).grid(row=10, column=0, columnspan=2)

        # Calendario
        Button(master, text="Seleccionar Fecha", command=self.select_date).grid(row=4, column=2, columnspan=2)
        self.selected_date = None

        # Cuadro de texto para visualizar el CSV
        self.csv_text = Text(master, height=10, width=40)
        self.csv_text.grid(row=0, column=4, rowspan=10)

        # Actualizar el cuadro de texto con el contenido actual del CSV
        self.update_csv_text()

        # Nueva sección para gestión de inventario
        Label(master, text="--- Inventario ---").grid(row=12, column=0, columnspan=2)

        Label(master, text="Producto:").grid(row=13, column=0)
        self.product_name_var = StringVar()
        Entry(master, textvariable=self.product_name_var).grid(row=13, column=1)

        Label(master, text="Cantidad:").grid(row=14, column=0)
        self.product_quantity_var = StringVar()
        Spinbox(master, from_=1, to=100, textvariable=self.product_quantity_var).grid(row=14, column=1)

        Label(master, text="Precio Unitario:").grid(row=15, column=0)
        self.product_price_var = StringVar()
        Spinbox(master, from_=0, to=1000, increment=0.01, textvariable=self.product_price_var).grid(row=15, column=1)

        Button(master, text="Agregar Producto", command=self.add_product).grid(row=16, column=0, columnspan=2)
        Button(master, text="Ver Inventario", command=self.show_inventory).grid(row=17, column=0, columnspan=2)
        Button(master, text="Eliminar productos", command=self.remove_product).grid(row=18, column=0, columnspan=2)

        self.update_inventory_text()






    def add_product(self):
        product_name = self.product_name_var.get()
        product_quantity = int(self.product_quantity_var.get())
        product_price = float(self.product_price_var.get())

        # Create a Product object
        product = Product(product_name, product_quantity, product_price)

        # Save to the MySQL database
        query = "INSERT INTO inventory (Name, Amount, Price) VALUES (%s, %s, %s)"
        data = (product_name, product_quantity, product_price)
        self.db_cursor.execute(query, data)
        self.db_connection.commit()

        # Update the text box with the current inventory content
        self.update_inventory_text()

    def remove_product(self):
        product_name = simpledialog.askstring("Eliminar Producto", "Ingrese el nombre del producto a eliminar:")

        if product_name:
            product_quantity_to_remove_str = simpledialog.askstring("Eliminar Producto", f"Ingrese la cantidad a eliminar del producto {product_name}:")

            if product_quantity_to_remove_str:
                try:
                    product_quantity_to_remove = int(product_quantity_to_remove_str)
                except ValueError:
                    messagebox.showerror("Error", "La cantidad ingresada no es un número entero válido.")
                    return

                # Read current inventory data from the database
                self.db_cursor.execute("SELECT * FROM Inventory")
                inventory_data = self.db_cursor.fetchall()

                # Convert data to Product objects
                inventory_objects = [Product(row[1], row[2], row[3]) for row in inventory_data]

                product_found = False

                for i, product in enumerate(inventory_objects):
                    if product.name == product_name:
                        product_found = True

                        if product.quantity >= product_quantity_to_remove:
                            product.quantity -= product_quantity_to_remove

                            # Update the MySQL database with the updated inventory
                            self.db_cursor.execute("DELETE FROM Inventory")
                            query = "INSERT INTO Inventory (Name, Amount, Price) VALUES (%s, %s, %s)"
                            data = [(p.name, p.quantity, p.price) for p in inventory_objects]
                            self.db_cursor.executemany(query, data)
                            self.db_connection.commit()

                            messagebox.showinfo("Producto Eliminado", f"Se eliminaron {product_quantity_to_remove} unidades de {product.name}.")
                        else:
                            messagebox.showwarning("Error", f"No hay suficientes unidades de {product.name} en inventario.")
                        break

                if not product_found:
                    messagebox.showwarning("Error", f"No se encontró el producto {product_name} en inventario.")

                self.update_inventory_text()






    def show_inventory(self):
        self.db_cursor.execute("SELECT * FROM Inventory")
        inventory_data = self.db_cursor.fetchall()

        inventory_objects = [Product(row[1], row[2], row[3]) for row in inventory_data]

        if inventory_objects:
            message = "Inventario:\n\n"
            for product in inventory_objects:
                message += f"{product.name}: {product.quantity} unidades, Precio Unitario: ${product.price:.2f}\n"
        else:
            message = "El inventario está vacío."

        messagebox.showinfo("Inventario", message)


    def update_inventory_text(self):
        self.db_cursor.execute("SELECT * FROM Inventory")
        inventory_data = self.db_cursor.fetchall()
        csv_content = "\n".join([",".join((str(row[1]), str(row[2]), str(row[3]))) for row in inventory_data])
        self.csv_text.delete(1.0, END)
        self.csv_text.insert(END, csv_content)



    def add_service(self):
        service_name = self.service_var.get()
        performer = self.performer_var.get()
        quantity = int(self.quantity_var.get())
        price = float(self.price_var.get())
        date = self.date_var if not self.selected_date else self.selected_date
        payment_method = self.payment_method_var.get()

        # The correct total_price is just the price, not the product of quantity and price
        total_price = price

        # Create a Service object
        service = Service(service_name, performer, quantity, total_price, date, payment_method)

        # Save to the MySQL database
        query = "INSERT INTO Services (ServiceType, Price, Date, Amount, Performer, PaymentMethod) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (service_name, total_price, date, quantity, performer, payment_method)
        self.db_cursor.execute(query, data)
        self.db_connection.commit()

        self.update_csv_text()


    def show_employee_services(self):
        # Mostrar cuántos servicios realizó un empleado en un rango de tiempo
        performer = simpledialog.askstring("Input", "Ingrese el nombre del empleado:")

        if performer:
            date_range_dialog = DateRangeDialog(self.master)
            self.master.wait_window(date_range_dialog.top)

            if date_range_dialog.selected_dates:
                start_date, end_date = date_range_dialog.selected_dates

                # Fetch services for the specified performer and date range from the database
                query = "SELECT * FROM Services WHERE Performer = %s AND Date BETWEEN %s AND %s"
                self.db_cursor.execute(query, (performer, start_date, end_date))
                services_data = self.db_cursor.fetchall()

                # Convert data to Service objects
                services_objects = [Service(row[1], row[5], row[4], row[2], row[3], row[6]) for row in services_data]

                total_services = sum(service.quantity for service in services_objects)

                # Mostrar un popup con el total de servicios
                messagebox.showinfo("Total de Servicios", f"{performer} realizó {total_services} servicios en el rango de fechas seleccionado.")
            else:
                messagebox.showwarning("Error", "Se requiere seleccionar un rango de fechas.")
        else:
            messagebox.showwarning("Error", "Se requiere ingresar el nombre del empleado.")


    
    def calculate_income(self):
        # Calcular ingresos por empleado
        performer = simpledialog.askstring("Input", "Ingrese el nombre del empleado:")
        if performer:
            date_range_dialog = DateRangeDialog(self.master)
            self.master.wait_window(date_range_dialog.top)

            print(f"Selected dates: {date_range_dialog.selected_dates}")

            if date_range_dialog.selected_dates:
                start_date, end_date = date_range_dialog.selected_dates

                # Fetch services for the specified performer and date range from the database
                query = "SELECT * FROM Services WHERE Performer = %s AND Date BETWEEN %s AND %s"
                self.db_cursor.execute(query, (performer, start_date, end_date))
                services_data = self.db_cursor.fetchall()

                # Convert data to Service objects
                services_objects = [Service(row[1], row[5], row[4], row[2], row[3], row[6]) for row in services_data]

                # Add this line to print the list
                for service in services_objects:
                    print(service)

                # Calcular e imprimir el total de ingresos multiplicando cantidad por precio
                total_income = sum(service.quantity * service.total_price for service in services_objects)
                sueldo_quincenal = total_income * Decimal('0.4')
                sueldo = f"{performer} generó ${total_income} en el rango de fechas seleccionado. Sueldo quincenal para {performer}: ${sueldo_quincenal}"
                messagebox.showinfo("Ingreso y sueldo", sueldo)

            else:
                print("Se requiere seleccionar un rango de fechas.")
        else:
            print("Se requiere ingresar el nombre del empleado.")




    def show_cash_report(self):
        # Use the current date
        today = DayManager.get_current_day()

        # Print today's date for debugging
        print(f"Today's date: {today}")

        # Fetch services for the current date from the database
        query = "SELECT * FROM Services WHERE Date = %s"
        self.db_cursor.execute(query, (today,))
        services_data = self.db_cursor.fetchall()

        # Print services data for today for debugging
        print(f"Services data for today: {services_data}")

        # Convert data to Service objects
        services_objects = [Service(row[1], row[2], row[3], row[4], row[5], row[6]) for row in services_data]

        # Filter services for the current date
        filtered_services = Service.filter_by_date(services_objects, today)

        # Check if filtered_services is not empty before further processing
        if not filtered_services:
            print("No services found for today.")
            return

        # Debugging: print filtered services
        print("Filtered Services:")
        for service in filtered_services:
            print(service.service_name, service.total_price, service.payment_method)

                    # Calculate total earnings for cash and transfer payments for all service types
            total_corte_cash = sum(service.total_price * service.quantity for service in filtered_services if
                                service.payment_method == "Efectivo" and service.service_name == "Corte")
            total_corte_cash += sum(service.total_price * service.quantity for service in filtered_services if
                                    service.payment_method == "Efectivo" and service.service_name == "Corte y barba")
            total_corte_cash += sum(service.total_price * service.quantity for service in filtered_services if
                                    service.payment_method == "Efectivo" and service.service_name == "Barba")
            total_expenses_cash = sum(service.total_price * service.quantity for service in filtered_services if
                                    service.payment_method == "Efectivo" and service.service_name == "Gasto")

            total_corte_transfer = sum(service.total_price * service.quantity for service in filtered_services if
                                    service.payment_method == "Transferencia" and service.service_name == "Corte")
            total_corte_transfer += sum(service.total_price * service.quantity for service in filtered_services if
                                        service.payment_method == "Transferencia" and service.service_name == "Corte y barba")
            total_corte_transfer += sum(service.total_price * service.quantity for service in filtered_services if
                                        service.payment_method == "Transferencia" and service.service_name == "Barba")
            total_expenses_transfer = sum(service.total_price * service.quantity for service in filtered_services if
                                        service.payment_method == "Transferencia" and service.service_name == "Gasto")


        # Debugging: print totals
        print("\nTotals:")
        print(f"Total Corte Cash: {total_corte_cash}")
        print(f"Total Corte Transfer: {total_corte_transfer}")
        print(f"Total Expenses Cash: {total_expenses_cash}")
        print(f"Total Expenses Transfer: {total_expenses_transfer}")

        # Calculate net cash and transfer amounts for all service types
        net_cash = total_corte_cash - total_expenses_cash
        net_transfer = total_corte_transfer - total_expenses_transfer

        # Display the results in a message box
        message = f"Arqueo de caja para el día {today}:\n\n"
        message += f"En efectivo: ${net_cash}\n"
        message += f"En transferencia: ${net_transfer}"

        messagebox.showinfo("Arqueo de Caja", message)







    def show_expenses(self):
        # Mostrar cuántos gastos hubo en efectivo y en transferencia en el día
        today = DayManager.get_current_day()

        # Fetch services for the current date from the database
        query = "SELECT * FROM Services WHERE Date = %s"
        self.db_cursor.execute(query, (today,))
        services_data = self.db_cursor.fetchall()

        # Convert data to Service objects
        services_objects = [Service(row[1], row[2], row[3], row[4], row[5], row[6]) for row in services_data]

        cash_expenses, transfer_expenses, total_cash_amount, total_transfer_amount = Service.calculate_daily_expenses(
            services_objects, today)

        # Mostrar la información en un cuadro de mensaje
        message = (
            f"Hubo {cash_expenses} gastos en efectivo por un total de ${total_cash_amount:.2f} y "
            f"{transfer_expenses} gastos por transferencia por un total de ${total_transfer_amount:.2f} hoy."
        )
        messagebox.showinfo("Gastos del Día", message)

    def update_csv_text(self):
        # Fetch all services from the database
        query = "SELECT * FROM Services"
        self.db_cursor.execute(query)
        services_data = self.db_cursor.fetchall()

        # Convert data to Service objects
        services_objects = [Service(row[1], row[2], row[3], row[4], row[5], row[6]) for row in services_data]

        # Update the text box with the current CSV content
        csv_content = "\n".join([f"{service.service_name},{service.employee},{service.quantity},{service.total_price},{service.date},{service.payment_method}" for service in services_objects])
        self.csv_text.delete(1.0, END)
        self.csv_text.insert(END, csv_content)










