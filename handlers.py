from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard


class LaunchRequestHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return is_intent_name("")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class HelloWorldIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: # (HandlerInput) -> bool
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: # (HandlerInput) -> Response
        speech_text = "Hello World"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: # (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: # (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: # (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: # (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type(HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response

