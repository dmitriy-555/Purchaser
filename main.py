from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
# from kivy.properties import StringProperty, ListProperty

from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
# from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList, ThreeLineListItem, TwoLineIconListItem

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty, ObjectProperty
import datetime

# from kivymd.icon_definitions import md_icons
# from kivymd.font_definitions import fonts
# from kivymd.uix.label import MDLabel
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, BaseListItem
# from kivy.uix.scrollview import ScrollView
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label

import sqlite3

import requests

Window.size = (400, 600)


class event_screen(Screen):
    pass


class dish_screen(Screen):
    pass


class ing_screen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class Tab(MDFloatLayout, MDTabsBase):
    pass


class Content(TwoLineIconListItem):
    pass


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class dish_container(BaseListItem):
    ntext = StringProperty()


class TestNavigationDrawer(MDApp):
    title = "Purchaser"
    by_who = "by sssss"
    index = 2
    ccru = 1
    name_tab = "Добавление мероприятия"
    dir_list = []
    data_on_bd = {}


    event_item_test = {
        "просмотр аниме": "Нажмите для подробностей"
    }

    image_path = ""



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind()
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        self.exit_manager()
        toast(path)

        self.image_path = path

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def build(self):
        return Builder.load_file('my.kv')

    def on_start(self):
        self.record_on_data()

        conn = sqlite3.connect("fgh.db")

        pudge = conn.cursor()

        pudge.execute("""CREATE TABLE IF NOT EXISTS eventbase(
                            event_id INTEGER,
                            name text) 
                         """)
        pudge.execute("SELECT name FROM eventbase")

        conn.commit()

        conn.close()

    def create_bd_for_image(self):
        bd_image = sqlite3.connect("image.db")

        rubick = bd_image.cursor()

        rubick.execute("""CREATE TABLE IF NOT EXISTS image(
                                    image_id INTEGER PRIMARY KEY ,
                                    image BLOB NOT NULL) 
                                 """)
        rubick.execute("SELECT name FROM eventbase")

        bd_image.commit()

        bd_image.close()

    def on_save_event_click(self, text1, text2, text3):

        conn = sqlite3.connect("fgh.db")

        pudge = conn.cursor()

        pudge.execute("INSERT INTO eventbase VALUES (:fgh)",
                      {
                          "fgh": self.root.ids.text_user1.text,
                      })

        conn.commit()

        conn.close()


        container = Content(text=text2, secondary_text=text3)

        if self.image_path == "":
            container.add_widget(IconLeftWidget(icon="calendar-alert"))
        else:
            container.add_widget(IconLeftWidget(icon=self.image_path))
        self.dir_list.append(container)
        if text2 == "":
            text2 = " "
        if text3 == "":
            text3 = " "
        if text1 != "":
            self.root.screen_manager.current = "main_screen"
            if self.image_path == "":
                self.root.ids.event_list.add_widget(MDExpansionPanel(icon="calendar-alert",
                                                                     content=container,
                                                                     panel_cls=MDExpansionPanelTwoLine(
                                                                         text=text1,
                                                                         secondary_text="Нажмите для подробностей"
                                                                     )))
            else:
                self.root.ids.event_list.add_widget(MDExpansionPanel(icon=self.image_path,
                                                                     content=container,
                                                                     panel_cls=MDExpansionPanelTwoLine(
                                                                         text=text1,
                                                                         secondary_text="Нажмите для подробностей"
                                                                     )))

            self.root.ids.text_user1.text = ""
            self.root.ids.text_user2.text = ""
            self.root.ids.text_user3.text = ""
            self.image_path = ""

    def record_on_data(self):

        conn = sqlite3.connect("fgh.db")

        pudge = conn.cursor()

        pudge.execute("SELECT * FROM eventbase")
        records = pudge.fetchall()
        for record in records:
            self.event_item_test[record[0]] = "Нажмите для подробностей"


        for items in self.event_item_test.keys():
            self.root.ids.event_list.add_widget(MDExpansionPanel(icon="dish/b9.jpg",
                                                                 content=Content(text='просто так проверка',
                                                                                 secondary_text='Это образец но 2'),
                                                                 panel_cls=MDExpansionPanelTwoLine(
                                                                     text=items,
                                                                     secondary_text=self.event_item_test[items]
                                                                 )))



    def delete_data(self):
        conn = sqlite3.connect("fgh.db")

        pudge = conn.cursor()

        pudge.execute("DELETE FROM eventbase WHERE rowid > 2")

        #ниже_обновление_данных
        # pudge.execute("UPDATE eventbase SET fgh = хз че тут ну там типа обновление строки в табл. для изменения блюда")

        conn.commit()

        conn.close()

    def on_save(self, instance, value, date_range):
        self.root.ids.text_user3.text = value.strftime("%d-%m-%Y")

    def on_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        self.root.ids.text_user3.focus = False
        date_dialog = MDDatePicker(primary_color=(1, 0.6, 0, 0.8), text_current_color=(1, 0.5, 0, 0.8),
                                   selector_color=(1, 0.5, 0, 0.8), text_button_color=(0, 0, 0, 1))
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save_dish_click(self):
        dish = dish_container()
        dish.add_widget(MDBoxLayout(padding=5))
        dish.add_widget(Image(source=self.image_path))
        dish.add_widget(Label(text=self.root.ids.text_user_dish))
        self.root.ids.list2.add_widget(dish)

    def on_add_dish_click(self):
        pass


TestNavigationDrawer().run()
