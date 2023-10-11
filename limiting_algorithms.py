from datetime import datetime, timedelta
import threading
from fastapi import HTTPException
from cache import Cache

redis = Cache()

class RateLimit:
    def __init__(self):
        self.interval = 60
        self.limit_per_interval = 60
        self.lock = threading.Lock()


class RateLimitExceeded(HTTPException):
    def __init__(self, detail="Rate limit exceeded"):
        super().__init__(status_code=429, detail=detail)

class TokenBucket(RateLimit):
    def __init__(self):
        super().__init__()

        self.total_capacity = 10
        self.token_interval = 1
        self.tokens_per_interval = 1
        self.tokens = 10
        self.last_updated = datetime.now()
        



    def allow_request(self):
        with self.lock:
            curr = datetime.now()
            gap = (curr - self.last_updated).total_seconds()
            tokens_to_add =  gap*self.tokens_per_interval

            self.tokens = min(self.total_capacity,tokens_to_add+self.tokens)
            self.last_updated = curr

            if self.tokens>=1:
                self.tokens-=1
                return True
            raise RateLimitExceeded()

class FixedCounterWindow(RateLimit):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.curr_time = datetime.now().time().replace(second=0,microsecond=0)
    
    def allow_request(self):
        with self.lock:
            curr = datetime.now().time().replace(second=0,microsecond=0)
            if curr!=self.curr_time:
                self.curr_time = curr
                self.counter = 0
            
            if self.counter>=self.limit_per_interval:
                raise RateLimitExceeded()
            self.counter+=1
            return True

class SlidingWindow(RateLimit):
    def __init__(self):
        super().__init__()
        self.logs = []
        self.limit_per_interval = 60
        self.interval = 60

    
    def allow_request(self):
        while self.lock:
            curr = datetime.now()
            while len(self.logs)>0 and (curr-self.logs[0]).total_seconds()>self.interval:
                self.logs.pop(0)

            if len(self.logs)>=self.limit_per_interval:
                raise RateLimitExceeded()
                return
            
            self.logs.append(curr)
            return True
        
class SlidingWindowCounter(RateLimit):
    def __init__(self):
        super().__init__()
        self.current_window_counter = 0
        self.prev_window_counter = 0
        self.curr_window = datetime.now().replace(second=0,microsecond=0)
    
    def rotate_counter(self):
        curr = datetime.now().replace(second=0,microsecond=0)
        if curr == self.curr_window:
            return
        
        self.prev_window_counter = self.current_window_counter if ((curr-self.curr_window).total_seconds()//60)==1 else 0
        self.current_window_counter=0
        self.curr_window = curr

    
    def allow_request(self,ip):
        lock_acquired,lock_key = redis.aquire_lock(ip)
        if lock_acquired:
            self.current_window_counter,self.prev_window_counter,self.curr_window = redis.get_data(ip)
            seconds = datetime.now().second
            prev_window_reminder = self.limit_per_interval - seconds
            self.rotate_counter()
            print(self.current_window_counter,self.prev_window_counter, prev_window_reminder)
            limit = self.current_window_counter + int(self.prev_window_counter*(prev_window_reminder/60))
            
            if limit >= self.limit_per_interval:
                redis.release_lock(lock_key)
                raise RateLimitExceeded()
            self.current_window_counter+=1
            redis.set_data(ip,self.current_window_counter,self.prev_window_counter,self.curr_window)
            redis.release_lock(lock_key)
            return True


