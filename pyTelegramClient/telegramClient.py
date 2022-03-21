import requests , json , logging , re


logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

class TelegramClient:
    def __init__(self, token ):
        self.token = token
        self.message_handlers = []               # { callback: <func> , regexp:None , text:[] , commands:[] , type:[ "text" ] }
        self.edited_message_handlers = []        # 
        self.channel_post_handlers = []          #
        self.edited_channel_post_handlers = []   #
        self.inline_handlers = []                # { callback: <func> , regexp:None , query:[] }
        self.chosen_inline_handlers = []         #
        self.callback_query_handlers = []        # { callback: <func> , regexp:None , data:[] }
        self.shipping_query_handlers = []
        self.pre_checkout_query_handlers = []
        self.poll_handlers = []
        self.poll_answer_handlers = []
        self.my_chat_member_handlers = []
        self.chat_member_handlers = []
        self.chat_join_request_handlers = []    
    
    
    def _polling(self , offset):
        req = self.callApi("getUpdates" , {"offset":offset} )
        if req["ok"] == False:
            self.polling = False            
            logging.warning("pyTelegramClient : check bot token and try again .")
            return None
        else:
            return req
        
    def start_polling(self):
        self.polling = True
        offset = 0
        logging.warning("worker : pyTelegramClient has started polling .")
        while self.polling :
            updates = self._polling(offset+1)
            if updates is not None:
                for x in updates["result"]:
                    offset = x["update_id"] 
                    self.processUpdate (x)
    
    
    """
    ====×  REQUEST HANDLER { 1 }  ×====
    """
    
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
            logging.warning("pyTelegramClient : registered new message handler . ")          
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
            logging.warning("pyTelegramClient : registered new message handler . ")
        return inner
    
    """
    ====×  REQUEST HANDLER { 2 }  ×====
    """
    
    def addMessageHandler(self , callback=None , commands= None , types= None , regexp= [], text= None ):
        if callback is None:
            return logging.warning("pyTelegramClient : callback function not found !. ") 
        _dict = {"callback": callback , "commands":[] , "types":[] , "regexp": None , "text":[] }
        if commands:
            if isinstance( commands , list) == False:
                return logging.warning("pyTelegramClient : 'commands' list must an array . ") 
            arr = []
            for x in commands:
                _cmd = self.extractCommand(x)
                if _cmd is not None:
                    arr.append( _cmd )
            _dict["commands"] = arr
        if types:
            if isinstance( types  , list) == False:
                return logging.warning("pyTelegramClient : 'types' list must an array . ") 
            _dict["types"] = types
        if regexp:
            _dict["regexp"] = regexp 
        if text:
            if isinstance( text , list) == False:
                return logging.warning("pyTelegramClient : 'text' list must an array . ") 
            _dict["text"] = text
        self.inline_handlers.append(_dict)
        logging.warning("pyTelegramClient : registered new message handler . ")
        return True            
    
    def addInlineHandler(self , callback=None , regexp=None , query=None ):
        if callback is None:
            return logging.warning("pyTelegramClient : callback function not found !. ") 
        _dict = {"callback": callback , "regexp": None , "query":[] }
        if regexp:
            _dict["regexp"] = regexp
        if query:
            if isinstance( query , list) == False:
                return logging.warning("pyTelegramClient : 'query' list must an array . ") 
            _dict["query"] = query
        self.inline_handlers.append(_dict)
        logging.warning("pyTelegramClient : registered new message handler . ")
        return True    
    
    """
    ====×  MESSAGE PROCESSOR & NOTIFIER  ×====
    """
    
    def processUpdate(self , req ):
        if "message" in req :
            update = self.parseMessage( req["message"] )
            return self._notify_message(update)
        if "inline_query" in req:
            update = self.parseInlineQuery( req["inline_query"] )
            return self._notify_inline(update)
    
    def _notify_inline(self , update):
        q = update.get("query", "None")
        for x in self.inline_handlers:
            if x["regexp"] is not None:
                r = re.search( x["regexp"] , str(q))
                if r :
                    return x["callback"]( update )
            if len(x["query"]) > 0:
                if q in x["query"]:
                    return x["callback"]( update ) 
    
    def _notify_message(self , update):
        text = update.get("text", "None")
        for x in self.message_handlers:
            if len(x["text"]) > 0:
                if text in x["text"]:
                    return x["callback"]( update ) 
            if x["regexp"] is not None:
                r = re.search( x["regexp"] , str(text))
                if r :
                    return x["callback"]( update )
            if len(x["commands"]) > 0:
                cmd = self.extractCommand(text)
                if cmd in x["commands"]:
                    return x["callback"]( update )
            if "text" in x["types"]:
                return x["callback"]( update )
    
    """
    ====×  UTILS  ×====
    """
    
    def is_command(self , text):
        if text is None: 
            return False
        return text.startswith('/')
    
    def extractCommand(self , text):
        if text is None: 
            return None
        return text.split()[0].split('@')[0][1:] if self.is_command(text) else None
    
    def callApi(self , method ,  params={} ,  files=None):
        data = requests.post ( f"https://api.telegram.org/bot{self.token}/{method}" , data = params , files = files  )
        return data.json()
    
    """
    ====×  REQUEST PARSERS  ×====
    """
    
    def parseUserDict(self , obj):
        _dict = {
            "id": obj["id"],
            "is_bot": obj.get("is_bot"),
            "first_name": obj["first_name"],
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
                
        
        
    
    
