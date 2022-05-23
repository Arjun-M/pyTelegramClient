from collections import namedtuple
import json

class User:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.id = obj.get("id")
        self.is_bot = obj.get("is_bot")
        self.first_name = obj.get("first_name")
        self.last_name = obj.get("last_name") 
        self.username = obj.get("username")
        self.language_code = obj.get("language_code") 
        self.can_join_groups = obj.get("can_join_groups") 
        self.can_read_all_group_messages = obj.get("can_read_all_group_messages") 
        self.supports_inline_queries = obj.get("supports_inline_queries") 
        
    def tuple( self ):
        return _create_tuple("User" , self.__dict__)
        
    def json( self ):
        return self.__dict__
        
class Chat:
    def __init__(self , obj):
        if obj is None:  obj = {}
        self.id = obj.get("id")
        self.type = obj.get("type")
        self.title = obj.get("title")
        self.username = obj.get("username")
        self.first_name = obj.get("first_name")
        self.last_name = obj.get("last_name")
        self.all_members_are_administrators = obj.get("all_members_are_administrators")
        self.photo = obj.get("photo")
        self.description = obj.get("description")
        self.invite_link = obj.get("invite_link")
        self.pinned_message = obj.get("pinned_message")
        self.permissions = obj.get("permissions")
        self.slow_mode_delay = obj.get("slow_mode_delay")
        self.sticker_set_name = obj.get("sticker_set_name")
        self.can_set_sticker_set = obj.get("can_set_sticker_set")
        
    def tuple( self ):
        return _create_tuple("Chat" , self.__dict__)
        
    def json( self ):
        return self.__dict__
        
class MessageEntity:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.type = obj.get("type")
        self.offset = obj.get("offset")
        self.length = obj.get("length")
        self.url = obj.get("url")
        self.language = obj.get("language")
        self.user = User(obj.get("user" , {})).tuple()
        
    def tuple( self ):
        return _create_tuple("MessageEntity" , self.__dict__)
        
class PhotoSize:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.file_id = obj.get("file_id")
        self.file_unique_id = obj.get("file_unique_id")
        self.width = obj.get("width")
        self.height = obj.get("height")
        self.file_size = obj.get("file_size")
        
    def tuple( self ):
        return _create_tuple("PhotoSize" , self.__dict__)
        
class Animation:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.file_unique_id = obj.get("file_unique_id")
        self.file_id = obj.get("file_id")
        self.width = obj.get("width")
        self.height = obj.get("height")
        self.duration = obj.get("duration")
        self.file_name = obj.get("file_name")
        self.mime_type = obj.get("mime_type")
        self.file_size = obj.get("file_size")
        self.thumb = PhotoSize( obj.get( "thumb", {} ) ).tuple()
        
    def tuple( self ):
        return _create_tuple("Animation" , self.__dict__)
        
class Audio:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.file_unique_id = obj.get("file_unique_id")
        self.file_id = obj.get("file_id")
        self.duration = obj.get("duration")
        self.performer = obj.get("performer")
        self.title = obj.get("title")
        self.file_name = obj.get("file_name")
        self.mime_type = obj.get("mime_type")
        self.file_size = obj.get("file_size")
        self.thumb = PhotoSize( obj.get("thumb",{}) ).tuple()
        
    def tuple( self ):
        return _create_tuple("Audio" , self.__dict__)
        
class Document:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.file_unique_id = obj.get("file_unique_id")
        self.file_id = obj.get("file_id")
        self.duration = obj.get("duration")
        self.file_name = obj.get("file_name")
        self.mime_type = obj.get("mime_type")
        self.file_size = obj.get("file_size")
        self.thumb = PhotoSize( obj.get( "thumb", {} ) ).tuple()
        
    def tuple( self ):
        return _create_tuple("Document" , self.__dict__)   

