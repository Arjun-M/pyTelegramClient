import json , requests , time , re
from .telegram import Telegram 
from threading import Thread , local
from requests.sessions import  Session
from .event import messageEvent 
from .types import isCommand , getCommand , getType , filterCommands , isClassHandler , isString , isList
from requests.exceptions import HTTPError, ConnectionError, Timeout

localThreadPool = local()
allClientProcess = [ " " ]

class Client:
    def __init__(self, token ):
        self.token = token
        self.answers = { }                       # { [chat_id]: <func> }
        self.telegram = Telegram( client=self )  # << class representing telegram api methods . >>
        self.message_handlers = []               # { callback: <func> , regexp:None , text:[] , commands:[] , type:[ "text" ] }
        self.edited_message_handlers = []        # { callback: <func> , regexp:None , text:[] , type:[ "text" ] }
        self.inline_handlers = []                # { callback: <func> , regexp:None , query:[] }
        self.callback_query_handlers = []        # { callback: <func> , regexp:None , data:[] }
        self.my_chat_member_handlers = []        # {  }
        self.chat_member_handlers = []           # {  }
        self.chat_join_request_handlers = []     # {  }
        self.process_handlers = { }
        self.master_function = []
    
    def reject( self ):
        return "$reject"
        
    def use(self , func):
        self.master_function.append( func )
        return self.debug("Added new master function .","INFO")
    
    def HTTP(self):
        if not hasattr( localThreadPool ,'session'):
            localThreadPool.session = requests.Session()
        return localThreadPool.session
        
    def debug(self , text , types="INFO" ):
        _time = time.strftime("%H:%M:%S", time.localtime() )
        print(f"{_time} [{types}] : {text}") # 23:46:10 [INFO] : {TEXT} !!
            
    def wait(self , time):
        time.sleep(int(time))
        
    def callApi(self , method ,  params={} ,  files=None):
        try:
            data = self.HTTP().post( f"https://api.telegram.org/bot{self.token}/{method}" , data = params , files = files  )
            return self._check_recived_result( data , method , files , params)
        except HTTPError:  
            return self._process_telegram_exception(files , params , method , None)
        except ConnectionError:  
            return self._process_telegram_exception(files , params , method , None)
        except Timeout:  
            return self._process_telegram_exception(files , params , method , None)
    
    def _post(self , method ,  params={} ,  files=None):
        try:
            data = self.HTTP().post( f"https://api.telegram.org/bot{self.token}/{method}" , data = params , files = files  )
            return data.json()
        except : 
            return None
    
    def register_conversation(self , chat , func):
        self.answers[chat] = func
        return 
    
    def _process_polling(self , offset , allowed_updates ):
        req = self._post("getUpdates" , {"offset":offset , "allowed_updates": allowed_updates , "limit":100} )
        if req["ok"] == False:
            self.polling = False            
            self.debug("Failed to 'getUpdates' seems this is not a valid token ." , "WARNING")
            return False
        else:   return req
    
    def polling(self , log_updates=False , drop_pending_updates=False , allowed_updates=None):
        self.polling = True
        offset = 0
        if self._post("getMe")["ok"] is False : return self.debug("Check your token and try again .!" , "WARNING")
        self._post("deleteWebhook", { "drop_pending_updates":drop_pending_updates }) # delete webhook before start polling .
        self.debug( "Polling has been started !.")
        while self.polling :
            updates = self._process_polling(offset+1 , allowed_updates )
            if updates is False:  break;
            if updates is not None:
                for x in updates["result"]:
                    offset = x["update_id"] 
                    self.processUpdate ( x )    
                    if log_updates is True:  self.debug( json.dumps( x ) )
        self.debug( "Polling has been stopped !." , "WARNING" )
        
    def _process_message_update(self , update ):
        event = messageEvent( self , update )
        cmd = getCommand( event.text )
        update_type = getType( event.update )
        for _handler in self.message_handlers:
            if event.chat.id in self.answers:
                return self.answers[ event.chat.id ]( event )
            if event.text in _handler["text"] :
                return _handler["callback"]( event )
            if _handler["regexp"] is not None and event.text is not None:
                r = re.search( _handler["regexp"] , str(event.text) )
                if r : return _handler["callback"]( event ) 
            if cmd in _handler["commands"]:
                return _handler["callback"]( event )
            if update_type in _handler["types"]:
                return _handler["callback"]( event )
    
    def _process_telegram_exception(self , files=None , payload=None , method=None , data=None):
        pass
        
    def processUpdate(self, update):
        for func in self.master_function:
            if func( update ) == "$reject": return self.debug( "Rejected an Update .!" , "WARNING")
        if "message" in update:
            return self._process_message_update( update["message"] )
    
    def addHandler(self , _class):
        if not isClassHandler(_class): return
        if _class.type == "messageHandler":
            return self._message_handler(_class.handler)
    
    def handler(self , *args, **kwargs):
        def inner(func):
            self.addHandler(list(args)[0])
            return func
        return inner

    def _check_recived_result(self, data , method , files , params ):
        try:
            result = data.json()
            if result['ok'] :  return _create_tuple( result["result"] )
            self._process_telegram_exception( method=method , files=files , payload=params , data= result )           
        except:
            self._process_telegram_exception( method=method , files=files , payload=params , data= "Invalid JSON Response") 
        return False
        
    def _message_handler(self , _args ):
        _dict = {"callback": _args["func"] , "commands":[] , "types":[] , "regexp": _args.get('regexp', None) , "text":[] }
        if "text" in _args:  
            if isList( _args["text"] ) : _dict["text"] = _args["text"]
        if "regexp" in _args:
            if isString( _args["regexp"] ) : _dict["regexp"] = _args["regexp"] 
        if "commands" in _args: 
            if isList( _args["commands"] ) : _dict["commands"] = filterCommands( _args["commands"] )
        if "types" in _args: 
            if isList( _args["types"] ) : _dict["types"] = _args["types"]
        self.message_handlers.append(_dict)
    
      
        
