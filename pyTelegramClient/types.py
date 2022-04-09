import json

def is_command(text):
    if text is None: 
        return False
    return text.startswith('/')

def extractCommand(text):
    if text is None: 
        return None
    return text.split()[0].split('@')[0][1:] if self.is_command(text) else None
    
class Markup:
    def keyboard(_dict , resize_keyboard=False , one_time_keyboard=False , input_field_placeholder=None):
        return { "keyboard": _dict , "resize_keyboard": resize_keyboard , "one_time_keyboard":one_time_keyboard , "input_field_placeholder":input_field_placeholder }
    
    def inline_keyboard(_dict):
        return {"inline_keyboard": json.dumps(_dict) }
    
    def remove_keyboard( selective=False ):
        return { "remove_keyboard": True , "selective": selective }
    
    def force_reply( input_field_placeholder=None , selective=False ):
        return { "force_reply":True , "selective": selective , "input_field_placeholder": input_field_placeholder }
    
    
class Button:
    def url(name , url):
        return { "text": str(name) , "url": str(url) }
    
    def inline(name , data):
        return { "text": str(name) , "callback_data": str(data) }
    
    def switch_inline(name , text):
        return { "text": str(name) , "switch_inline_query": str(text) }    
    
    def switch_inline_current(name , data):
        return { "text": str(name) , "switch_inline_query_current_chat": str(data) }
    
    def text(name):
        return str(name)
    
    def inline(name , data):
        return { "text": str(name) , "callback_data": str(data) }
    
    def keyboard(_dict , resize_keyboard=False , one_time_keyboard=False , input_field_placeholder=None):
        return { "keyboard": _dict , "resize_keyboard": resize_keyboard , "one_time_keyboard":one_time_keyboard , "input_field_placeholder":input_field_placeholder }
    
    def inline_keyboard(_dict):
        return {"inline_keyboard": json.dumps(_dict) }
    
    def remove_keyboard( selective=False ):
        return { "remove_keyboard": True , "selective": selective }
    
    def force_reply( input_field_placeholder=None , selective=False ):
        return { "force_reply":True , "selective": selective , "input_field_placeholder": input_field_placeholder }
    
    
def messageHandler(func , regexp = None , text = None , commands = None , types = None ):
    _dict = { "content_type": "message", "callback": func , "commands":[] , "types":[] , "regexp": None , "text":[] }
    if text is not None :
        if isinstance( text , list) == False:
            return logging.warning("pyTelegramClient : 'text' list must an array . ") 
        _dict["text"] = text
    if commands is not None :
        if isinstance( commands , list) == False:
            return logging.warning("pyTelegramClient : 'commands' list must an array . ") 
        arr = []
        for x in commands:
            _cmd = extractCommand(x)
            if _cmd is not None:
                arr.append( _cmd )
                _dict["commands"] = arr
    if types is not None:
        if isinstance( types  , list) == False:
            return logging.warning("pyTelegramClient : 'types' list must an array . ") 
        _dict["types"] = types
    return _dict




