from re import S
from tkinter import font
import kivy
kivy.require('2.0.0')
import kivymd

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton, MDRoundFlatIconButton, MDFlatButton, MDFillRoundFlatIconButton, MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore

import webbrowser

from datetime import datetime, timedelta

### CHECKING ON SMARTPHONE SIZE SCREEN
#Window.size = (400, 700)

### DEPLOYMENT MANDATES

from android.permissions import request_permissions, Permission

from jnius import autoclass

try:
    Environment = autoclass('android.os.Environment')
    path = Environment.getExternalStorageDirectory().getAbsolutePath()
except:
    path = MDApp.get_running_app().user_data_dir

### DEPLOYMENT MANDATES

class SmokingHistoryApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Yellow'
        self.theme_cls.primary_hue = 'A700'
        self.theme_cls.theme_style = 'Dark'

        self.state = 1
        self.theme_state = 1

        self.screen = Screen()

        self.btn_list = MDRectangleFlatIconButton(
            text = 'History',
            icon = 'table-eye',
            font_size = '17sp',
            pos_hint = {'center_x': 0.3, 'center_y': 0.05},
            line_color = [0, 0, 0, 0],
            on_release = self.view_full_list
        )
        self.screen.add_widget(self.btn_list)

        self.btn_home = MDRectangleFlatIconButton(
            text = 'Home',
            icon = 'home',
            font_size = '17sp',
            pos_hint = {'center_x': 0.3, 'center_y': 0.05},
            line_color = [0, 0, 0, 0],
            on_release = self.back_to_home
        )

        self.btn_about = MDRectangleFlatIconButton(
            text = 'About',
            icon = 'information-outline',
            font_size = '17sp',
            pos_hint = {'center_x': 0.7, 'center_y': 0.05},
            line_color = [0, 0, 0, 0],
            on_release = self.about_page
        )
        self.screen.add_widget(self.btn_about)

        self.toolbar = MDToolbar(title="Track Dhoom!")
        self.toolbar.right_action_items = [['exit-to-app', lambda x: MDApp.get_running_app().stop()]]
        self.toolbar.pos_hint = {"top": 1}
        self.screen.add_widget(self.toolbar)

        self.tf_cost = MDTextField(
            pos_hint = {'center_x': 0.5, 'center_y': 0.85},
            hint_text = 'Cost',
            helper_text = 'price of your smoke',
            helper_text_mode = 'on_focus',
            size_hint = (0.8, 1)
        )
        self.screen.add_widget(self.tf_cost)

        self.btn_smoked = MDFillRoundFlatIconButton(
            text='Smoking One!',
            icon='smoking-pipe',
            on_release=self.db_create,
            pos_hint={'center_x': 0.5, 'center_y': 0.75},
            md_bg_color=[1,1,0,1],
            font_size="20sp"
        )
        self.screen.add_widget(self.btn_smoked)

        self.lbl_total = MDLabel(
            text='YOUR SMOKING HISTORY SHOWS HERE!',
            halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint_x = 0.8,
            theme_text_color='Primary',
            font_style='H5'
        )
        self.screen.add_widget(self.lbl_total)

        self.btn_weekly_cost = MDRoundFlatIconButton(
            text = 'Weekly Spent',
            icon = 'wallet',
            on_release = self.weekly_spent,
            pos_hint = {'center_x': 0.3, 'center_y': 0.4},
            size_hint_x = None,
            width = 150,
            font_size = '16sp'
        )
        self.screen.add_widget(self.btn_weekly_cost)

        self.btn_weekly_total = MDRoundFlatIconButton(
            text='Weekly Total',
            icon='calendar-weekend',
            on_release=self.weekly_total_count,
            pos_hint={'center_x': 0.7, 'center_y': 0.4},
            size_hint_x=None,
            width=150,
            font_size='16sp'
        )
        self.screen.add_widget(self.btn_weekly_total)

        self.btn_monthly_cost = MDRoundFlatIconButton(
            text='Monthly Spent',
            icon='wallet-outline',
            on_release=self.monthly_spent,
            pos_hint={'center_x': 0.3, 'center_y': 0.34},
            size_hint_x=None,
            width=150,
            font_size='16sp'
        )
        self.screen.add_widget(self.btn_monthly_cost)

        self.btn_monthly_total = MDRoundFlatIconButton(
            text='Monthly Total',
            icon='calendar-month-outline',
            on_release=self.monthly_count,
            pos_hint={'center_x': 0.7, 'center_y': 0.34},
            size_hint_x=None,
            width=150,
            font_size='16sp'
        )
        self.screen.add_widget(self.btn_monthly_total)

        self.btn_total_spent = MDRoundFlatIconButton(
            text='Total Spent',
            icon='wallet',
            on_release=self.total_spent,
            pos_hint={'center_x': 0.3, 'center_y': 0.28},
            size_hint_x=None,
            width=150,
            font_size='16sp'
        )
        self.screen.add_widget(self.btn_total_spent)

        self.btn_total = MDRoundFlatIconButton(
            text='Total Smoked',
            icon='calendar-check',
            on_release=self.total_count,
            pos_hint={'center_x': 0.7, 'center_y': 0.28},
            size_hint_x=None,
            width=150,
            font_size='16sp'
        )
        self.screen.add_widget(self.btn_total)

        self.table = MDDataTable(
            rows_num = 10,
            use_pagination = True,
            pagination_menu_pos = 'auto',
            pagination_menu_height = '240dp',
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            size_hint = (1, 0.75),
            column_data = [
                ('Date', dp(30)),
                ('Time', dp(30)),
                ('Cost', dp(30))
            ]
        )

        self.lbl_about = MDLabel(
            text = "It's the Beta/Trial version of Track Dhoom. There is no noble objective except to help myself and my friends with this app!" + "\n\n" + "At the time of smoking, open the app and enter the price of your smoke; press the 'Smoking One' button. That's all! The app will keep a record of your smoking." + "\n\n" + "In this version, you can see some basic and important statistics of your smoking habit. In the upcoming versions, I am coming up with some more interesting and useful statistical models.",
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            size_hint_x = 0.8
        )

        return self.screen

    def view_full_list(self, args):
        if self.state == 3:
            self.screen.remove_widget(self.btn_github)

        self.state = 2

        self.screen.remove_widget(self.tf_cost)
        self.screen.remove_widget(self.btn_smoked)
        self.screen.remove_widget(self.lbl_total)
        self.screen.remove_widget(self.btn_weekly_total)
        self.screen.remove_widget(self.btn_monthly_cost)
        self.screen.remove_widget(self.btn_total_spent)
        self.screen.remove_widget(self.btn_monthly_total)
        self.screen.remove_widget(self.btn_total)
        self.screen.remove_widget(self.btn_weekly_cost)
        self.screen.remove_widget(self.btn_list)
        self.screen.remove_widget(self.lbl_about)
        self.screen.remove_widget(self.btn_about)

        self.screen.add_widget(self.table)
        self.screen.add_widget(self.btn_home)
        self.screen.add_widget(self.btn_about)

    def back_to_home(self, args):
        if self.state == 3:
            self.screen.remove_widget(self.btn_github)

        self.state = 1

        self.screen.remove_widget(self.table)
        self.screen.remove_widget(self.btn_home)
        self.screen.remove_widget(self.lbl_about)
        self.screen.remove_widget(self.btn_about)

        self.screen.add_widget(self.tf_cost)
        self.screen.add_widget(self.btn_smoked)
        self.screen.add_widget(self.lbl_total)
        self.screen.add_widget(self.btn_weekly_total)
        self.screen.add_widget(self.btn_monthly_cost)
        self.screen.add_widget(self.btn_total_spent)
        self.screen.add_widget(self.btn_monthly_total)
        self.screen.add_widget(self.btn_total)
        self.screen.add_widget(self.btn_weekly_cost)
        self.screen.add_widget(self.btn_list)
        self.screen.add_widget(self.btn_about)

    def about_page(self, args):
        if self.state == 1:
            self.screen.remove_widget(self.tf_cost)
            self.screen.remove_widget(self.btn_smoked)
            self.screen.remove_widget(self.lbl_total)
            self.screen.remove_widget(self.btn_weekly_total)
            self.screen.remove_widget(self.btn_monthly_cost)
            self.screen.remove_widget(self.btn_total_spent)
            self.screen.remove_widget(self.btn_monthly_total)
            self.screen.remove_widget(self.btn_total)
            self.screen.remove_widget(self.btn_weekly_cost)
            self.screen.remove_widget(self.btn_list)

            self.screen.add_widget(self.btn_home)
        elif self.state == 2:
            self.screen.remove_widget(self.table)
            self.screen.remove_widget(self.btn_home)
            
            self.screen.add_widget(self.btn_list)

        self.state = 3

        self.screen.remove_widget(self.btn_about)

        self.btn_github = MDFlatButton(
            text = 'Open GitHub Repository',
            font_style = 'H6',
            theme_text_color='Primary',
            pos_hint = {'center_x': 0.5, 'center_y': 0.25}
        )
        self.btn_github.bind(on_press=lambda x: webbrowser.open('https://github.com/ee-shan/Track-Dhoom'))

        self.screen.add_widget(self.btn_github)
        self.screen.add_widget(self.lbl_about)

    def on_start(self):
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]) ### DEPLOYMENT MANDATE
        self.store = JsonStore(f"{path}/db_trackdhoom.json") ### DEPLOYMENT MANDATE
