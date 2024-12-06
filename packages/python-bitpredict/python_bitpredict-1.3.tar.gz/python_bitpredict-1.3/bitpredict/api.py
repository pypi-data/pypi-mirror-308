import requests

key = ""


def authenticate(input_key):
    global key
    key = input_key
# def get_stats():
#     global key
#     endpoint = "https://ztbitredict-be.vercel.app/get_stats"
#     headers = {"Authorization": "Bearer " + key}
#     return requests.get(endpoint, headers=headers).json()
def get_stats(model_name=""):
    global key
    if model_name == "":
        endpoint = "https://ztbitredict-be.vercel.app/get_stats"
        headers = {"Authorization": "Bearer " + key}
        return requests.get(endpoint, headers=headers).json()
    else:
        # if len(model_name.split("_")) == 3:
        #     endpoint = "https://ztbitredict-be.vercel.app/get/live_stats/" + model_name
        #     headers = {"Authorization": "Bearer " + key}
        #     return requests.get(endpoint, headers=headers).json()
        # else:
        endpoint = "https://ztbitredict-be.vercel.app/get_stats/" + model_name
        headers = {"Authorization": "Bearer " + key}
        return requests.get(endpoint, headers=headers).json()  

def get_forecast(model_name=""):
    global key
    if model_name == "":
        endpoint = "https://ztbitredict-be.vercel.app/get_strategies"
        headers = {"Authorization": "Bearer " + key}
        return requests.get(endpoint, headers=headers).json()
    else:
        # if len(model_name.split("_")) == 3:
        #     endpoint = "https://ztbitredict-be.vercel.app/get/live_strategies/" + model_name
        #     headers = {"Authorization": "Bearer " + key}
        #     return requests.get(endpoint, headers=headers).json()
        # else:
        endpoint = "https://ztbitredict-be.vercel.app/get_strategy/"+model_name
        headers = {"Authorization": "Bearer " + key}
        return requests.get(endpoint, headers=headers).json()
def get_ledger(model_name=""):
    global key
    if model_name != "":
        endpoint = "https://ztbitredict-be.vercel.app/get_ledger/" + str(model_name)
        headers = {"Authorization": "Bearer " + key}
        return requests.get(endpoint, headers=headers).json()
    else:
        return "Pass model name for ledger"

def get_historical_forecasts(model_name=""):
    global key
    if model_name != "":
        endpoint = "https://ztbitredict-be.vercel.app/get_ledger/" + str(model_name)
        headers = {"Authorization": "Bearer " + key}
        return requests.get(endpoint, headers=headers).json()
    else:
        return "Pass model name for getting historical forecasts"