class Sticker:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.file_unique_id = obj.get("file_unique_id")
        self.file_id = obj.get("file_id")
        self.width = obj.get("width")
        self.height = obj.get("height")
        self.is_animated = obj.get("is_animated")
        self.file_size = obj.get("file_size")
        self.is_video = obj.get( "is_video" )
        self.emoji = obj.get("emoji")
        self.set_name = obj.get("set_name")
        self.mask_position = MaskPosition( obj.get("mask_position") ).tuple()
        self.thumb = PhotoSize( obj.get( "thumb", {} ) ).tuple()
        
    def tuple( self ):
        return _create_tuple("Sticker" , self.__dict__)   
        
class MaskPosition:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.point = obj.get("point")
        self.x_shift = obj.get("x_shift")
        self.y_shift = obj.get("y_shift")
        self.scale = obj.get("scale")
        
    def tuple( self ):
        return _create_tuple("MaskPosition" , self.__dict__)

class Video:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.file_unique_id = obj.get("file_unique_id")
        self.file_id = obj.get("file_id")
        self.width = obj.get("width")
        self.height = obj.get("height")
        self.duration = obj.get("duration")
        self.file_name = obj.get("file_name")
        self.mime_type = obj.get("mime_type")
        self.file_size = obj.get("file_size")
        self.thumb = PhotoSize( obj.get( "thumb", {} ) ).tuple()
        
    def tuple( self ):
        return _create_tuple("Video" , self.__dict__)

class VideoNote:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.file_unique_id = obj.get("file_unique_id")
        self.file_id = obj.get("file_id")
        self.length = obj.get("length")
        self.duration = obj.get("duration")
        self.file_size = obj.get("file_size")
        self.thumb = PhotoSize( obj.get( "thumb", {} ) ).tuple()
        
    def tuple( self ):
        return _create_tuple("VideoNote" , self.__dict__)

class Voice:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.file_unique_id = obj.get("file_unique_id")
        self.file_id = obj.get("file_id")
        self.duration = obj.get("duration")
        self.mime_type = obj.get("mime_type")
        self.file_size = obj.get("file_size")
        
    def tuple( self ):
        return _create_tuple("Voice" , self.__dict__)

class Contact:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.phone_number = obj.get("phone_number")
        self.first_name = obj.get("first_name")
        self.last_name = obj.get("last_name")
        self.user_id = obj.get("user_id")
        self.vcard = obj.get("vcard")
        
    def tuple( self ):
        return _create_tuple("Contact" , self.__dict__)
        
class Dice:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.emoji = obj.get("emoji")
        self.value = obj.get("value")
        
    def tuple( self ):
        return _create_tuple("Dice" , self.__dict__)

class Game:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.description = obj.get("description")
        self.title = obj.get("title")
        self.text = obj.get("text")
        self.animation = Animation( obj.get("animation") ).tuple()
        self.text_entities = []
        self.photo = []
        
        if "photo" in obj:
            for _x in obj["photo"]: self.photo.append( PhotoSize(_x).tuple() )
        if "text_entities" in obj:
            for _x in obj["text_entities"]:  self.text_entities.append( MessageEntity( _x ).tuple() )
        
    def tuple( self ):
        return _create_tuple("Game" , self.__dict__)


class PollOption:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.text = obj.get("text")
        self.voter_count = obj.get("voter_count")
        
    def tuple( self ):
        return _create_tuple("PollOption" , self.__dict__)
        
class PollAnswer:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.poll_id = obj.get("poll_id")
        self.user = User( obj.get("user") ).tuple()
        self.option_ids = obj.get("option_ids")
        
    def tuple( self ):
        return _create_tuple("PollAnswer" , self.__dict__)

