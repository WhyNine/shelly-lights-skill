from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
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
        LOGGER.info(f"Trying to change state of light '{name}' to '{state}'")
        if (not name in self.names):
            self.speak_dialog('unknown', data={'name': name}, wait=False)
            return
        res = requests.get(url='http://' + self.names[name] + '/relay/0?turn=' + state,auth=("waller", "croft"))
        LOGGER.debug(f"Result code = {res.status_code}, text = {res.text}")
        if (res.ok):
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
            LOGGER.info(f"Added light '{name}' at IP address '{ip}'")


def create_skill():
    return ShellyLights()

