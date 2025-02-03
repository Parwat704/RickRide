import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button as DropDownButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.uix.spinner import Spinner


# Sign-Up Screen with User Type
class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.username_input = TextInput(hint_text="Username", multiline=False, size_hint=(1, 0.1))
        self.email_input = TextInput(hint_text="Email", multiline=False, size_hint=(1, 0.1))
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint=(1, 0.1))
        self.confirm_password_input = TextInput(hint_text="Confirm Password", multiline=False, password=True, size_hint=(1, 0.1))

        self.user_type_dropdown = DropDown()
        self.driver_button = DropDownButton(text="Driver", size_hint_y=None, height=44)
        self.customer_button = DropDownButton(text="Customer", size_hint_y=None, height=44)
        self.driver_button.bind(on_release=self.set_user_type_driver)
        self.customer_button.bind(on_release=self.set_user_type_customer)
        
        self.user_type_button = Button(text="Select User Type", size_hint=(1, 0.1))
        self.user_type_button.bind(on_release=self.user_type_dropdown.open)
        
        self.user_type_dropdown.add_widget(self.driver_button)
        self.user_type_dropdown.add_widget(self.customer_button)

        sign_up_button = Button(text="Sign Up", size_hint=(1, 0.1))
        sign_up_button.bind(on_press=self.sign_up)

        layout.add_widget(self.username_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.confirm_password_input)
        layout.add_widget(self.user_type_button)
        layout.add_widget(sign_up_button)

        self.add_widget(layout)

    def set_user_type_driver(self, instance):
        self.user_type = "driver"
        self.user_type_button.text = "Driver"
        self.user_type_dropdown.dismiss()

    def set_user_type_customer(self, instance):
        self.user_type = "customer"
        self.user_type_button.text = "Customer"
        self.user_type_dropdown.dismiss()

    def sign_up(self, instance):
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if not username or not email or not password or not confirm_password or not hasattr(self, 'user_type'):
            self.show_popup("Error", "All fields are required!")
            return
        if password != confirm_password:
            self.show_popup("Error", "Passwords do not match!")
            return

        self.manager.get_screen("login").users_db[username] = {
            "email": email,
            "password": password,
            "user_type": self.user_type
        }
        self.show_popup("Success", "Account created successfully!")
        self.manager.current = "login"

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text="Close", on_press=lambda instance: popup.dismiss())
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        popup.open()


# Login Screen with User Type Checking
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.users_db = {}

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.username_input = TextInput(hint_text="Username", multiline=False, size_hint=(1, 0.1))
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint=(1, 0.1))
        login_button = Button(text="Login", size_hint=(1, 0.1))
        login_button.bind(on_press=self.check_login)

        sign_up_button = Button(text="Sign Up", size_hint=(1, 0.1))
        sign_up_button.bind(on_press=self.switch_to_sign_up)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(sign_up_button)

        self.add_widget(layout)

    def check_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username in self.users_db and self.users_db[username]["password"] == password:
            user_type = self.users_db[username]["user_type"]
            if user_type == "customer":
                self.manager.current = "customer_dashboard"
            elif user_type == "driver":
                self.manager.current = "driver_dashboard"
        else:
            self.show_popup("Error", "Invalid username or password.")

    def switch_to_sign_up(self, instance):
        self.manager.current = "sign_up"  

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text="Close", on_press=lambda instance: popup.dismiss())
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        popup.open()


# Customer Dashboard Screen
class CustomerDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Welcome to Customer Dashboard"))

        # Request Ride Button
        request_ride_button = Button(text="Request Ride", size_hint=(1, 0.1))
        request_ride_button.bind(on_press=self.request_ride)
        layout.add_widget(request_ride_button)

        self.add_widget(layout)

    def request_ride(self, instance):
        self.manager.current = "ride_request_screen"  # Go to ride request screen

# Driver Dashboard Screen
class DriverDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Welcome to Driver Dashboard"))

        # Toggle availability for driver
        self.availability_switch = Switch(active=False)
        self.availability_switch.bind(active=self.toggle_availability)
        layout.add_widget(Label(text="Mark Availability"))
        layout.add_widget(self.availability_switch)

        # Simulate ride notifications
        ride_notification_button = Button(text="New Ride Request", size_hint=(1, 0.1))
        ride_notification_button.bind(on_press=self.show_ride_request)
        layout.add_widget(ride_notification_button)

        self.add_widget(layout)

    def toggle_availability(self, instance, value):
        if value:
            print("Driver is now available for rides.")
        else:
            print("Driver is unavailable for rides.")

    def show_ride_request(self, instance):
        self.show_popup("Ride Request", "New ride request from customer.")
        
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text="Close", on_press=lambda instance: popup.dismiss())
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        popup.open()


# Main App Class
class AutoRickshawApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignUpScreen(name="sign_up"))
        sm.add_widget(CustomerDashboard(name="customer_dashboard"))
        sm.add_widget(DriverDashboard(name="driver_dashboard"))

        return sm

if __name__ == "__main__":
    AutoRickshawApp().run()
