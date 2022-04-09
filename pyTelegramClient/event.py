import json

class messageEvent:
    def __init__(self , Bot , request):
        self.client = Bot
        self.request = request  # Extension for getting updates
        self.json = request     # Extension for getting updates
        self.update = request   # Extension for getting updates
        
    def json(self):
        return self.request
    
    """
    ➢ Mirror Extension of "sendChatAction()"
    """
    def typing(self ):
        chat = self.user().get("id")
        payload = {'chat_id': chat , 'action': "typing"}
        return self.client.callApi( "sendChatAction" , payload )    
    
    """
    ➢ Mirror Extension of "sendMessage()"
    """
    def respond(self , text , reply=False , disable_web_page_preview=None , reply_markup=None , disable_notification=None, entities=None , parse_mode=None , protect_content=None):
        chat = self.request.get("chat").get("id")
        payload = {'chat_id': str(chat), 'text': text , 'allow_sending_without_reply':True}
        request = self.request
        if reply == True :
            payload['reply_to_message_id'] = self.request.get("reply_to_message_id")
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
    
    """
    ➢ Mirror Extension of "deleteMessage()"
    """
    def delete(self):
        payload = { "chat_id": self.request.get("chat").get("id"), "message_id": self.request.get("message_id")    }
        return self.client.callApi("deleteMessage" , payload )
    
    """
    ➢ Mirror Extension of "sendMessage()"
    """
    def sendKeyboard(self , btn , message):
        buttons = { "keyboard": btn , "resize_keyboard":True }
        if isinstance(btn  , str):
            buttons = btn
        payload = { "text": message , "chat_id": self.request.get("chat").get("id"), "reply_markup": btn }
        return self.client.callApi("sendMessage" , payload )
    
    def sendInlineKeyboard(self , btn , message):
        buttons = { "inline_keyboard": btn }
        if isinstance(btn  , str):
            buttons = btn
        payload = { "text": message , "chat_id": self.request.get("chat").get("id"), "reply_markup": btn }
        return self.client.callApi("sendMessage" , payload )
    
class callbackQueryEvent:
    def __init__(self , Bot , request):
        self.client = Bot
        self.request = request  # Extension for getting updates
        self.json = request     # Extension for getting updates
        self.update = request   # Extension for getting updates
        
    def json(self):
        return self.request    
        
    """
    ➢ Mirror Extension of "deleteMessage()"
    """
    def delete(self):
        request = self.json()
        payload = { "chat_id": request.get("message").get("chat").get("id"), "message_id": request["message"].get("message_id")  }
        return self.client.callApi("deleteMessage" , payload )
    
    """
    ➢ Mirror Extension of "answerCallbackQuery()"
    """
    def answer(self , text , alert=False):
        payload = { "callback_query_id": self.json().get("id") }
        if alert :
            payload['show_alert'] = alert
        return self.client.callApi("answerCallbackQuery" , payload )
    
    """
    ➢ Mirror Extension of "editMessageText()"
    """
    def edit(self, text): # edit both reply mark and text
        request = self.json()
        payload = {"text":text}
        if request.get("inline_message_id") is not None:
            payload["inline_message_id"] = request.get("inline_message_id")
        else:
            payload["message_id"] = request.get("message").get("message_id")
        return 
    
    def editInlineKeyboard(self , buttons): # edit just reply mark and leave text as it is
        pass
    

class inlineQueryEvent:
    def __init__(self , Bot , request):
        self.client = Bot
        self.request = request  # Extension for getting updates
        self.json = request     # Extension for getting updates
        self.update = request   # Extension for getting updates
        
    def json(self):
        return self.request    
    
    """
    ➢ Mirror Extension of "answerInlineQuery()"
    """
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
    
    
    
    
