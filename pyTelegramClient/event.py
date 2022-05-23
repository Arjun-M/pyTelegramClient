from .telegram import Telegram
from .types import User , Chat , Message , Video , Document , Audio , Animation , PhotoSize , MessageEntity , PhotoSize , Animation , Audio , Document , Sticker , MaskPosition , Video , VideoNote , Voice , Contact , Dice , Game , PollOption , PollAnswer , Poll , Location, Venue,  WebAppData , ProximityAlertTriggered , MessageAutoDeleteTimerChanged , VideoChatScheduled , VideoChatEnded , VideoChatParticipantsInvited  , UserProfilePhotos , WebAppInfo , LoginUrl , InlineKeyboardMarkup , InlineKeyboardButton , Message    

class messageEvent:
    def __init__(self , client , update):
        self._client = client
        self.telegram = Telegram( client = client )
        self.update = update
        self.id = update["message_id"]
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
        self.video_chat_started = update.get("video_chat_started") 
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

    def respond(self , text , reply=False , disable_web_page_preview=None , reply_markup=None , disable_notification=None, entities=None , parse_mode=None , protect_content=None):
        """
        : Mirror Extension of "client.telegram.sendMessage()"
        """
        payload = {'chat_id': self.chat.id , 'text': text , 'allow_sending_without_reply':True}
        if reply == True :
            payload['reply_to_message_id'] = self.message_id
        if disable_web_page_preview is not None:
            payload['disable_web_page_preview'] = disable_web_page_preview
        if reply_markup:
            payload['reply_markup'] = reply_markup
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if entities:
            payload['entities'] = entities 
        if protect_content is not None:
            payload['protect_content'] = protect_content
        return self._client.callApi("sendMessage" , payload )
        
    def typing(self ):
        """
        : Mirror Extension of "client.telegram.sendChatAction()"
        """
        payload = {'chat_id': self.chat.id , 'action': "typing"}
        return self._client.callApi( "sendChatAction" , payload )
        
    def delete(self):
        """
        : Mirror Extension of "client.telegram.deleteMessage()"
        """
        payload = { "chat_id": self.chat.id , "message_id": self.message_id }
        return self._client.callApi("deleteMessage" , payload )
    
