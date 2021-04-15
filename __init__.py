from mycroft import MycroftSkill, intent_handler
import requests
import ipaddress
from mycroft.util.log import getLogger

LOGGER = getLogger(__name__)

class ShellyLights(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self.get_settings()

    @intent_handler('lights.shelly.intent')
    def handle_lights_shelly(self, message):
        light{'name'} = message.data.get('name')
        light{'state'} = message.data.get('state')
        LOGGER.info(f"Trying to turn {light{'name'}} {light{'state'}}")
        if (self.names{light{'name'}} is None):
            self.speak_dialog('unknown', data={'name': light{'name'}}, wait=False)
            return
        res = requests.get('http://' + self.names{light{'name'}} + '/relay/0?turn=' + light{'state'})
        if (res.status_code == 200):
            self.speak_dialog('lights.shelly', data={'name': light{'name'}, 'state': light{'state'}}, wait=False)
        else:
            self.speak_dialog('fail', data={'name': light{'name'}, 'state': light{'state'}}, wait=False)

    def on_settings_changed(self):
        self.get_settings()

    def get_settings(self):
        self.names = {}
        for i in range(1, 4):
            name = self.settings.get(f'name{i}', "")
            if ((name is None) or (len(name) < 4)):
                LOGGER.debug(f"Skipping name {i} (missing name or too short)")
                next
            ip = self.settings.get(f'ip{i}', "")
            try:
                ipaddress.IPv4Address(ip)
            except AddressValueError:
                LOGGER.info(f"Bad IP address for {name}")
                next
            self.names{name} = ip


def create_skill():
    return ShellyLights()

