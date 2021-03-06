
import json

# import for GIS
from kivy_garden.mapview import MapView

# imports for _UI
from kivy.app import App

from kivy.uix.gridlayout import GridLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput


from communication_operator import create_listener, stop_listener, send_message_to_all


def _callback(msg_type, msg):
    if msg_type == 'text':
        msg = json.loads(msg)
        _UI.DRONE_LIST.children[_DroneButton.IDs.index(msg["id"])].set_data(
            msg["coords"]["x"],
            msg["coords"]["y"],
            msg["coords"]["z"],
            msg["charge"]
        )
    elif msg_type == 'image_path':
        _UI.IMAGE.source = msg
        _UI.IMAGE.reload()


class _DroneButton(Button):

    IDs: list = []

    def __init__(self, ID):
        super().__init__()
        self.ID = ID
        self.x_coord = None
        self.y_coord = None
        self.z_coord = None
        self.charge = None

        self.text = f'Drone {ID}'
        self.size_hint_y = None
        self.height = 40

        _DroneButton.IDs.insert(0, ID)

    def set_data(self, x, y, z, charge):
        self.x_coord = x
        self.y_coord = y
        self.z_coord = z
        self.charge = charge

        if _UI.INFO_ID.text == f"{self.ID}":
            _UI.INFO_X.text = f'{self.x_coord}' if self.x_coord is not None else ''
            _UI.INFO_Y.text = f'{self.y_coord}' if self.y_coord is not None else ''
            _UI.INFO_Z.text = f'{self.z_coord}' if self.z_coord is not None else ''
            _UI.INFO_CHRG.text = f'{self.charge}' if self.charge is not None else ''

    def on_press(self):
        _UI.INFO_ID.text = f'{self.ID}'
        _UI.INFO_X.text = f'{self.x_coord}' if self.x_coord is not None else ''
        _UI.INFO_Y.text = f'{self.y_coord}' if self.y_coord is not None else ''
        _UI.INFO_Z.text = f'{self.z_coord}' if self.z_coord is not None else ''
        _UI.INFO_CHRG.text = f'{self.charge}' if self.charge is not None else ''


class _SendButton(Button):
    def __init__(self, cmnd=None):
        super().__init__()
        self.text = 'SEND MESSAGE TO DRONES' if cmnd is None else cmnd
        self.cmnd = cmnd
        if cmnd is not None:
            self.size_hint_x = 0.4

    def on_press(self):
        if self.cmnd is not None:
            send_message_to_all(self.cmnd)
        elif _UI.DATA_INPUT.text:
            send_message_to_all(_UI.DATA_INPUT.text)
            _UI.DATA_INPUT.text = ""

        if self.cmnd == "start":
            _UI.IMAGE.source = "blank_image.png"
            _UI.IMAGE.reload()


class _UI(App):

    def build(self):

        base_layout = GridLayout(
            spacing=10,
            orientation='lr-tb',
            rows=1
        )

        left_layout = GridLayout(
            spacing=10,
            orientation='lr-tb',
            cols=1
        )

        right_layout = GridLayout(
            spacing=10,
            orientation='lr-tb',
            cols=1
        )

        btns_grid = GridLayout(
            spacing=5,
            orientation="lr-tb",
            cols=2,
            size_hint_y=0.2
        )

        left_layout.add_widget(MapView(zoom=16, lat=59.927283, lon=30.338344))

        data_input = TextInput(multiline=False)
        _UI.DATA_INPUT = data_input

        btns_grid.add_widget(data_input)
        btns_grid.add_widget(_SendButton(cmnd="start"))
        btns_grid.add_widget(_SendButton())
        btns_grid.add_widget(_SendButton(cmnd="finish"))

        left_layout.add_widget(btns_grid)

        drone_table = GridLayout(
            spacing=10,
            orientation='lr-tb',
            rows=1,
            size_hint_y=1.5
        )

        drone_list = GridLayout(
            spacing=5,
            cols=1,
            size_hint_y=None
        )
        drone_list.bind(minimum_height=drone_list.setter('height'))
        _UI.DRONE_LIST = drone_list

        with open('configuration.json') as cnfg:
            config = json.load(cnfg)
        for i in range(config['drones count']):
            drone_list.add_widget(_DroneButton(ID=i))

        scroll = ScrollView()

        scroll.add_widget(drone_list)

        info_widget = GridLayout(
            spacing=10,
            orientation='lr-tb',
            cols=1
        )
        info_widget.add_widget(Label(text='Drone ID'))
        info_widget.add_widget(Label(text=''))
        info_widget.add_widget(Label(text='X Coord'))
        info_widget.add_widget(Label(text=''))
        info_widget.add_widget(Label(text='Y Coord'))
        info_widget.add_widget(Label(text=''))
        info_widget.add_widget(Label(text='Z Coord'))
        info_widget.add_widget(Label(text=''))
        info_widget.add_widget(Label(text='Charge'))
        info_widget.add_widget(Label(text=''))
        _UI.INFO_ID = info_widget.children[8]
        _UI.INFO_X = info_widget.children[6]
        _UI.INFO_Y = info_widget.children[4]
        _UI.INFO_Z = info_widget.children[2]
        _UI.INFO_CHRG = info_widget.children[0]

        image_widget = AsyncImage()
        _UI.IMAGE = image_widget
        _UI.IMAGE.source = "blank_image.png"

        drone_table.add_widget(scroll)
        drone_table.add_widget(info_widget)

        right_layout.add_widget(drone_table)
        right_layout.add_widget(image_widget)

        base_layout.add_widget(left_layout)
        base_layout.add_widget(right_layout)

        return base_layout


def run():
    """Starts the application."""

    create_listener(_callback)
    _UI().run()

    stop_listener()
