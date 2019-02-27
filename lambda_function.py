from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
import logging
import random
from main import Character, Room
from ask_sdk_core.skill_builder import SkillBuilder

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
character = None
room = None


def handle_attack(self):
    global character
    global room
    i = 0
    for e in room.enemies:
        if e.health > 0:
            enemy = e
            break
    if character.health <= 0:
        speech_text = "You died, please try again."
    else:
        enemy.damage_character(character.damage)
        if enemy.health <= 0:
            speech_text = "You did {} damage, well done you killed the {}".format(character.damage, enemy.name)
        else:
            character.damage_character(enemy.damage)
            speech_text = "You attacked the {} for {} damage, it has {} health remaining. The {} attacked you for {} damage, you have {} health remaining, what would you like to do?".format(
                enemy.name, character.damage, enemy.health, enemy.name, enemy.damage, character.health)
    card_title = "ATTACK"
    card_text = "you attacked the {}".format(enemy.name)
    reprompt = "attack again?"
    return build_response(speech_text, card_title, card_text, reprompt, False)


def handle_room(event):
    global character
    global room
    set_scene(event, [create_enemy(event)])
    if character.health <= 0:
        speech = "You died, please try again."
    else:
        speech = "You enter a {} and see a {} it {}, what would you like to do?".format(room.description,
                                                                                        room.enemies[0].name,
                                                                                        room.enemies[0].description)
    reprompt = 'Do you attack?'
    card_title = 'New Room'
    card_text = speech
    return build_response(speech, card_title, card_text, reprompt, False)


def handle_speak(event):
    global character
    global room
    enemy = room.enemies[0]
    if enemy.is_friendly():
        speech_text = enemy.talk()
    else:
        speech_text = "The {} ignored you and attacked, you took {} damage. ".format(enemy.name, enemy.damage)
        character.damage_character(enemy.damage)
        if character.health <= 0:
            speech_text += "You died, please try again."
    reprompt = 'Trying to talk it out'
    card_title = 'trying to talk it out'
    card_text = speech_text
    return build_response(speech_text, card_title, card_text, reprompt, False)


def set_scene(event, enemies):
    global room
    room = Room(enemies)


def state_room(event):
    global character
    global room
    speech = "you are in a {} with a {} in it, it still {}, what would you like to do?".format(room.description,
                                                                                               room.enemies[0].name,
                                                                                               room.enemies[
                                                                                                   0].description)
    reprompt = 'Do you attack?'
    card_title = 'same room'
    card_text = speech
    return build_response(speech, card_title, card_text, reprompt, False)


def create_enemy(event):
    x = random.randint(0, 1)
    if x == 0:
        enemy = Character(random.randint(2, 8), random.randint(5, 10))
    else:
        enemy = Character(random.randint(6, 12), random.randint(10, 20))
    return enemy


def set_up(event):
    global room
    global character
    input = event['request']['intent']['slots']['input']['value']
    character = Character(100, 5)
    set_scene(event, [create_enemy(event)])
    if input == 'no':
        speech = "Despite not wanting to go on an adventure the ground breaks out from underneath you and you find yourself in a {} and see a {} it {}, what would you like to do?".format(
            room.description, room.enemies[0].name, room.enemies[0].description)
    else:
        speech = "You enter a {} and see a {} it {}".format(room.description, room.enemies[0].name,
                                                            room.enemies[0].description)
    reprompt = 'Do you attack?'
    card_title = 'New Room'
    card_text = speech
    return build_response(speech, card_title, card_text, reprompt, False)


def on_start():
    logger.info('Start of Game')
    return on_launch()


def on_launch():
    speech = "Welcome to Folklore, Do you want to go on an adventure?"
    card_title = "Folklore"
    card_text = "Welcome to Folklore, its adventure time"
    prompt_text = "are you ready?"
    return build_response(speech, card_title, card_text, prompt_text, False)


def on_end():
    logger.info('End of Game')


def lambda_handler(event, context):
    if event['session']['new'] == 'true':
        on_start()
    if event['request']['type'] == 'LaunchRequest':
        return on_launch()
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()


def intent_scheme(event):
    intent_name = event['request']['intent']['name']
    if intent_name == "ConfirmIntent":
        return set_up(event)
    elif intent_name == "AttackIntent":
        return handle_attack(event)
    elif intent_name == "ListRoomIntent":
        return state_room(event)
    elif intent_name == "StartGame":
        return on_launch(event)
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "SpeakIntent":
        return handle_speak(event)
    elif intent_name == "RoomIntent":
        return handle_room(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)

def build_card(text, title):
    card = {}
    card['title'] = title
    card['text'] = text
    card['type'] = 'Simple'
    return card


def build_speech(text):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = text
    return speech


def build_sub_fields(speech_text, card_title, card_text, prompt, end_session):
    speech_response = {}
    speech_response['outputSpeech'] = build_speech(speech_text)
    speech_response['card'] = build_card(card_text, card_title)
    speech_response['shouldEndSession'] = end_session
    return speech_response


def build_response(speech_text, card_title, card_text, prompt, end_session, character=None, room=None):
    response = {}
    response['version'] = '1.0'
    response['response'] = build_sub_fields(speech_text, card_title, card_text, prompt, end_session)
    if character:
        response['session'] = {}
        response['session']['character'] = build_character_json(character)
    if room:
        response['session'] = {}
        response['session']['room'] = build_room_json(room)
    logger.info(response)
    return response


def build_character_json(character):
    response = {}
    response['name'] = character.name
    response['health'] = character.health
    response['damage'] = character.damage
    response['description'] = character.description
    response['friendly'] = character.friendly
    return response


def build_room_json(room):
    response = {}
    response['enemy'] = build_character_json(room.enemy)
    response['description'] = room.description
    return response


def get_character_from_json(json):
    character = Character()
    character.name = json['name']
    character.health = json['health']
    character.damage = json['damage']
    character.description = json['description']
    character.is_friendly = json['friendly']
    return character


def get_room_from_json(json):
    room = Room()
    room.enemy = get_character_from_json(json['enemy'])
    room.description = json[description]
    return room