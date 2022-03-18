import requests , json , logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

message = {  }
inline = {  }
globalhandler = { "inline":[] , "chosen_inline_result":[] }

class TelegramClient:
    def __init__(self, token ):
        self.token = token
        self.polling = False        
    
    def callApi(self , method ,  params={} ):
        data = requests.post (f"https://api.telegram.org/bot{self.token}/{method}" , params).json()
        return data
    
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
                                        
    def processUpdate(self , update={} ):
        req = None
        if "message" in update:
            req = parseMessage( update["message"] )
            return self.emitMessage( req )
        
    def addMessageHandler(self , func , commands=None , chat_types= None , regexp = None , content_types= None ):
        return True
    
    def addInlineHandler(self , func , query=None ):
        if query is None:
            globalhandler["inline"].append(func)
            return True
        inline[query] = func
        return True
    
    def addChosenInlineHandler(self , func):
        globalhandler["chosen_inline_result"].append(func)
        return True
    
    
        
        
        
