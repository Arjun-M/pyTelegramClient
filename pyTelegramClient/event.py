import json

class messageEvent:
    def __init__(self , Bot , request):
        self.client = Bot
        self.request = request
        
    def json(self):
        return self.request
    
    def user(self):
        req = self.request
        return req.get("user" , {} )
    
    def reply(self , text , disable_web_page_preview=None , reply_markup=None , disable_notification=None, entities=None , parse_mode=None , protect_content=None):
        chat = self.user().get("id")
        request = self.request
        payload = {'chat_id': str(chat), 'text': text , 'reply_to_message_id': request.get("message_id") , 'allow_sending_without_reply':True}
        chat = request.get("user", {} ).get("id")        
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
        return self.client.callApi("sendMessage" , payload )
    
    def typing(self ):
        chat = self.user().get("id")
        payload = {'chat_id': chat , 'action': "typing"}
        return self.client.callApi( "sendChatAction" , payload )    
    
    def respond(self , text , reply_to_message_id=None , disable_web_page_preview=None , reply_markup=None , disable_notification=None, entities=None , parse_mode=None , protect_content=None):
        chat = self.user().get("id")
        payload = {'chat_id': str(chat), 'text': text , 'allow_sending_without_reply':True}
        request = self.request
        if reply_to_message_id :
            payload['reply_to_message_id'] = reply_to_message_id 
        chat = request.get("user", {} ).get("id")        
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
        return self.client.callApi("sendMessage" , payload )
    
    def delete(self):
        payload = { 
          "chat_id": self.request.get("chat").get("id"),
          "message_id": self.request.get("message_id") 
        }
        return self.client.callApi("deleteMessage" , payload )
        
    
class callbackQueryEvent:
    def __init__(self , Bot , request):
        self.client = Bot
        self.request = request
        
    def json(self):
        return self.request
    
    def user(self):
        req = self.json()
        return req.get("user" , {} )    
    
    def delete(self):
        request = self.json()
        payload = { "chat_id": request.get("message").get("chat").get("id"), "message_id": request["message"].get("message_id")  }
        return self.client.callApi("deleteMessage" , payload )
    
    def answer(self , text , alert=False):
        payload = { "callback_query_id": self.json().get("id") }
        if alert :
            payload['show_alert'] = alert
        return self.client.callApi("answerCallbackQuery" , payload )
    
    def edit(self, text):
        request = self.json()
        payload = {"text":text}
        if request.get("inline_message_id") is not None:
            payload["inline_message_id"] = request.get("inline_message_id")
        else:
            payload["message_id"] = request.get("message").get("message_id")
        return 
    
    
class inlineQueryEvent:
    def __init__(self , Bot , request):
        self.client = Bot
        self.request = request
        
    def json(self):
        return self.request
    
    def user(self):
        req = self.request
        return req.get("user" , {} )
    
    def answer(self , results, cache_time=None, is_personal=None, next_offset=None, switch_pm_text=None, switch_pm_parameter=None):
        inline_query_id = self.request.get("inline_query_id")
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
    
    
