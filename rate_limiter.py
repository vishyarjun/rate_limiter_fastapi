
from limiting_algorithms import FixedCounterWindow,TokenBucket, SlidingWindow, SlidingWindowCounter
class RateLimitFactory:
   @staticmethod
   def get_instance(algorithm:str = None):
    if algorithm== "TokenBucket":
        return TokenBucket()
    
    elif algorithm== "FixedCounterWindow":
        return FixedCounterWindow()

    elif algorithm== "SlidingWindow":
        return SlidingWindow()
    
    else:
        return SlidingWindowCounter()

    



    

