import json
import datetime
import logging

from db import config


def store_data(data_birds: dict) -> None:
    """
    The function get a dictionary include data about birds, and save it into a json file
    :param data_birds: Dictionary with data about birds
    """
    try:
        with open(config.DB_OF_BIRDS, 'r') as json_file:
            existing_data = json.load(json_file)
        existing_data.append(data_birds)
        with open(config.DB_OF_BIRDS, 'w') as json_file:
            json.dump(existing_data, json_file)
        logging.info(f"Data saved successfully.")
    except Exception as e:
        logging.error("Failed to store data: %s", e)


def get_data(since: datetime, to: datetime) -> list[dict]:
    """
    The function gets two dates, and returns the data that saved between these dates
    :param since:   First datetime
    :param to:   Last datetime
    :return:   A list of dictionary with data about the birds
    """
    with open(config.DB_OF_BIRDS, 'r') as json_file:
        birds_list = json.load(json_file)
        filtered_data = []
        for birds_data in birds_list:
            bird_datetime = datetime.datetime.strptime(birds_data["time"], "%d/%m/%Y %H:%M:%S")
            if since <= bird_datetime <= to:
                filtered_data.append(birds_data)
        return filtered_data