from mycroft import MycroftSkill, intent_handler
import requests
from mycroft.util.log import getLogger

LOGGER = getLogger(__name__)

class ShellyLights(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('lights.shelly.intent')
    def handle_lights_shelly(self, message):
        light{'name'} = = message.data.get('name')
        light{'state'} = = message.data.get('state')
        LOGGER.info(f"Trying to turn {light{'name'}} {light{'state'}}")
        if (names{light{'name'}} is None):
            self.speak_dialog('unknown', data={'name': light{'name'}}, wait=False)
            return
        res = requests.get('http://' + ip{light{'name'}} + '/relay/0?turn=' + light{'state'})
        if (res.status_code == 200):
            self.speak_dialog('lights.shelly', data={'name': light{'name'}, 'state': light{'state'}}, wait=False)
        else:
            self.speak_dialog('fail', data={'name': light{'name'}, 'state': light{'state'}}, wait=False)


def create_skill():
    return ShellyLights()

