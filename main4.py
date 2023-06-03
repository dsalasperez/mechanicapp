from datetime import datetime
import mysql.connector
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="mechanic",
            password="2",
            database="mechdb"
        )
        self.cursor = self.db.cursor()

    def create_user(self, username, password, name, email):
        query = "INSERT INTO users (username, password, name, email) VALUES (%s, %s, %s, %s)"
        values = (username, password, name, email)
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            print("User created successfully.")
            return self.cursor.lastrowid
        except Exception as e:
            print("An error occurred when creating a user:", e)
            return None

    def validate_credentials(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]  # Assuming the first column is id
        else:
            return None

    def insert_data(self, car, parts, description, datetime, user_id, submitted_by):
        query = "INSERT INTO repairs (car, parts, description, datetime, user_id, submitted_by) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (car, parts, description, datetime, user_id, submitted_by)

        self.cursor.execute(query, values)
        self.db.commit()

    def get_username(self, user_id):
        query = "SELECT username FROM users WHERE id = %s"
        values = (user_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

class LoginScreen(Screen):
    user_id = None  # Add user_id attribute

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

    def goto_register(self, instance):
        self.manager.current = 'register'

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # Perform login logic and validate credentials
        user_id = self.database.validate_credentials(username, password)

        if user_id is not None:
            self.user_id = user_id  # Update the user_id attribute
            self.manager.current = 'data'  # Transition to the data screen
            print(f"Successfully logged in as user with ID {user_id}")
        else:
            print("Invalid username or password")

    def validate_credentials(self, username, password):
        # Replace this with your own logic to validate the credentials
        # You can use the provided database class or any other mechanism

        # Example implementation using the Database class
        user_id = self.database.validate_credentials(username, password)
        if user_id is not None:
            return True
        else:
            return False    

# RegisterScreen class
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

        layout.add_widget(Label(text='Email'))  # Added email label
        self.email_input = TextInput(multiline=False)  # Added email input field
        layout.add_widget(self.email_input)  # Added email input field

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
        email = self.email_input.text  # Retrieve email value
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        # Validate input
        if not name or not username or not email or not password or not confirm_password:
            print("Please fill in all fields.")
            return

        if password != confirm_password:
            print("Passwords do not match.")
            return

        # Perform the registration logic here
        # You can use the provided database class or any other mechanism to store the user information
        # After successful registration, you can transition to another screen if needed

        user_id = self.database.create_user(username, password, name, email)  # Pass email parameter
        if user_id is not None:
            print(f"Successfully registered user {username} with ID {user_id}")
            self.manager.current = 'data'  # Transition to the data screen
        else:
            print(f"Failed to register user {username}")

        # Clear input fields
        self.name_input.text = ""
        self.username_input.text = ""
        self.email_input.text = ""  # Clear email input field
        self.password_input.text = ""
        self.confirm_password_input.text = ""

class DataScreen(Screen):
    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)

        self.database = Database()

        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        layout.add_widget(Label(text='Car'))
        self.car_input = TextInput(multiline=False)  # Store reference to TextInput in instance variable
        layout.add_widget(self.car_input)

        layout.add_widget(Label(text='Parts'))
        self.parts_input = TextInput(multiline=False)  # Store reference to TextInput in instance variable
        layout.add_widget(self.parts_input)

        layout.add_widget(Label(text='Description'))
        self.description_input = TextInput(multiline=True)  # Store reference to TextInput in instance variable
        layout.add_widget(self.description_input)

        submit_button = Button(text='Submit')
        submit_button.bind(on_press=self.submit_data)
        layout.add_widget(submit_button)

        logout_button = Button(text='Logout')
        logout_button.bind(on_press=self.logout)
        layout.add_widget(logout_button)

    def submit_data(self, instance):
        # Extract information from input widgets using instance variables
        car = self.car_input.text
        parts = self.parts_input.text
        description = self.description_input.text
        datetime_input = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = self.manager.get_screen('login').user_id  # Get user id from the login screen
        submitted_by = self.database.get_username(user_id)

        # Insert data to database
        self.database.insert_data(car, parts, description, datetime_input, user_id, submitted_by)

        # Clear the input fields
        self.car_input.text = ""
        self.parts_input.text = ""
        self.description_input.text = ""

        # Show a message that the data was submitted
        popup = Popup(title='Success',
                      content=Label(text='Data submitted successfully'),
                      size_hint=(None, None), size=(400, 400))
        popup.open()

    def logout(self, instance):
        self.manager.current = 'login'
        print("Logged out successfully.")

class MechanicApp(App):
    def build(self):
        sm = ScreenManager()

        login_screen = LoginScreen(name='login')
        sm.add_widget(login_screen)

        # Create the register screen
        register_screen = RegisterScreen(name='register')
        sm.add_widget(register_screen)

        # Create the data entry screen
        data_screen = DataScreen(name='data')
        sm.add_widget(data_screen)

        return sm


if __name__ == '__main__':
    MechanicApp().run()