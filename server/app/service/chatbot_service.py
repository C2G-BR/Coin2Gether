import random

from app.service.bot import Chatbot
from app.service.auth_service import verify_token
from app.service.post_story import post_story

cb = Chatbot(threshold = 0.25)
sessions = {'test': 1}

def handle_data(data, token):
    message = _get_field(data, 'message')
    session_id = _get_field(data, 'session_id')
    is_action = False
    is_navigate = False
    is_confirmation = False
    cb_message = ''
    if (message is None):
        cb_message = cb.get_greeting()
    else:
        if not (valid_session_id(session_id)):
            cb_message = cb.predict(message)
            if (is_story(cb_message)):
                if not (valid_token(token)):
                    cb_message = 'Please log in first.'
                else:
                    story = post_story(token)
                    session_id = get_session_id(story)
                    cb_message = story.get_next_step()
                    is_confirmation = story.is_confirmation_step()
                    sessions[session_id] = story
            else:
                is_navigate = get_is_navigate(cb_message)
                is_action = get_is_action(cb_message)
                if (is_action and not valid_token(token)):
                    cb_message = 'Please log in first.'
                    is_action = False
        else:
            message = _converter(message)
            cb_message = sessions[session_id].answer_current_step(message)
            if (sessions[session_id].is_complete):
                del sessions[session_id]
                session_id = None
            else:
                is_confirmation = sessions[session_id].is_confirmation_step()
    return _response_parser(cb_message, session_id, is_action or is_navigate, is_confirmation)
    
def _get_field(data, field:str):
    value = None
    try:
        value = data[field]
    except:
        pass
    return value

def _converter(message:str):
    _tmp = message.lower()
    if (_tmp == 'true'):
        return True
    elif(_tmp == 'false'):
        return False
    return message

def _response_parser(message:str, session_id:str, is_action:bool, is_confirmation:bool):
    return {
        'message': message,
        'session_id': session_id,
        'is_action': is_action,
        'is_confirmation': is_confirmation
    }

def get_is_action(classification:str):
    return classification.startswith('action::')

def get_is_navigate(classification:str):
    return classification.startswith('navigate::')

def is_story(classsification:str):
    stories = ['action::create_post']
    for story in stories:
        if (classsification == story):
            return True
    return False

def valid_token(token:str):
    try:
        verify_token(token)
        return True
    except:
        return False

def valid_session_id(session_id:str):
    if (session_id is None):
        return False
    else:
        try:
            sessions[session_id]
            return True
        except:
            return False

def get_session_id(story):
    exists = True
    while exists:
        hash = hex(random.getrandbits(64))
        exists = hash in sessions.keys()
    return hash