class Poll:
    def __init__(self , obj):
        if obj is None : obj = {}
        self.id = obj.get("id")
        self.question = obj.get("question")
        self.options = []
        self.total_voter_count = obj.get("total_voter_count")
        self.is_closed = obj.get("is_closed")
        self.is_anonymous = obj.get("is_anonymous")
        self.type = obj.get("type")
        self.allows_multiple_answers = obj.get("allows_multiple_answers")
        self.correct_option_id = obj.get("correct_option_id")
        self.explanation = obj.get("explanation")
        self.explanation_entities = []
        self.open_period = obj.get("open_period")
        self.close_date = obj.get("close_date")
        
        if "explanation_entities" in obj:
            for x in obj["explanation_entities"]: self.explanation_entities.append( MessageEntity(x).tuple() )
        if "options" in obj:
            for x in obj["options"]: self.options.append( PollOption(x).tuple() )
            
    def tuple( self ):
        return _create_tuple("Poll" , self.__dict__)
        
class Location:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.longitude = obj.get("longitude")
        self.latitude = obj.get("latitude")
        self.horizontal_accuracy = obj.get("horizontal_accuracy")
        self.live_period = obj.get("live_period")
        self.heading = obj.get("heading")
        self.proximity_alert_radius = obj.get("proximity_alert_radius")
        
    def tuple( self ):
        return _create_tuple("Location" , self.__dict__)

class Venue:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.location = obj.get("location")
        self.title = obj.get("title")
        self.address = obj.get("address")
        self.foursquare_id = obj.get("foursquare_id")
        self.foursquare_type = obj.get("foursquare_type")
        self.google_place_id = obj.get("google_place_id")
        self.google_place_type = obj.get("google_place_type")
        
    def tuple( self ):
        return _create_tuple("Venue" , self.__dict__)

class WebAppData:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.data = obj.get("data")
        self.button_text = obj.get("button_text")
        
    def tuple( self ):
        return _create_tuple("WebAppData" , self.__dict__)
        
class ProximityAlertTriggered:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.traveler = User( obj.get("traveler") ).tuple()
        self.watcher = User( obj.get("watcher") ).tuple()
        self.distance = obj.get("distance")
        
    def tuple( self ):
        return _create_tuple("ProximityAlertTriggered" , self.__dict__)
        
class MessageAutoDeleteTimerChanged:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.message_auto_delete_time = obj.get("message_auto_delete_time")
        
    def tuple( self ):
        return _create_tuple("MessageAutoDeleteTimerChanged" , self.__dict__)

class VideoChatScheduled:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.start_date = obj.get("start_date")
        
    def tuple( self ):
        return _create_tuple("VideoChatScheduled" , self.__dict__)
        
class VideoChatEnded:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.duration = obj.get("duration")
        
    def tuple( self ):
        return _create_tuple("VideoChatEnded" , self.__dict__)
        
class VideoChatParticipantsInvited:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.users = []
        if "users" in obj:
            for x in obj["users"]: self.users.append( User( obj.get("user") ).tuple() )
        
    def tuple( self ):
        return _create_tuple("VideoChatParticipantsInvited" , self.__dict__)

class UserProfilePhotos:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.total_count = obj.get("total_count")
        self.photos = []
        if "photos" in obj:
            for x in obj["photos"]: self.photos.append(PhotoSize(x).tuple())
        
    def tuple( self ):
        return _create_tuple("UserProfilePhotos" , self.__dict__)
        
class File:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.file_id = obj.get("file_id")
        self.file_unique_id =  obj.get("file_unique_id") 
        self.file_size = obj.get("file_size")
        self.file_path = obj.get("file_path")
        
    def tuple( self ):
        return _create_tuple("File" , self.__dict__)
        
class WebAppInfo:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.url = obj.get("url")
        
    def tuple( self ):
        return _create_tuple("WebAppInfo" , self.__dict__)
        
class LoginUrl:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.url = obj.get("url")
        self.forward_text =  obj.get("forward_text") 
        self.bot_username = obj.get("bot_username")
        self.request_write_access = obj.get("request_write_access")
        
    def tuple( self ):
        return _create_tuple("LoginUrl" , self.__dict__)
        
