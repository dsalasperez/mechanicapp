from datetime import datetime
import mysql.connector
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen


class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="mechanic",
            password="2",
            database="mechdb"
        )
        self.cursor = self.db.cursor()

    def insert_data(self, car, parts, description):
        query = "INSERT INTO repairs (car, parts, description, datetime) VALUES (%s, %s, %s, %s)"
        values = (car, parts, description, datetime.now())
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print("An error occurred when inserting data:", e)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.database = Database()

        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        username_label = Label(text='Username:')
        self.username_input = TextInput()
        layout.add_widget(username_label)
        layout.add_widget(self.username_input)

        password_label = Label(text='Password:')
        self.password_input = TextInput(password=True)
        layout.add_widget(password_label)
        layout.add_widget(self.password_input)

        login_button = Button(text='Login')
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # Add your login logic here
        # You can use the provided database class or any other mechanism to validate the credentials

        # For demonstration purposes, let's assume a successful login
        self.manager.current = 'data'  # Transition to the data entry screen


class DataScreen(Screen):
    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)
        self.database = Database()

        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        car_label = Label(text='Car:')
        self.car_input = TextInput()
        layout.add_widget(car_label)
        layout.add_widget(self.car_input)

        parts_label = Label(text='Parts:')
        self.parts_input = TextInput()
        layout.add_widget(parts_label)
        layout.add_widget(self.parts_input)

        description_label = Label(text='Description:')
        self.description_input = TextInput()
        layout.add_widget(description_label)
        layout.add_widget(self.description_input)

        submit_button = Button(text='Submit')
        submit_button.bind(on_press=self.submit_data)
        layout.add_widget(submit_button)

    def submit_data(self, instance):
        car = self.car_input.text
        parts = self.parts_input.text
        description = self.description_input.text

        self.database.insert_data(car, parts, description)

        self.clear_inputs()
        print("Data submitted successfully.")

    def clear_inputs(self):
        self.car_input.text = ""
        self.parts_input.text = ""
        self.description_input.text = ""


class MechanicApp(App):
    def build(self):
        sm = ScreenManager()

        login_screen = LoginScreen(name='login')
        sm.add_widget(login_screen)

        data_screen = DataScreen(name='data')
        sm.add_widget(data_screen)

        return sm


if __name__ == '__main__':
    MechanicApp().run()