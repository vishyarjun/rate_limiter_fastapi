from fastapi import FastAPI, Request
from rate_limiter import RateLimitFactory
from limiting_algorithms import RateLimitExceeded
app = FastAPI()
rate_limiter = RateLimitFactory.get_instance()

@app.get("/limited")
def limited(request: Request):
    client = request.client.host
    try:
        if rate_limiter.allow_request(client):
            return "This is a limited use API"
    except RateLimitExceeded as e:
        raise e

@app.get("/unlimited")
def unlimited(request: Request):
    return "Free to use API limitless"