class InlineKeyboardMarkup:
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.inline_keyboard = []
        if "inline_keyboard" in obj:
            for _x in obj["inline_keyboard"]: self.inline_keyboard.append( InlineKeyboardButton(_x).tuple() )
        
    def tuple( self ):
        return _create_tuple("InlineKeyboardMarkup" , self.__dict__)
        
class InlineKeyboardButton:  # TODO 🐈
    def __init__(self , obj):
        if obj is None:   obj = {}
        self.text = obj.get("text")
        self.url =  obj.get("url") 
        self.callback_data = obj.get("callback_data")
        self.web_app = WebAppInfo( obj.get("web_app") ).tuple()
        self.login_url = LoginUrl( obj.get("login_url") ).tuple()
        self.switch_inline_query = obj.get("switch_inline_query")
        self.switch_inline_query_current_chat = obj.get("switch_inline_query_current_chat")
        self.callback_game = obj.get("callback_game") # TODO 🐈
        self.pay = obj.get("pay")
        
    def tuple( self ):
        return _create_tuple("InlineKeyboardButton" , self.__dict__)

class Message:
    def __init__(self , update):
        self.message_id = update["message_id"]
        self.user = User( update.get("from") ).tuple()
        self.chat = Chat( update.get("chat") ).tuple()
        self.sender_chat = Chat( update.get("sender_chat") ).tuple()
        self.forward_from = User( update.get("forward_from") ).tuple()
        self.forward_from_chat = Chat( update.get("forward_from_chat") ).tuple()
        self.forward_from_message_id = update.get("forward_from_message_id")
        self.forward_signature = update.get("forward_signature")
        self.forward_sender_name = update.get("forward_sender_name")
        self.forward_date = update.get("forward_date")
        self.is_automatic_forward = update.get("is_automatic_forward")
        self.reply_to_message = None
        self.via_bot = User( update.get("via_bot") ).tuple()
        self.edit_date = update.get("edit_date")
        self.has_protected_content = update.get("has_protected_content")
        self.media_group_id = update.get("media_group_id")
        self.author_signature = update.get("author_signature")
        self.text = update.get("text")
        self.entities = []
        self.animation = Animation( update.get("animation") ) .tuple()
        self.audio = Audio( update.get("audio") ) .tuple()
        self.document = Document( update.get("document") ) .tuple()
        self.photo = [] 
        self.sticker = Sticker( update.get("sticker") ).tuple() 
        self.video = Video( update.get("video") ) .tuple()
        self.video_note = VideoNote( update.get("video_note") ).tuple()
        self.voice = Voice( update.get("voice") ).tuple()
        self.contact = Contact( update.get("contact") ).tuple()
        self.dice = Dice( update.get("dice") ).tuple()
        self.game = Game( update.get("game") ).tuple()
        self.poll = Poll( update.get("poll") ).tuple()
        self.venue = Venue( update.get("venue") ).tuple()
        self.location = Location( update.get("location") ).tuple()
        self.caption = update.get("caption")
        self.caption_entities = []
        self.left_chat_member = User( update.get("left_chat_member") ).tuple()
        self.new_chat_members = []
        self.new_chat_title = update.get("new_chat_title")
        self.new_chat_photo = []
        self.delete_chat_photo = update.get("delete_chat_photo ")
        self.group_chat_created = update.get("group_chat_created")
        self.supergroup_chat_created = update.get("supergroup_chat_created")
        self.channel_chat_created = update.get("channel_chat_created")
        self.message_auto_delete_timer_changed = MessageAutoDeleteTimerChanged( update.get("message_auto_delete_timer_changed") ).tuple()
        self.migrate_to_chat_id = update.get("migrate_to_chat_id")
        self.migrate_from_chat_id = update.get("migrate_from_chat_id")
        self.pinned_message = None
        self.invoice = update.get("invoice") # TODO 🐈
        self.successful_payment = update.get("successful_payment") # TODO 🐈
        self.connected_website = update.get("connected_website")
        self.passport_data = update.get("passport_data") # TODO 🐈
        self.proximity_alert_triggered = ProximityAlertTriggered( update.get("proximity_alert_triggered") ).tuple()
        self.video_chat_scheduled = VideoChatScheduled( update.get("video_chat_scheduled") ).tuple()
        self.video_chat_started = update.get("video_chat_started") # TODO 🐈
        self.video_chat_ended = VideoChatEnded( update.get("video_chat_ended") ).tuple()
        self.video_chat_participants_invited = VideoChatParticipantsInvited( update.get("video_chat_participants_invited") ).tuple()   
        self.web_app_data = WebAppData( update.get("web_app_data") ).tuple()
        self.reply_markup = InlineKeyboardMarkup( update.get("reply_markup") ).tuple()
        
        if "photo" in update:
            for _x in update["photo"]: self.photo.append( PhotoSize(_x).tuple() )
        if "entities" in update:
            for _x in update["entities"]:  self.entities.append( MessageEntity( _x ).tuple() )
        if "caption_entities" in update:
            for _x in update["caption_entities"]:  self.caption_entities.append( MessageEntity( _x ).tuple() )
        if "delete_chat_photo" in update:  self.delete_chat_photo = update["delete_chat_photo"]
        if "new_chat_photo" in update:  self.new_chat_photo = update["new_chat_photo"]
        if "new_chat_members" in update:  self.new_chat_members = update["new_chat_members"]
        if "pinned_message" in update:  self.pinned_message = Message( update["pinned_message"] ).tuple()
        if "reply_to_message" in update:   self.reply_to_message = Message( update["reply_to_message"] ).tuple()
        
    def tuple( self ):
        return _create_tuple("Message" , self.__dict__)

