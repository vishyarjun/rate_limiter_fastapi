import redis
from datetime import datetime
class Cache:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)
        self.expiration_time_seconds = 60
    
    def set_data(self,ip,current_window_counter,prev_window_counter,curr_window):
        data = {
            "current_window_counter": current_window_counter,
            "prev_window_counter": prev_window_counter,
            "curr_window": str(curr_window)
        }
        self.redis_client.hmset(ip, data)
        self.redis_client.expire(ip, self.expiration_time_seconds)
        
            

    def aquire_lock(self,ip):
        key = f"ip:{ip}"
        lock_key = f"lock:{str(datetime.now())}"  # Define a lock key
        lock_ttl = 5  # Set a reasonable lock time-to-live (in seconds)
        lock_acquired = self.redis_client.setnx(lock_key, "1")
        return lock_acquired,lock_key
    
    def release_lock(self, lock_key):
        self.redis_client.delete(lock_key)


    def get_data(self,ip):
        fields = ['current_window_counter','prev_window_counter','curr_window']
        values = self.redis_client.hmget(ip,fields)
        current_window_counter,prev_window_counter,curr_window = [value.decode('utf-8') if value is not None else None for value in values]
        format_str = "%Y-%m-%d %H:%M:%S"
        # Parse the string into a datetime object
        
        if curr_window is None:
            current_window_counter = 0 
            prev_window_counter = 0
            curr_window = datetime.now().replace(second=0,microsecond=0)
        else:
            current_window_counter,prev_window_counter,curr_window = [value.decode('utf-8') if value is not None else None for value in values]
            curr_window = datetime.strptime(curr_window, format_str)
            current_window_counter = int(current_window_counter)
            prev_window_counter = int(prev_window_counter)
        return current_window_counter,prev_window_counter,curr_window