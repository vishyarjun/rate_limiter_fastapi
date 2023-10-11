# Build your own API Rate Limiter - FastAPI
An API rate limiter is a crucial component in many web applications and APIs to manage and control the rate at which clients or users can make requests to the API. Its primary purpose is to prevent abuse, ensure fair usage, protect the API server from overload, and maintain a high quality of service for all users. Rate limiting is often implemented to:
- Protect Resources
- Ensure Fairness
- Mitigate DDoS Attacks
- Billing and Monetization

This is a FastAPI implementation of rate limiter

## Prerequisites
1. Python Virtual Environment - Follow this [simple guide](https://medium.com/datacat/a-simple-guide-to-creating-a-virtual-environment-in-python-for-windows-and-mac-1079f40be518) to create a virtual environment
2. Docker Installation - Follow [this guide](https://docs.docker.com/engine/install/) to install docker on your local machine

## Installation
1. Open Docker and run a redis container instance using below command (in a terminal or cmd)
```sh
docker run -d --name redis-container -p 6379:6379 redis:latest 
```
2. verify if the container is up and running using the command  `docker ps -a`
3. Create and Enter into your virtual environment
4. cd to the root directory of the application 
4. Install the dependencies using following command `pip install -r requirements.txt`
5. Once the dependencies are installed, we can run the program using following commands.
- To Run the Sliding Window Counter Algorithm based API rate limiter use the following command 
```sh
uvicorn api:app --reload
```
- To run all the other algorithms, Open the file `api2.py`
- Choose the algorithm by modifying line no.13 (Example: TokenBucket)
- Once the algorithm is chosen, run the app 
```sh
uvicorn api2:app --reload
```

## Run the app in multiple servers
The Sliding Window Counter Algorithm implementation uses redis cache. As the storage is centralized, this implementation supports scaling and running multiple app servers. You can make API calls to both the servers and see the consistent results. Following are the steps

- Open the venv
- Run the first app in port 8000
```sh
uvicorn api:app --reload --port 8000
```
- Open another terminal instance and enter into venv
- Run the second app in port 7000
```sh
uvicorn api:app --reload --port 7000
```