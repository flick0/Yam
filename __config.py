import json


class config:
    def get_json():
        with open("./config.json", "r") as f:
            return json.load(f)

    def channel(arg, /):
        return config.get_json()["channels"].get(arg)

    def message(arg, /):
        return config.get_json()["messages"].get(arg)

    def role(arg, /):
        return config.get_json()["roles"].get(arg)