class messageHandler:
    def __init__(self , func , regexp = None , text = None , commands = None , types = None ):
        self.handler = { "func": func }
        self.type = "messageHandler"
        if regexp is not None:
            self.handler["regexp"] = regexp
        if text is not None: 
            self.handler["text"] = text
        if commands is not None: 
            self.handler["commands"] = commands
        if types is not None: 
            self.handler["types"] = types

def isCommand(text):
    if text is None: return False
    return text.startswith('/')
        
def getCommand(text):
    if text is None: return None
    return text.split()[0].split('@')[0][1:] if isCommand(text) else None

def getType(obj):
    if "photo" in obj : return "photo"
    if "text" in obj: return "text"
    if "audio" in obj : return "audio"
    if "document" in obj: return "document"
    if "animation" in obj: return "animation"
    if "game" in obj: return "game"
    if "sticker" in obj : return "sticker"
    if "poll" in obj : return "poll"
    if "video" in obj : return "video"
    if "voice" in obj: return "voice"
    if "video_note" in obj: return "video_note"
    if "contact" in obj: return "contact"
    if "dice" in obj:  return "dice" 
    if "location" in obj: return "location"
    if "venue" in obj:  return "venue"
    if "invoice" in obj:  return "invoice"
    if "via_bot"  in obj:  return "via_bot"
        
def filterCommands(cmds):
    arr = []
    for x in cmds:
        _cmd = getCommand(x)
        if _cmd is not None: arr.append( _cmd )
    return arr

def isClassHandler( _class):
    try:  
        _try = _class.type
        return True
    except: 
        return False
        
  
def _create_tuple( name , _dict ):
    _ar = []
    for x in _dict:
        _ar.append( x )
    _raw_tuple = namedtuple( name, _ar )
    _tuple = _raw_tuple(**_dict)
    return _tuple
    
def _convert_markup( _markup ):
    markup = None
    try:   
        markup = _markup.de_json()
    except:   
        if isList( _markup ): markup = json.dumps({ "inline_keyboard": _markup })
        elif isString( _markup ): markup = _markup
        elif isJson( _markup ): markup = json.dumps( _markup )
    return markup
        
def isString( _str ):
    return isinstance( _str , str )

def isJson( _dict ):
    return isinstance( _dict , dict )

def isList( _list ):
    return isinstance( _list , list )

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
