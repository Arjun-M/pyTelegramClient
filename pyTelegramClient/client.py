import json , logging , re , requests, calendar , time , datetime
from requests.sessions import Session
from .event import messageEvent , callbackQueryEvent , inlineQueryEvent
from threading import Thread , local

thread_local = local()
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

class Client:
    def __init__(self, token ):
        self.token = token
        self.answers = {}                        # { [chat_id]: <func> }
        self.message_handlers = []               # { callback: <func> , regexp:None , text:[] , commands:[] , type:[ "text" ] }
        self.edited_message_handlers = []        # { callback: <func> , regexp:None , text:[] , type:[ "text" ] }
        self.channel_post_handlers = []          # { callback: <func> } TODO : "type"
        self.edited_channel_post_handlers = []   # { callback: <func> }
        self.inline_handlers = []                # { callback: <func> , regexp:None , query:[] }
        self.chosen_inline_handlers = []         # { callback: <func> }
        self.callback_query_handlers = []        # { callback: <func> , regexp:None , data:[] }
        self.shipping_query_handlers = []        # Not interested 🤪 : TODO
        self.pre_checkout_query_handlers = []    # Not interested 🤪 : TODO
        self.poll_handlers = []                  # {}
        self.poll_answer_handlers = []           # {}
        self.my_chat_member_handlers = []        # {}
        self.chat_member_handlers = []           # {}
        self.chat_join_request_handlers = []     # {}
        self.httpError = None                    # Telegram API error catching .
        
    def new_req_thread(self):
        if not hasattr(thread_local,'session'):
            thread_local.session = requests.Session()
        return thread_local.session
    
    def _polling(self , offset , allowed_updates ):
        req = self.callApiNoLogs("getUpdates" , {"offset":offset , "allowed_updates": allowed_updates , "limit":100} )
        if req["ok"] == False:
            self.polling = False            
            logging.warning("pyTelegramClient : failed to 'getUpdates' seems this is not a valid token .")
            return False
        else:
            return req
        
    def stop(self):
        self.polling = False
    
    def polling(self , log_updates=False , drop_pending_updates=False , allowed_updates=None):
        self.polling = True
        offset = 0
        logging.warning("pyTelegramClient : started long polling .")
        self.callApiNoLogs("deleteWebhook", { "drop_pending_updates":drop_pending_updates }) # delete webhook before start polling .
        while self.polling :
            updates = self._polling(offset+1 , allowed_updates )
            if updates is False:
                break;
            if updates is not None:
                for x in updates["result"]:
                    offset = x["update_id"] 
                    self.processUpdate (x)                    
                    if log_updates is True:
                        logging.warning ( str(x) )
    
    def start(self , log_updates=False , drop_pending_updates=False , allowed_updates=None):
        return self.polling( log_updates , drop_pending_updates , allowed_updates )
    
    def launch(self , log_updates=False , drop_pending_updates=False , allowed_updates=None):
        return self.polling( log_updates , drop_pending_updates , allowed_updates )
    
    def messageHandler(self , *args, **kwargs):
        def inner(func):
            _dict = {"callback": func , "commands":[] , "types":[] , "regexp": kwargs.get('regexp', None) , "text":[] }
            if "text" in kwargs:
                if isinstance( kwargs["text"] , list) == False:
                    return logging.warning("pyTelegramClient : 'text' list must an array . ") 
                _dict["text"] = kwargs["text"]
            if "commands" in kwargs:
                if isinstance( kwargs["commands"] , list) == False:
                    return logging.warning("pyTelegramClient : 'commands' list must an array . ") 
                arr = []
                for x in kwargs["commands"]:
                    _cmd = self.extractCommand(x)
                    if _cmd is not None:                        
                        arr.append( _cmd )
                _dict["commands"] = arr
            if "types" in kwargs:
                if isinstance( kwargs["types"]  , list) == False:
                    return logging.warning("pyTelegramClient : 'types' list must an array . ") 
                _dict["types"] = kwargs["types"]            
            self.message_handlers.append(_dict)
        return inner
    
    def callbackQueryHandler(self , *args, **kwargs):
        def inner(func):
            _dict = {"callback": func , "regexp": None , "data":[] }
            if "regexp"in kwargs:
                _dict["regexp"] = kwargs["regexp"]
            if "data" in kwargs :
                if isinstance( kwargs["data"] , list) == False:
                    return logging.warning("pyTelegramClient : 'query' list must an array . ") 
                _dict["data"] = kwargs["data"]
            self.callback_query_handlers.append(_dict)
            logging.warning("pyTelegramClient : registered new callback_query handler . ")
        return inner
    
    def channelPostHandler(self , *args, **kwargs):
        def inner(func):
            _dict = {"callback": func }
            self.channel_post_handlers.append( _dict )
        return inner
    
    def choosenInlineResultHandler(self , *args, **kwargs):
        def inner(func):
            _dict = {"callback": func }
            self.chosen_inline_handlers.append( _dict )
        return inner
    
    def editChannelPostHandler(self , *args, **kwargs):
        def inner(func):
            _dict = {"callback": func }
            self.edited_channel_post_handlers.append( _dict )
        return inner
    
    def inlineHandler(self , *args, **kwargs):
        def inner(func):
            _dict = {"callback": func , "regexp": None , "query":[] }
            if "regexp"in kwargs:
                _dict["regexp"] = kwargs["regexp"]
            if "query" in kwargs :
                if isinstance( kwargs["query"] , list) == False:
                    return logging.warning("pyTelegramClient : 'query' list must an array . ") 
                _dict["query"] = kwargs["query"]
            self.inline_handlers.append(_dict)
        return inner
    
    def editMessageHandler(self , *args, **kwargs):
        def inner(func):
            _dict = {"callback": func , "commands":[] , "types":[] , "regexp": None , "text":[] }
            if "types" in kwargs :
                if isinstance( kwargs["types"] , list) == False:
                    return logging.warning("pyTelegramClient : 'types' list must an array . ") 
                _dict["types"] = kwargs["types"]
            if "regexp" in kwargs:
                _dict["regexp"] = kwargs["regexp"] 
            if "text" in kwargs:
                if isinstance( kwargs["text"] , list) == False:
                    return logging.warning("pyTelegramClient : 'text' list must an array . ") 
                _dict["text"] = kwargs["text"]
            self.edited_message_handlers.append(_dict)
        return inner
    
    def onClientError(self , *args, **kwargs):
        def inner(func):
            self.httpError = func
        return inner
    
    def processUpdate(self , req ):
        if "message" in req :
            update = self.parseMessage( req["message"] )
            return self._notify_message( update )
        if "inline_query" in req:
            update = self.parseInlineQuery( req["inline_query"] )
            return self._notify_inline( update )
        if "callback_query" in req:
            update = self.parseCallbackData( req["callback_query"] )
            return self._notify_callback( update )
        if "edited_message" in req:
            update = self.parseMessage( req["edited_message"] )
            return self._notify_edit_message( update )
        if "channel_post" in req:
            update = self.parseMessage( req["channel_post"] )
            return self._notify_channel_post( update )
        if "edited_channel_post" in req:
            update = self.parseMessage( req["edited_channel_post"] )
            return self._notify_edit_channel_post( update )
        if "chosen_inline_result" in req:
            update = self.parseChoosenInlineResult( req[ "chosen_inline_result" ] )
            return self._notify_chosen_inline( update )
        if "poll" in req:
            update = self.parsePoll( req["poll"] )
            return self._notify_poll( update )
        if "poll_answer" in req:
            update = self.parsePollAnswer( req["poll_answer"] )
            return self._notify_poll_answers(update)
    
    # Re write !!!!!!!
    def _notify_inline(self , update):
        q = update.get("query", None)
        event = inlineQueryEvent(update)
        for x in self.inline_handlers:
            if x["regexp"] is not None and q is not None:
                r = re.search( x["regexp"] , str(q))
                if r :
                    return _emit_callback(x["callback"] , event )   
            if len(x["query"]) > 0:
                if q in x["query"]:
                    return _emit_callback(x["callback"] , event ) 
    
    def _notify_channel_post(self , update):
        event = messageEvent( self , update ) # TODO : add channel post event .
        for x in self.channel_post_handlers:
            return _emit_callback(x["callback"] , event )   
    
    def _notify_poll(self , update):
        event = messageEvent( self , update ) # TODO : add poll event .
        """for x in self.channel_post_handlers:
            return x["callback"]( event )"""
    
    def _notify_poll_answers(self , update):
        event = messageEvent( self , update ) # TODO : add poll answer event .
        """for x in self.channel_post_handlers:
            return x["callback"]( event )"""
    
    def _notify_chosen_inline(self , update):
        event = messageEvent( self , update ) # TODO : add choosen inline post event .
        for x in self.chosen_inline_handlers:
            return _emit_callback(x["callback"] , event )   
        
    def _notify_edit_channel_post(self , update):
        event = messageEvent( self , update ) # TODO : add edit channel post event .
        for x in self.edited_channel_post_handlers:
            return _emit_callback(x["callback"] , event )
    
    def _notify_edit_message(self , update):
        text = update.get("text")
        event = messageEvent( self , update )
        for x in self.edited_message_handlers:
            if len(x["text"]) > 0:
                if text in x["text"]:
                    return _emit_callback(x["callback"] , event )
            if x["regexp"] is not None and text is not None:
                r = re.search( x["regexp"] , str(text))
                if r :
                    return _emit_callback(x["callback"] , event )   
            type = self.getType( update )                
            if type in x["types"]:
                return _emit_callback(x["callback"] , event )         
    
    def _notify_callback(self , update):
        data = update.get("data", None)
        event = callbackQueryEvent(self , update)
        for x in self.callback_query_handlers:
            if x["regexp"] is not None and data is not None:
                r = re.search( x["regexp"] , str( data ))
                if r :
                    return _emit_callback(x["callback"] , event )
            if len(x["data"]) > 0:
                if q in x["data"]:
                    return _emit_callback(x["callback"] , event ) 
    
    def _notify_message(self , update):
        text = update.get("text", None)
        event = messageEvent( self , update )
        chat = update.get("chat").get("id")
        for x in self.message_handlers:
            if chat in self.answers:
                return _emit_callback( self.answers[chat] , event)
            if len(x["text"]) > 0:
                if text in x["text"]:
                    return _emit_callback(x["callback"] , event ) 
            if x["regexp"] is not None and text is not None:
                r = re.search( x["regexp"] , str(text))
                if r :
                    return _emit_callback(x["callback"] , event ) 
            if len(x["commands"]) > 0:
                cmd = self.extractCommand(text)
                if cmd in x["commands"]:
                    return _emit_callback(x["callback"] , event )
            type = self.getType(update )                                
            if type in x["types"]:
                return _emit_callback(x["callback"] , event )      
            
    def _notify_api_error(self , files=None , payload=None , method=None , data=None ):
        GMT = time.gmtime()
       _dict = { "method": method, "payload": payload, "has_file": False , "error": data , "string": "Telegram API returned "+str(data), "time": calendar.timegm(GMT) }
        if files is not None:
            _dict["has_file"] = True
        if self.httpError is not None:
            return self.httpError(_dict)
        raise Exception ( "Telegram API returned "+str(_dict)+" ." )        
        
    def _emit_callback(self , callback , event):
        return callback( event )
    
    def addMessageListner(self , chat , func):
        self.answers[chat] = func
        return True
    
    def removeMessageListner(self , chat ):
        if chat in self.answers:
            del self.answers[chat]
        return True  
    
    def is_command(self , text):
        if text is None: 
            return False
        return text.startswith('/')
    
    def extractCommand(self , text):
        if text is None: 
            return None
        return text.split()[0].split('@')[0][1:] if self.is_command(text) else None
    
    def callApi(self , method ,  params={} ,  files=None):
        data = self.new_req_thread().post ( f"https://api.telegram.org/bot{self.token}/{method}" , data = params , files = files  )
        result = self._result(data ,method , files , params )
        return result
        
    def callApiNoLogs(self , method ,  params={} ,  files=None):
        data = self.new_req_thread().post ( f"https://api.telegram.org/bot{self.token}/{method}" , data = params , files = files  ).json()
        return data
    
    def _result(self, data , method , files , params ):
        try:
            result = data.json()
        except:
            if data.status_code != 200:
                self._notify_api_error( method=method , files=files , payload=params , data= "Server returned an invalid HTTP status code , {}".format(data.status_code) )                 
            else:
                self._notify_api_error( method=method , files=files , payload=params , data= "Server returned an invalid JSON response , ") 
        else:
            if result['ok'] == False:
                self._notify_api_error( method=method , files=files , payload=params , data= result )           
            return result

    
    def getType(self , obj):
        if obj.get("photo") is not None:
            return "photo"
        if obj.get("text") is not None:
            return "text"
        if obj.get("audio") is not None:
            return "audio"
        if obj.get("document") is not None:
            return "document"
        if obj.get("animation") is not None:
            return "animation"
        if obj.get( "game" ) is not None:
            return "game"
        if obj.get("sticker") is not None:
            return "sticker"
        if obj.get("poll") is not None:
            return "poll"
        if obj.get( "video" ) is not None:
            return "video"
        if obj.get( "voice" ) is not None:
            return "voice"
        if obj.get( "video_note" ) is not None:
            return "video_note"
        if obj.get( "contact" ) is not None:
            return "contact"
        if obj.get( "dice" ) is not None:
            return "dice"        
        if obj.get("location") is not None:
            return "location"
        if obj.get("venue") is not None:
            return "venue"
        if obj.get( "invoice" ) is not None:
            return "invoice"
        if obj.get( "via_bot" ) is not None:
            return "via_bot"
        
    
    
    
    
    
    def parseUserDict(self , obj):
        _dict = {
            "id": obj.get("id"),
            "is_bot": obj.get("is_bot"),
            "first_name": obj.get("first_name"),
            "last_name":obj.get("last_name") , 
            "username":obj.get("username"), 
            "language_code":obj.get("language_code") , 
            "can_join_groups":obj.get("can_join_groups") ,
            "can_read_all_group_messages" :obj.get("can_read_all_group_messages") ,
            "supports_inline_queries":obj.get("supports_inline_queries") 
        }
        return _dict
    
    def parseChatDict(self , obj):
        _dict =  { 
            "id": obj["id"],
            "type": obj.get("type"),
            "title": obj.get("title"),
            "username": obj.get("username"),
            "first_name": obj.get("first_name"),
            "last_name": obj.get("last_name"),
            "all_members_are_administrators": obj.get("all_members_are_administrators"),
            "photo": obj.get("photo"),
            "description": obj.get("description"),
            "invite_link": obj.get("invite_link"),
            "pinned_message": obj.get("pinned_message"),
            "permissions": obj.get("permissions"),
            "slow_mode_delay": obj.get("slow_mode_delay"),
            "sticker_set_name": obj.get("sticker_set_name"),
            "can_set_sticker_set": obj.get("can_set_sticker_set")
        }
        return _dict
    
    def parseMessage(self , obj):
        opts = {
            "message_id": obj["message_id"] , "user": {} , "sender_chat": None ,"chat":{} ,"forward_from": None , "forward_from_chat": None, "forward_from_message_id": None, "forward_signature": None, "forward_sender_name": None, "forward_date": None, "reply_to_message": None,"via_bot": None, "edit_date": None, "media_group_id": None, "author_signature": None, "text": None , "entities": [], "caption_entities": [], "audio": None, "document": None,  "animation": None, "game": None, "photo": None , "sticker": None, "video": None, "voice": None,  "video_note": None, "caption": None, "contact": None, "dice": None,
            "location": None, "venue": None, "poll": None, "new_chat_members": None , "left_chat_member": None, "new_chat_title": None, "new_chat_photo": None , "delete_chat_photo": None, "group_chat_created": None, "supergroup_chat_created": None, "channel_chat_created": None, "message_auto_delete_timer_changed": None,"migrate_to_chat_id": None, "migrate_from_chat_id": None, "pinned_message": None, "invoice": None, "successful_payment": None, "connected_website": None, "passport_data": None, "proximity_alert_triggered": None, "voice_chat_started": None, "voice_chat_ended": None, "voice_chat_participants_invited": None, "reply_markup": None
        }    
        if "from" in obj:
            opts["user"] = self.parseUserDict( obj["from"] )
        if "chat" in obj:
            opts["chat"] = self.parseChatDict( obj["chat"] )
        if "sender_chat" in obj :
            opts["sender_chat"] = self.parseChatDict( obj["sender_chat"] )
        if "forward_from" in obj:
            opts["forward_from"] = self.parseUserDict(obj["forward_from"])
        if "forward_from_chat" in obj:
            opts["forward_from_chat"] = self.parseChatDict( obj["forward_from_chat"] )
        if "forward_from_message_id" in obj:
            opts["forward_from_message_id"] = obj["forward_from_message_id"]
        if "forward_from_message_id" in obj:
            opts["forward_from_message_id"] = obj.get("forward_from_message_id")
        if "forward_signature" in obj:
            opts["forward_signature"] = obj.get("forward_signature")
        if "forward_sender_name" in obj:
            opts["forward_sender_name"] = obj.get("forward_sender_name")
        if "forward_date" in obj:
            opts["forward_date"] = obj.get("forward_date")
        if "is_automatic_forward" in obj:
            opts["is_automatic_forward"] = obj.get("is_automatic_forward")
        if "reply_to_message" in obj:
            opts["reply_to_message"] = obj["reply_to_message"] 
        if "via_bot" in obj:
            opts["via_bot"] = obj["via_bot"]     
        if "has_protected_content" in obj:
            opts["has_protected_content"] = obj.get("has_protected_content")
        if "media_group_id" in obj:
            opts["media_group_id"] = obj.get("media_group_id")
        if "author_signature" in obj:
            opts["author_signature"] = obj.get("author_signature")
        if "entities" in obj:
            opts["entities"] = obj["entities"]
        if "caption_entities" in obj:
            opts["caption_entities"] = obj["caption_entities"]
        if "text" in obj:
            opts["text"] = obj["text"]
        if "audio" in obj:
            opts["audio"] = obj["audio"]
        if "document" in obj:
            opts["document"] = obj["document"]
        if "animation" in obj:
            opts["animation"] = obj["animation"]
        if "game" in obj:
            opts["game"] = obj["game"]
        if "photo" in obj:
            opts["photo"] = obj["photo"]
        if "sticker" in obj:
            opts["sticker"] = obj["sticker"]
        if "video" in obj:
            opts["video"] = obj["video"]
        if "video_note" in obj:
            opts["video_note"] = obj["video_note"]
        if "voice" in obj:
            opts["voice"] = obj["voice"]
        if "caption" in obj:
            opts["caption"] = obj["caption"]
        if "contact" in obj:
            opts["contact"] = obj["contact"]
        if "location" in obj:
            opts["location"] = obj["location"]
        if "venue" in obj:
            opts["venue"] = obj["venue"]
        if "dice" in obj:
            opts["dice"] = obj["dice"]
        if "new_chat_members" in obj:
            opts["new_new_chat_members"] = obj["new_chat_members"]
        if "left_chat_member" in obj:
            opts["left_chat_member"] = self.parseUserDict(obj["left_chat_member"])
        if "new_chat_title" in obj:
            opts["new_chat_title"] = obj["new_chat_title"]
        if "new_chat_photo" in obj:
            opts["new_chat_photo"] = obj["new_chat_photo"]
        if "delete_chat_photo" in obj:
            opts["delete_chat_photo"] = obj["delete_chat_photo"]
        if "group_chat_created" in obj:
            opts["group_chat_created"] = obj["group_chat_created"]
        if "supergroup_chat_created" in obj:
            opts["supergroup_chat_created"] = obj["supergroup_chat_created"]
        if "channel_chat_created" in obj:
            opts["channel_chat_created"] = obj["channel_chat_created"]
        if "migrate_to_chat_id" in obj:
            opts["migrate_to_chat_id"] = obj["migrate_to_chat_id"]
        if "migrate_from_chat_id" in obj:
            opts["migrate_from_chat_id"] = obj["migrate_from_chat_id"]
        if "pinned_message" in obj:
            opts["pinned_message"] = obj["pinned_message"]
        if "invoice" in obj:
            opts["invoice"] = obj["invoice"]
        if "successful_payment" in obj:
            opts["successful_payment"] = obj["successful_payment"]
        if "connected_website" in obj:
            opts["connected_website"] = obj["connected_website"]
        if "poll" in obj:
            opts["poll"] = obj["poll"]
        if "passport_data" in obj:
            opts["passport_data"] = obj["passport_data"]
        if "proximity_alert_triggered" in obj:
            opts["proximity_alert_triggered"] = obj["proximity_alert_triggered"]
        if "voice_chat_scheduled" in obj:
            opts["voice_chat_scheduled"] = obj["voice_chat_scheduled"]
        if "voice_chat_started" in obj:
            opts["voice_chat_started"] = obj["voice_chat_started"]   
        if "voice_chat_ended" in obj:
            opts["voice_chat_ended"] = obj["voice_chat_ended"]
        if "voice_chat_participants_invited" in obj:
            opts["voice_chat_participants_invited"] = obj["voice_chat_participants_invited"]
        if "message_auto_delete_timer_changed" in obj:
            opts["message_auto_delete_timer_changed"] = obj["message_auto_delete_timer_changed"]
        if "date" in obj:
            opts["date"] = obj["date"]
        if "reply_markup" in obj:
            opts["reply_markup"] = obj["reply_markup"]
        if "edit_date" in obj:
            opts["edit_date"] = obj.get("edit_date")
        return opts 
    
    def parseInlineQuery(self , obj):
        opts = {
            "id": obj["id"] , "user": { },"location": None , "query": "", "chat_type":None , "offset":None
        }
        if "from" in obj:
            opts["user"] = self.parseUserDict( obj["from"] )
        if "offset" in obj:
            opts["offset"] = obj["offset"]
        if "location" in obj:
            opts["location"] = obj["location"]
        if "chat_type" in obj:
            opts["chat_type"] = obj["chat_type"]
        if "query" in obj:
            opts["query"] = obj["query"]
        return opts
    
    def parseCallbackData(self , obj):
        opts = {
            "id" : obj["id"] , "user":{} , "message":{} ,  "inline_message_id": None , "chat_instance": None , "data":None , "game_short_name":None
        }
        if "from" in obj:
            opts["user"] = self.parseUserDict( obj["from"] )
        if "message" in obj:
            opts["message"]  = self.parseMessage( obj["message"] )
        if "data" in obj:
            opts["data"] = obj["data"]
        if "inline_message_id" in obj:
            opts["inline_message_id"] = obj["inline_message_id"]
        if "data" in obj:
            opts["data"] = obj["data"]
        if "chat_instance" in obj:
            opts["chat_instance"] = obj["chat_instance"]
        if "game_short_name" in obj:
            opts["game_short_name"] = obj["game_short_name"]
        return opts
    
    def parseChoosenInlineResult(self , obj):
        opts = {
            "result_id":None , "user":{} , "location":None , "inline_message_id":None , "query":None
        }
        if "result_id" in obj:
            opts["result_id"] = obj["result_id"]
        if "from" in obj:
            opts["user"] = self.parseUserDict( obj["from"] )
        if "location" in obj:
            opts["location"] = obj["location"]
        if "inline_message_id" in obj:
            opts["inline_message_id"] = obj["inline_message_id"]
        if "query" in obj:
            opts["query"] = obj["query"]
        return opts
    
    def parsePoll(self , obj):
        opts = {
            "id": None , "question": None ,"options":None , "total_voter_count":None , "is_closed":None , "is_anonymous":None , "type":None ,"allows_multiple_answers":None , "correct_option_id":None , "explanation":None , "explanation_entities":None , "open_period":None , "close_date":None
        }
        if "id" in obj:
            opts["id"] = obj["id"]
        if "question" in obj:
            opts["question"] = obj["question"]
        if "options" in obj:
            opts["options"] = obj["options"]
        if "total_voter_count" in obj:
            opts["total_voter_count"] = obj["total_voter_count"]
        if "is_closed" in obj:
            opts["is_closed"] = obj["is_closed"]
        if "is_anonymous" in obj:
            opts["is_anonymous"] = obj["is_anonymous"]
        if "type" in obj:
            opts["type"] = obj["type"]
        if "allows_multiple_answers" in obj:
            opts["allows_multiple_answers"] = obj["allows_multiple_answers"]
        if "correct_option_id" in obj:
            opts["correct_option_id"] = obj["correct_option_id"]
        if "explanation" in obj:
            opts["explanation"] = obj["explanation"]
        if "explanation_entities" in obj:
            opts["explanation_entities"] = obj["explanation_entities"]
        if "open_period" in obj:
            opts["open_period"] = obj["open_period"]
        if "close_date" in obj:
            opts["close_date"] = obj["close_date"]
        return opts
    
    def parsePollAnswer(self , obj):
        opts ={
            "poll_id":None , "user": None , "option_ids":None
        }
        if "poll_id" in obj:
            opts["poll_id"] = obj["poll_id"]
        if "option_ids" in obj:
            opts["option_ids"] = obj["option_ids"]
        if "user" in obj:
            opts["user"] = self.parseUserDict( obj["user"] ) 
        return opts
            
            
