from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import mysql.connector


class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="mechanic",
            password="2",
            database="mechanicappdb"
        )
        self.cursor = self.db.cursor()

    def create_mechanic(self, username, password, name):
        query = "INSERT INTO mechanics (username, password, name) VALUES (%s, %s, %s)"
        values = (username, password, name)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            print("Mechanic created successfully.")
            return self.cursor.lastrowid
        except Exception as e:
            print("An error occurred when creating a mechanic:", e)
            return None

    def validate_credentials(self, username, password):
        query = "SELECT * FROM mechanics WHERE username = %s AND password = %s"
        values = (username, password)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]  # Assuming the first column is id
        else:
            return None

    def log_repair_data(self, mechanic_id, part_name, date_replaced, comments):
        query = "INSERT INTO repair_data (mechanic_id, part_name, date_replaced, comments) VALUES (%s, %s, %s, %s)"
        values = (mechanic_id, part_name, date_replaced, comments)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            print("Data logged successfully.")
        except Exception as e:
            print("An error occurred when logging repair data:", e)

    def get_mechanic_name(self, mechanic_id):
        query = "SELECT name FROM mechanics WHERE id = %s"
        values = (mechanic_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.database = Database()

        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        layout.add_widget(Label(text='Name'))
        self.name_input = TextInput(multiline=False)
        layout.add_widget(self.name_input)

        layout.add_widget(Label(text='Username'))
        self.username_input = TextInput(multiline=False)
        layout.add_widget(self.username_input)

        layout.add_widget(Label(text='Password'))
        self.password_input = TextInput(password=True, multiline=False)
        layout.add_widget(self.password_input)

        layout.add_widget(Label(text='Confirm Password'))
        self.confirm_password_input = TextInput(password=True, multiline=False)
        layout.add_widget(self.confirm_password_input)

        register_button = Button(text='Register')
        register_button.bind(on_press=self.register)
        layout.add_widget(register_button)

    def register(self, instance):
        name = self.name_input.text
        username = self.username_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        # Validate input
        if not name or not username or not password or not confirm_password:
            print("Please fill in all fields.")
            return

        if password != confirm_password:
            print("Passwords do not match.")
            return

        # Perform the registration logic here
        # You can use the provided database class or any other mechanism to store the user information
        # After successful registration, you can transition to another screen if needed

        mechanic_id = self.database.create_mechanic(username, password, name)
        if mechanic_id is not None:
            print(f"Successfully registered mechanic {username} with ID {mechanic_id}")
            self.manager.current = 'login'  # Transition to the login screen
        else:
            print(f"Failed to register mechanic {username}")

        # Clear input fields
        self.name_input.text = ""
        self.username_input.text = ""
        self.password_input.text = ""
        self.confirm_password_input.text = ""

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.database = Database()

        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        layout.add_widget(Label(text='Username'))
        self.username_input = TextInput(multiline=False)
        layout.add_widget(self.username_input)

        layout.add_widget(Label(text='Password'))
        self.password_input = TextInput(password=True, multiline=False)
        layout.add_widget(self.password_input)

        login_button = Button(text='Login')
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)

        register_button = Button(text='Register')
        register_button.bind(on_press=self.goto_register)
        layout.add_widget(register_button)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # Validate input
        if not username or not password:
            print("Please fill in all fields.")
            return

        mechanic_id = self.database.validate_credentials(username, password)
        if mechanic_id is not None:
            data_screen = self.manager.get_screen('data')
            data_screen.set_mechanic_id(mechanic_id)
            self.manager.current = 'data'  # Transition to the data screen
        else:
            print("Invalid credentials.")

        # Clear input fields
        self.username_input.text = ""
        self.password_input.text = ""

    def goto_register(self, instance):
        self.manager.current = 'register'

class DataScreen(Screen):
    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)
        self.mechanic_id = None
        self.database = Database()

        self.orientation = 'vertical'

        # Part Number
        part_number_label = Label(text='Part Number:')
        self.part_number_input = TextInput()
        self.add_widget(part_number_label)
        self.add_widget(self.part_number_input)

        # Price
        price_label = Label(text='Price:')
        self.price_input = TextInput()
        self.add_widget(price_label)
        self.add_widget(self.price_input)

        # Description
        description_label = Label(text='Description:')
        self.description_input = TextInput()
        self.add_widget(description_label)
        self.add_widget(self.description_input)

        # Vehicle
        vehicle_label = Label(text='Vehicle:')
        self.vehicle_input = TextInput()
        self.add_widget(vehicle_label)
        self.add_widget(self.vehicle_input)

        # Customer Name
        customer_name_label = Label(text='Customer Name:')
        self.customer_name_input = TextInput()
        self.add_widget(customer_name_label)
        self.add_widget(self.customer_name_input)

        # Submit Button
        submit_button = Button(text='Submit')
        submit_button.bind(on_press=self.submit_data)
        self.add_widget(submit_button)

        # Logout Button
        logout_button = Button(text='Logout')
        logout_button.bind(on_press=self.logout)
        self.add_widget(logout_button)

    def submit_data(self, instance):
        part_number = self.part_number_input.text
        price = self.price_input.text
        description = self.description_input.text
        vehicle = self.vehicle_input.text
        customer_name = self.customer_name_input.text
        mechanic_id = self.get_mechanic_id()
        date_replaced = date.today()  # Assuming today's date
        comments = ""  # No comments input field, leaving it empty for now

        # Insert the data into the database, including the mechanic's ID and the current timestamp
        self.database.log_repair_data(mechanic_id, part_number, date_replaced, comments)

        self.clear_inputs()
        print("Data submitted successfully.")

    def logout(self, instance):
        self.manager.current = 'login'
        print("Logged out successfully.")

    def get_mechanic_id(self):
        return self.mechanic_id

    def set_mechanic_id(self, mechanic_id):
        self.mechanic_id = mechanic_id

    def clear_inputs(self):
        self.part_number_input.text = ""
        self.price_input.text = ""
        self.description_input.text = ""
        self.vehicle_input.text = ""
        self.customer_name_input.text = ""

class MechanicApp(App):
    def build(self):
        sm = ScreenManager()

        # Create the login screen
        login_screen = LoginScreen(name='login')
        sm.add_widget(login_screen)

        # Create the data entry screen
        data_screen = DataScreen(name='data')
        sm.add_widget(data_screen)

        # Create the register screen
        register_screen = RegisterScreen(name='register')
        sm.add_widget(register_screen)

        return sm


if __name__ == '__main__':
    MechanicApp().run()
