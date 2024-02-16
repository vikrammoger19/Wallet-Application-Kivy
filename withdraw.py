from datetime import datetime

from anvil.tables import app_tables
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivy.core.window import Window

Builder.load_string(
    """
<WithdrawScreen>:
    # canvas.before:
    #     Color:
    #         rgba: 1, 1, 1, 1   # Background color (#DEF1FF)
    #     Rectangle:
    #         pos: self.pos
    #         size: self.size

    MDBoxLayout:
        orientation: 'vertical'              
        padding: [dp(0), dp(40), dp(0), dp(20)]  # Padding: left, top, right, bottom
        spacing: dp(20)
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_y: None
        height: self.minimum_height
        
        Widget:  # Added empty widget for space
            size_hint_y: None
            height: dp(30)

        MDTopAppBar:
            title: 'Withdraw Money'  # Updated title to 'Withdraw Money'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"
            pos_hint:{'top':1}

        MDCard:
            orientation: 'vertical'
            size_hint: 0.9, None  # 90% of parent width
            height: dp(140)
            pos_hint: {"center_x": 0.5}
            # elevation: 0.2
            radius: [10, 10, 10, 10]
            padding: dp(20)
            spacing: dp(20)
            md_bg_color: 0.7961, 0.9019, 0.9412, 1

            MDLabel:
                text: 'Total Wallet Balance'
                halign: 'left'  # Align text to the left
                valign: 'top'  # Align text to the top
                size_hint_y: None
                height: self.texture_size[1]
                pos_hint: {'x': 0}  # Align label to the left side of the MDCard

            MDBoxLayout:
                padding: dp(10)
                spacing: dp(10)
                adaptive_height: True
                pos_hint: {'center_x': 0.5, 'center_y': 0.5} 

                MDTextField:
                    id: balance_lbl
                    # text: 'Balance'
                    halign: 'center'
                    mode: "rectangle"
                    hint_text: "Balance"
                    pos_hint: {'center_x': .3}
                    size_hint: 0.8, 1.3
                    readonly: True
                    md_bg_color: 0.7961, 0.9019, 0.9412, 1
                    text_color: 0, 0, 0, 1
                    line_color: 0.5, 0.5, 0.5, 1

                MDIconButton:
                    id: options_button
                    icon: "currency-inr"
                    pos_hint: {'center_y':0.5}
                    md_bg_color: "#148EFE"  # Blue background color
                    theme_text_color: "Custom"
                    text_color: 0, 0, 0, 1  # White text color
                    on_release: root.show_currency_options(self)

        MDLabel:
            text: "Send Money from Wallet to Bank"
            halign: 'center'
            font_style: 'Subtitle1'
            size_hint_y: None
            height: dp(40)
            bold: True 
            pos_hint: {'center_x': 0.5}

        MDBoxLayout:
            padding: dp(10)
            spacing: dp(20)
            adaptive_height: True
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}  # This will create a 10dp gap

            MDRectangleFlatButton:
                id: bank_dropdown
                radius:40,40,40,40
                text: 'Select bank account'
                size_hint: 1, 1.3
                height: dp(50)
                pos_hint: {'center_x': 0.5}
                md_bg_color: 0.7961, 0.9019, 0.9412, 1
                on_release: root.fetch_bank_names()
                text_color: 0, 0, 0, 1
                line_color: 1, 1, 1, 1


        MDBoxLayout:
            padding: dp(5)
            spacing: dp(10)  # Adjust the spacing as needed
            adaptive_height: True
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}  # This will create a 10dp gap
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  # Black border color
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [15, 15, 15, 15] 
            MDTextField:
                id: amount_textfield
                mode: "rectangle"
                hint_text: "Enter amount"
                pos_hint: {'center_x': .5}
                line_color: 0.5, 0.5, 0.5, 1


        MDSeparator:
            height: dp(1)

        MDBoxLayout:
            padding: dp(10)
            spacing: dp(10)
            adaptive_height: True

            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            MDFlatButton:
                text: '+100'
                size_hint: 1, None  # Set the size_hint_x to 1 to fill the width
                height: dp(40)
                width: dp(64)
                md_bg_color: 0.7961, 0.9019, 0.9412, 1
                on_release: root.update_amount(100)

            MDFlatButton:
                text: '+200'
                size_hint: 1, None  # Set the size_hint_x to 1 to fill the width
                width: dp(64)
                height: dp(40)
                md_bg_color: 0.7961, 0.9019, 0.9412, 1
                on_release: root.update_amount(200)
            MDFlatButton:
                text: '+500'
                size_hint: 1, None
                width: dp(64)
                height: dp(40)
                md_bg_color: 0.7961, 0.9019, 0.9412, 1
                on_release: root.update_amount(500)
            MDFlatButton:
                text: '+1000'
                size_hint: 1, None
                width: dp(64)
                height: dp(40)
                md_bg_color: 0.7961, 0.9019, 0.9412, 1
                on_release: root.update_amount(1000)

        MDBoxLayout:
            padding: dp(10)
            adaptive_height: True
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            MDRaisedButton:
                text: 'Proceed '
                md_bg_color: 20/255, 142/255, 254/255, 1
                size_hint: 1.5, None  # Set the size_hint_x to 1 to fill the width
                height: dp(50)
                on_press: root.withdraw()

    MDBoxLayout:
        size_hint_y: None
        height: dp(100)
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        size_hint_x: None
        width: dp(100)
""")


