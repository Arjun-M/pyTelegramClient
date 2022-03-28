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
            payload['reply_markup'] = reply_markup
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
    
    def getMe(self):
        return self.client.callApi("getMe" , {} )
    
    def logOut(self):
        return self.client.callApi("logOut" , {} )      
    
    def close(self):
        return self.client.callApi("close" , {} )
    
    def getFile(self , file_id):
        payload = {"file_id":file_id}
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
            if photo.startswith("./"):
                files = {'photo': open(photo, "rb")}
            else:
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
    
    def sendLocation (self , chat_id, latitude, longitude, live_period=None, reply_to_message_id=None, reply_markup=None, disable_notification=None, horizontal_accuracy=None, heading=None, proximity_alert_radius=None, allow_sending_without_reply=None, protect_content=None):
        payload = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}
        if live_period:
            payload['live_period'] = live_period
        if horizontal_accuracy:
            payload['horizontal_accuracy'] = horizontal_accuracy
        if heading:
            payload['heading'] = heading
        if proximity_alert_radius:
            payload['proximity_alert_radius'] = proximity_alert_radius
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if allow_sending_without_reply is not None:
            payload['allow_sending_without_reply'] = allow_sending_without_reply
        if reply_markup:
            payload['reply_markup'] = reply_markup
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if protect_content is not None:
            payload['protect_content'] = protect_content
        return self.client.callApi( "sendLocation" , payload )
    
    def stopMessageLiveLocation(self , chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        payload = {}
        if chat_id:
            payload['chat_id'] = chat_id
        if message_id:
            payload['message_id'] = message_id
        if inline_message_id:
            payload['inline_message_id'] = inline_message_id
        if reply_markup:
            payload['reply_markup'] = reply_markup
        return self.client.callApi( "stopMessageLiveLocation" , payload )
    
    def editMessageLiveLocation( self , latitude, longitude, chat_id=None, message_id=None,  inline_message_id=None, reply_markup=None, horizontal_accuracy=None, heading=None, proximity_alert_radius=None):
        payload = {'latitude': latitude, 'longitude': longitude}
        if chat_id:
            payload['chat_id'] = chat_id
        if message_id:
            payload['message_id'] = message_id
        if horizontal_accuracy:
            payload['horizontal_accuracy'] = horizontal_accuracy
        if heading:
            payload['heading'] = heading
        if proximity_alert_radius:
            payload['proximity_alert_radius'] = proximity_alert_radius
        if inline_message_id:
            payload['inline_message_id'] = inline_message_id
        if reply_markup:
            payload['reply_markup'] = reply_markup
        return self.client.callApi( "editMessageLiveLocation" , payload )
        
    def sendContact(self , chat_id, phone_number, first_name, last_name=None, vcard=None, disable_notification=None, reply_to_message_id=None, reply_markup=None, allow_sending_without_reply=None, protect_content=None):
        payload = {'chat_id': chat_id, 'phone_number': phone_number, 'first_name': first_name}
        if last_name:
            payload['last_name'] = last_name
        if vcard:
            payload['vcard'] = vcard
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
        return self.client.callApi( "sendContact" , payload )
    
    def sendChatAction(self , chat_id, action):
        payload = {'chat_id': chat_id, 'action': action}
        return self.client.callApi( "sendChatAction" , payload )
    
    def sendMediaGroup(self , chat_id, media, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, protect_content=None):
        payload = {'chat_id': chat_id, 'media': media }
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if allow_sending_without_reply is not None:
            payload['allow_sending_without_reply'] = allow_sending_without_reply
        if protect_content is not None:
            payload['protect_content'] = protect_content
        return self.client.callApi( "sendMediaGroup" , payload )                
    
    def sendVenue(self , chat_id, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None, disable_notification=None, reply_to_message_id=None, reply_markup=None, allow_sending_without_reply=None, google_place_id=None,  google_place_type=None, protect_content=None):
        payload = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude, 'title': title, 'address': address}
        if foursquare_id:
            payload['foursquare_id'] = foursquare_id
        if foursquare_type:
            payload['foursquare_type'] = foursquare_type
        if disable_notification is not None:
            payload['disable_notification'] = disable_notification
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            payload['reply_markup'] = reply_markup
        if allow_sending_without_reply is not None:
            payload['allow_sending_without_reply'] = allow_sending_without_reply
        if google_place_id:
            payload['google_place_id'] = google_place_id
        if google_place_type:
            payload['google_place_type'] = google_place_type
        if protect_content is not None:
            payload['protect_content'] = protect_content
        return self.client.callApi( "sendVenue" , payload )
    
    def sendPoll( self , chat_id, question, options,is_anonymous = None, type = None, allows_multiple_answers = None, correct_option_id = None,  explanation = None, explanation_parse_mode=None, open_period = None, close_date = None, is_closed = None, disable_notification=False, reply_to_message_id=None, allow_sending_without_reply=None,  reply_markup=None, explanation_entities=None, protect_content=None):
        payload = { 'chat_id': str(chat_id), 'question': question, 'options': options  }
        if is_anonymous is not None:
            payload['is_anonymous'] = is_anonymous
        if type is not None:
            payload['type'] = type
        if allows_multiple_answers is not None:
            payload['allows_multiple_answers'] = allows_multiple_answers
        if correct_option_id is not None:
            payload['correct_option_id'] = correct_option_id
        if explanation is not None:
            payload['explanation'] = explanation
        if explanation_parse_mode is not None:
            payload['explanation_parse_mode'] = explanation_parse_mode
        if open_period is not None:
            payload['open_period'] = open_period
        if close_date is not None:
            payload['close_date'] = close_date
        if is_closed is not None:
            payload['is_closed'] = is_closed
        if disable_notification:
            payload['disable_notification'] = disable_notification
        if reply_to_message_id is not None:
            payload['reply_to_message_id'] = reply_to_message_id
        if allow_sending_without_reply is not None:
            payload['allow_sending_without_reply'] = allow_sending_without_reply
        if reply_markup is not None:
            payload['reply_markup'] = reply_markup
        if explanation_entities:
            payload['explanation_entities'] = explanation_entities
        if protect_content:
            payload['protect_content'] = protect_content 
        return self.client.callApi ("sendPoll", payload )
    
    def stopPoll(self , chat_id, message_id, reply_markup=None):
        payload = {'chat_id': str(chat_id), 'message_id': message_id}
        if reply_markup:
            payload['reply_markup'] = reply_markup
        return self.client.callApi ("stopPoll", payload )
    
    def answerCallbackQuery(self , callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
        payload = {'callback_query_id': callback_query_id}
        if text:
            payload['text'] = text
        if show_alert is not None:
            payload['show_alert'] = show_alert
        if url:
            payload['url'] = url
        if cache_time is not None:
            payload['cache_time'] = cache_time
        return self.client.callApi ("answerCallbackQuery", payload )
    
    def answerInlineQuery(self , inline_query_id, results, cache_time=None, is_personal=None, next_offset=None, switch_pm_text=None, switch_pm_parameter=None):
        payload = {'inline_query_id': inline_query_id, 'results': results }
        if cache_time is not None:
            payload['cache_time'] = cache_time
        if is_personal is not None:
            payload['is_personal'] = is_personal
        if next_offset is not None:
            payload['next_offset'] = next_offset
        if switch_pm_text:
            payload['switch_pm_text'] = switch_pm_text
        if switch_pm_parameter:
            payload['switch_pm_parameter'] = switch_pm_parameter
        return self.client.callApi ("answerInlineQuery", payload )
        
    
    
   

        
        
        
        
        
        

    
    
    
    
