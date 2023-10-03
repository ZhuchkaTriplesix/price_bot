import json

user_data = "user_list.json"


def get_data(user_data):
    with open(user_data, "r") as data_file:
        user_dict = json.load(data_file)
        return user_dict


def data_write(user_data, user_dict):
    with open(user_data, "w") as data_file:
        data_file.write(json.dumps(user_dict))