class WithdrawScreen(Screen):
    def __init__(self, **kwargs):
        super(WithdrawScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def go_back(self):
        self.ids.amount_textfield.text = ""  # Clear the amount input field
        self.ids.bank_dropdown.text = "Select bank account"  # Reset the bank dropdown text
        self.update_balance_label(self.ids.options_button.text)  # Update the balance label
        self.manager.current = 'dashboard'
    def on_key(self, window, key, scancode, codepoint, modifier):
        if key in [27, 9]:
            self.go_back()
            return True
        return False

    def fetch_bank_names(self):
        try:
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]

            bank_names = app_tables.wallet_users_account.search(phone=phone)
            bank_names_str = [str(row['bank_name']) for row in bank_names]
            if bank_names_str:
                self.menu_list = [
                    {"viewclass": "OneLineListItem", "text": bank_name,
                     "on_release": lambda x=bank_name: self.test(x)}
                    for bank_name in bank_names_str
                ]

                self.menu = MDDropdownMenu(
                    caller=self.ids.bank_dropdown,
                    items=self.menu_list,
                    width_mult=4
                )
                self.menu.open()
            else:
                toast("No accounts found")

        except Exception as e:
            print(f"Error fetching bank names: {e}")

        finally:
            pass

    def test(self, text):
        self.account_number = None
        self.account_holder_name = None
        self.ids.bank_dropdown.text = text
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]

        try:
            matching_accounts = app_tables.wallet_users_account.search(phone=phone, bank_name=text)
            if matching_accounts:
                self.account_number = matching_accounts[0]['account_number']
            else:
                toast("Account not found")
            self.menu.dismiss()
        except Exception as e:
            print(f"Error fetching account details: {e}")

    def select_currency(self, currency):
        wdrw_scr = self.manager.get_screen('withdraw')
        wdrw_scr.ids.options_button.text = currency

    def withdraw(self):
        wdrw_scr = self.manager.get_screen('withdraw')
        amount = wdrw_scr.ids.amount_textfield.text
        currency = wdrw_scr.ids.options_button.text  # Get the selected currency from options_button
        date = datetime.now()
        phone = JsonStore('user_data.json').get('user')['value']["phone"]
        balance_table = app_tables.wallet_users_balance.get(phone=phone, currency_type=currency)
        selected_bank = wdrw_scr.ids.bank_dropdown.text

        if not selected_bank or not amount or not currency:
            self.show_error_popup("Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            self.show_error_popup("Invalid amount. Please enter a valid number.")
            return

        try:
            if balance_table is not None:
                old_balance = balance_table['balance']
                if amount <= old_balance:
                    new_balance = old_balance - amount
                    balance_table['balance'] = new_balance
                    balance_table.update()
                else:
                    toast("Balance is less than the entered amount")
            else:
                toast("You don't have a balance in this currency type")
            app_tables.wallet_users_transaction.add_row(
                receiver_phone=float(self.account_number),
                phone=phone,
                fund=amount,
                date=date,
                transaction_type="debit"
            )

            success_message = f"Withdrawal successful."
            self.manager.show_success_popup(success_message)
            self.manager.show_balance()
        except Exception as e:
            print(f"Error withdrawing money: {e}")
            self.show_error_popup("An error occurred. Please try again.")

    def update_amount(self, amount):
        self.ids.amount_textfield.text = str(amount)

    def show_currency_options(self, button):
        currency_options = ["INR", "GBP", "USD", "EUR"]
        self.menu_list = [
            {"viewclass": "OneLineListItem", "text": currency, "on_release": lambda x=currency: self.menu_callback(x)}
            for currency in currency_options
        ]
        print(button)
        self.menu = MDDropdownMenu(
            caller=button,
            items=self.menu_list,
            width_mult=4
        )
        self.menu.open()

    menu = None
    options_button_icon_mapping = {
        "INR": "currency-inr",
        "GBP": "currency-gbp",
        "USD": "currency-usd",
        "EUR": "currency-eur"
    }

    def menu_callback(self, instance_menu_item):
        print(f"Selected currency: {instance_menu_item}")
        store = JsonStore('user_data.json')
        phone_no = store.get('user')['value']["phone"]
        total_balance = self.manager.get_total_balance(phone_no, instance_menu_item)

        self.ids.options_button.text = instance_menu_item
        self.ids.balance_lbl.text = f'balance: {total_balance} '
        print(total_balance)
        self.ids.options_button.icon = self.options_button_icon_mapping.get(instance_menu_item, "currency-inr")
        self.menu.dismiss()

    def currencyDropdown(self):
        try:
            currencies = ["INR", "USD", "EUR", "GBP", "JPY", "AUD"]
            self.menu_list = [
                {"viewclass": "OneLineListItem", "text": currency,
                 "on_release": lambda x=currency: self.select_currency(x)}
                for currency in currencies
            ]
            self.menu = MDDropdownMenu(
                caller=self.ids.currency_dropdown,
                items=self.menu_list,
                width_mult=4
            )
            self.menu.open()
        except Exception as e:
            print(f"Error fetching currencies: {e}")

    def update_balance_label(self, currency):
        store = JsonStore('user_data.json')
        phone_no = store.get('user')['value']["phone"]
        total_balance = self.manager.get_total_balance(phone_no, currency)
        self.ids.balance_lbl.text = f'Balance: {total_balance} {currency}'