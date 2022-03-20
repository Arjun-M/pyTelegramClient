import requests , json , logging , re


logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')  

class TelegramClient:
    def __init__(self, token ):
        self.token = token
    
    def callApi(self , method ,  params={} ,  files=None):
        data = requests.post ( f"https://api.telegram.org/bot{self.token}/{method}" , data = params , files = files  )
        return data.json()
    
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
                    #self.processUpdate (x)