#        self.store = JsonStore('db_trackdhoom.json') ### TESTING ON PC

        count = 0
        for key in self.store.keys():
            if self.store.get(str(key))['date'] == datetime.now().strftime('%d/%m/%Y'):
                count += 1
        self.lbl_total.text = "YOU'VE ALREADY SMOKED " + str(count) + ' STICK(S) TODAY'

        for key in self.store.keys():
            date = self.store.get(str(key))['date']
            time = self.store.get(str(key))['time']
            cost = self.store.get(str(key))['cost']

            self.table.row_data.insert(len(self.table.row_data), (date, time, cost))

    def db_create(self, args):
        if self.tf_cost.text == '':
            self.dialog = MDDialog(
                title = 'Warning',
                text = 'You have to insert cost to record your smoking!',
                radius = [40, 7, 40, 7],
                buttons = [
                    MDFlatButton(
                        text = 'OK',
                        theme_text_color = 'Custom',
                        text_color = self.theme_cls.primary_color,
                        on_release = self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            self.dialog = MDDialog(
                title = 'Successful',
                text = 'Your smoking record has been added in the database!',
                radius = [40, 7, 40, 7],
                buttons = [
                    MDFlatButton(
                        text = 'OK',
                        theme_text_color = 'Custom',
                        text_color = self.theme_cls.primary_color,
                        on_release = self.close_dialog
                    )
                ]
            )
            self.dialog.open()

            current_date = datetime.now().strftime('%d/%m/%Y')
            current_time = datetime.now().strftime('%H:%M:%S')
            cost = int(self.tf_cost.text)

            if self.store.keys():
                idx = str(int(self.store.keys()[-1]) + 1)
            else:
                idx = str(1)

            self.store.put(
                idx,
                date = current_date,
                time = current_time,
                cost = cost
            )

            count = 0
            for key in self.store.keys():
                if self.store.get(str(key))['date'] == datetime.now().strftime('%d/%m/%Y'):
                    count += 1
            self.lbl_total.text = "YOU'VE ALREADY SMOKED " + str(count) + ' STICK(S) TODAY'
            
            self.table.row_data.insert(len(self.table.row_data), (current_date, current_time, cost))

    def close_dialog(self, args):
        self.dialog.dismiss()

    def total_count(self, args):
        self.lbl_total.text = 'OVERALL SMOKING COUNT:' + '\n' + str(len(self.store.keys())) + ' STICK(S)'

    def total_spent(self, args):
        cost = 0
        for key in self.store.keys():
            cost += int(self.store.get(str(key))['cost'])
        self.lbl_total.text = 'OVERALL SMOKING COST:' + '\n' + str(cost) + ' BDT'

    def weekly_total_count(self, args):
        prev_dt = datetime.now() - timedelta(days = 7)
        prev_y = int(prev_dt.strftime('%Y'))
        prev_m = int(prev_dt.strftime('%m'))
        prev_d = int(prev_dt.strftime('%d'))
        prev = datetime(prev_y, prev_m, prev_d)

        count = 0
        for key in self.store.keys():
            temp_dt = self.store.get(str(key))['date']
            temp_y = int(temp_dt[6:])
            temp_m = int(temp_dt[3:5])
            temp_d = int(temp_dt[0:2])
            temp = datetime(temp_y, temp_m, temp_d)

            if temp > prev:
                count += 1

        self.lbl_total.text = 'WEEKLY SMOKING COUNT:' + '\n' + str(count) + ' STICK(S)'

    def weekly_spent(self, args):
        prev_dt = datetime.now() - timedelta(days = 7)
        prev_y = int(prev_dt.strftime('%Y'))
        prev_m = int(prev_dt.strftime('%m'))
        prev_d = int(prev_dt.strftime('%d'))
        prev = datetime(prev_y, prev_m, prev_d)

        cost = 0
        for key in self.store.keys():
            temp_dt = self.store.get(str(key))['date']
            temp_y = int(temp_dt[6:])
            temp_m = int(temp_dt[3:5])
            temp_d = int(temp_dt[0:2])
            temp = datetime(temp_y, temp_m, temp_d)

            if temp > prev:
                cost += int(self.store.get(str(key))['cost'])

        self.lbl_total.text = 'WEEKLY SMOKING COST:' + '\n' + str(cost) + ' BDT'

    def monthly_count(self, args):
        count = 0
        for key in self.store.keys():
            if self.store.get(str(key))['date'][3:] == datetime.now().strftime('%m/%Y'):
                count += 1
        self.lbl_total.text = 'MONTHLY SMOKING COUNT:' + '\n' + str(count) + ' STICK(S)'

    def monthly_spent(self, args):
        cost = 0
        for key in self.store.keys():
            if self.store.get(str(key))['date'][3:] == datetime.now().strftime('%m/%Y'):
                cost += int(self.store.get(str(key))['cost'])
        self.lbl_total.text = 'MONTHLY SMOKING COST:' + '\n' + str(cost) + ' BDT'

if __name__ == '__main__':
    SmokingHistoryApp().run()
