from ask_sdk_core.skill_builder import SkillBuilder
from handlers import LaunchRequestHandler, HelloWorldIntentHandler, HelpIntentHandler, CancelAndStopIntentHandler, SessionEndedRequestHandler

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

handler = sb.lambda_handler()
