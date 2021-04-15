from mycroft import MycroftSkill, intent_file_handler


class ShellyLights(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('lights.shelly.intent')
    def handle_lights_shelly(self, message):
        self.speak_dialog('lights.shelly')


def create_skill():
    return ShellyLights()

