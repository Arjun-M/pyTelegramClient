import json , requests , asyncio , logging


logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

class createConnection:
    def __init__(self, client ):
        self.client = client
            
    def sendMessage(self , chat_id , text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, entities=None, allow_sending_without_reply=None, protect_content=None):
        payload = {'chat_id': str(chat_id), 'text': text}
        if disable_web_page_preview is not None:
            payload['disable_web_page_preview'] = disable_web_page_preview
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = _convert_markup(reply_markup)
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if entities:
            payload['entities'] = entities 
        if allow_sending_without_reply is not None:
            payload['allow_sending_without_reply'] = allow_sending_without_reply
        if protect_content is not None:
            payload['protect_content'] = protect_content
        return self.client.callApi("sendMessage" , payload )
    
    def deleteWebhook(self , drop_pending_updates=None ):
        payload = {}
        if drop_pending_updates is not None:  
            payload['drop_pending_updates'] = drop_pending_updates
        return self.client.callApi("deleteWebhook" , payload )
    
    def getWebhookInfo(self):
        return self.client.callApi("getWebhookInfo" , {} )
    
    def getUpdates(self , offset=None, limit=None, allowed_updates=None ):
        payload = {}
        if offset:
            payload['offset'] = offset
        if limit:
            payload['limit'] = limit
        if allowed_updates is not None:
            payload['allowed_updates'] = allowed_updates
        return self.client.callApi("getUpdates" , payload )
    
    def getUserProfilePhotos(token, user_id, offset=None, limit=None):
        payload = {'user_id': user_id}
        if offset:
            payload['offset'] = offset
        if limit:
            payload['limit'] = limit
        return self.client.callApi("getUserProfilePhotos" , {} )

    def getChat(self , chat_id):
        payload = {"chat_id":chat_id}
        return self.client.callApi("getChat" , payload )
    
    def setWebhook(self , url , certificate=None, max_connections=None, allowed_updates=None, ip_address=None, drop_pending_updates = None):
        payload = { 'url': url }
        files = None # set default .
        if certificate:
            files = {'certificate': certificate}
        if max_connections:
            payload['max_connections'] = max_connections
        if allowed_updates is not None: 
            payload['allowed_updates'] = allowed_updates
        if ip_address is not None:
            payload['ip_address'] = ip_address
        if drop_pending_updates is not None: 
            payload['drop_pending_updates'] = drop_pending_updates
        return self.client.callApi("setWebhook" , payload, files=files)

    def forwardMessage(self , chat_id, from_chat_id, message_id, disable_notification=None, protect_content=None):
        payload = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if protect_content is not None:
            payload['protect_content'] = protect_content
        return self.client.callApi("forwardMessage", payload)
    
    def copyMessage(self , chat_id, from_chat_id, message_id, caption=None, parse_mode=None, caption_entities=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None, protect_content=None):
        payload = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
        if caption is not None:
            payload['caption'] = caption
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if caption_entities is not None:
            payload['caption_entities'] = caption_entities
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            payload['reply_markup'] = reply_markup
        if allow_sending_without_reply is not None:
            payload['allow_sending_without_reply'] = allow_sending_without_reply    
        if protect_content is not None:
            payload['protect_content'] = protect_content
        return self.client.callApi("copyMessage" , payload)
    
    def sendDice( self, chat_id, emoji=None, disable_notification=None, reply_to_message_id=None, reply_markup=None, allow_sending_without_reply=None, protect_content=None):
        payload = {'chat_id': chat_id}
        if emoji:
            payload['emoji'] = emoji
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = reply_markup
        if allow_sending_without_reply is not None:
            payload['allow_sending_without_reply'] = allow_sending_without_reply
        if protect_content is not None:
            payload['protect_content'] = protect_content
        return self.client.callApi( "sendDice" , payload)
    
    def sendPhoto( self, chat_id, photo,  caption=None, reply_to_message_id=None, reply_markup=None,  parse_mode=None, disable_notification=None, caption_entities=None, allow_sending_without_reply=None, protect_content=None):
        payload = {'chat_id': chat_id}
        files = None # set default . 
        if isinstance(photo, str):
            payload['photo'] = photo
        else:
            files = {'photo': photo}
        if caption:
            payload['caption'] = caption
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = reply_markup
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if caption_entities:
            payload['caption_entities'] = caption_entities 
        if allow_sending_without_reply is not None:
            payload['allow_sending_without_reply'] = allow_sending_without_reply
        if protect_content is not None:
            payload['protect_content'] = protect_content
        return self.client.callApi( "sendPhoto" , payload, files=files )
    

    
    
    
    
