import json , logging 

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

class Broadcaster:
    def __init__(self , client , users , success=None ):
        self.users = users
        self.client = client
        self.success = success
        if isinstance(users , list) is False:
            self.users = [] 
    
    def user(self , users):
        self.users = users
        return self.users
    
    def onSuccess(self , callback):
        self.success = callback 
        return True
    
    def sendMessage(self , chat_id , text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, entities=None, allow_sending_without_reply=None, protect_content=None):
        payload = {'text': text}
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
        return self.newThread("sendMessage" , payload )
    
    def newThread(self , method , payload):
        error = []   # { chat_id: <int> , error: <str> }
        success = [] # { chat_id: <int> , result: <dict> }                
        for x in list:
            payload["chat_id"] = x
            resp = self.client. callApiNoLogs( method , payload )
            if resp["ok"] == False:
                _dict = { "chat_id": x , "error": "Telegram API returned error "+json.dumps(resp) }
                error.append( _dict )
            else:
                _dict = { "chat_id": x , "result": resp }
                success.append( _dict )                
        return self._notify( error , success , method , payload )
    
    def _notify(self , error , success , method , payload):
        t_error = len(error)
        t_success = len(success)
        total = t_error + t_success 
        remark = "Great !"
        if t_error > t_success:
            remark = "Error rate is more than success rate !"
        _dict = {
            "total" : total ,
            "success": {
                "integer" : str(t_success) , 
                "percentage" : t_success/total *100 ,
                "array" : success 
            },
            "error" : { 
                "integer" : str(t_error) , 
                "percentage" : t_error/total *100 ,
                "array" : error
            },
            "remark" : remark
        }
        if self.success is not None:
            return self.success( _dict )
        logging.warning("× : BROADCAST REPORT : ×")  
        print(json.dumps(_dict))
        
        
        
        
