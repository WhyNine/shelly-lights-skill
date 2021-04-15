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
        name = message.data.get('name')
        state = message.data.get('state')
        LOGGER.info(f"Trying to turn {name} {state}")
        if (name in self.names):
            self.speak_dialog('unknown', data={'name': name}, wait=False)
            return
        res = requests.get('http://' + self.names[name] + '/relay/0?turn=' + state)
        if (res.status_code == 200):
            self.speak_dialog('lights.shelly', data={'name': name, 'state': state}, wait=False)
        else:
            self.speak_dialog('fail', data={'name': name, 'state': state}, wait=False)

    def on_settings_changed(self):
        self.get_settings()

    def get_settings(self):
        self.names = {}
        for i in range(1, 5):
            name = self.settings.get(f"name{i}", "")
            if ((name is None) or (len(name) < 4)):
                LOGGER.debug(f"Skipping name {i} (missing name or too short)")
                continue
            ip = self.settings.get(f"ip{i}", "")
            try:
                ipaddress.IPv4Address(ip)
            except:
                LOGGER.info(f"Bad IP address for {name}")
                continue
            self.names[name] = ip


def create_skill():
    return ShellyLights()

