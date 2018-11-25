from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from main import Character, Room
from ask_sdk_core.skill_builder import SkillBuilder


class LaunchRequestHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return is_intent_name("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        speech_text = "Welcome to Folklore!"

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Folklore", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: # (HandlerInput) -> bool
        return is_intent_name("HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: # (HandlerInput) -> Response
        speech_text = "You will find no comfort here."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Folklore", speech_text))
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: # (HandlerInput) -> bool
        return is_intent_name("CancelIntent")(handler_input) or is_intent_name("StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: # (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Folklore", speech_text))
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type(HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response


class PlayGameHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type(HandlerInput) -> bool
        return is_request_type("StartIntent")(handler_input) or is_intent_name('StartGame')(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        if handler_input.attributes_manager.persistent_attributes['character'] is None:
            character = Character(100, 5)
            handler_input.response_builder.ask("What is your name?")
            handler_input.attributes_manager.persistent_attributes["character"] = character
        return handler_input.response_builder.response


class AttackHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type(HandlerInput) -> bool
        return is_request_type("AttackIntent")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        character = handler_input.attributes_manager.persistent_attributes['character']
        enemy = handler_input.attributes_manager.persistent_attributes['room'].enemy
        if character.health <= 0:
            speech_text = "You died, please try again."
            handler_input.attributes_manager.persistent_attributes['character'] = None
        else:
            enemy.damage_character(character.damage)
            if enemy.health <= 0:
                speech_text = "Well done you killed {}".format(enemy.name)
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class RoomHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type(HandlerInput) -> bool
        return is_request_type("MoveIntent")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        character = handler_input.attributes_manager.persistent_attributes['character']
        handler_input.attributes_manager.persistent_attributes['room'] = Room()
        room = handler_input.attributes_manager.persistent_attributes['room']
        enemy = room.enemy
        if character.health <= 0:
            speech_text = "You died, please try again."
            handler_input.attributes_manager.persistent_attributes['character'] = None
        else:
            speech_text = room.description + enemy.description
        handler_input.response_builder.speak(speech_text).ask("What would you like to do?")
        return handler_input.response_builder.response


class SpeakHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type(HandlerInput) -> bool
        return is_request_type("SpeakIntent")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        character = handler_input.attributes_manager.persistent_attributes['character']
        room = handler_input.attributes_manager.persistent_attributes['room']
        enemy = room.enemy
        if enemy.is_friendly():
            speech_text = enemy.talk()
            handler_input.attributes_manager.persistent_attributes['room'] = None
        else:
            speech_text = "The {} ignored you and attacked, you took {} damage. ".format(enemy.name, enemy.damage)
            character.damage_character(enemy.damage)
            speech_text += "You took {} damage. ".format(enemy.damage)
        if character.health <= 0:
            speech_text += "You died, please try again."
            handler_input.attributes_manager.persistent_attributes['character'] = None
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AttackHandler())
sb.add_request_handler(SpeakHandler())
sb.add_request_handler(RoomHandler())
sb.add_request_handler(PlayGameHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

handler = sb.lambda_handler()