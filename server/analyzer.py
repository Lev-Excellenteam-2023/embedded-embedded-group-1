from collections import defaultdict
import datetime
from db.utils_for_data import get_data


def hour_with_most_birds(num_of_days: int = 30) -> [int, float]:
    """
    Returns the hour when there were most birds in the last days
    """
    hour_counts = get_num_of_birds_per_hour(num_of_days)
    most_birds_hour = max(hour_counts, key=hour_counts.get)

    return most_birds_hour, hour_counts[most_birds_hour]/num_of_days


def api_hour_with_most_birds(num_of_days: int = 30) -> str:
    most_birds_hour, average_most_birds = hour_with_most_birds(num_of_days)
    message = f'The time when there were the most birds in the last {num_of_days} days: {most_birds_hour}:00 - {most_birds_hour + 1}:00\n' \
              f'The average number of birds observed at this hour: {average_most_birds}'
    return message


def api_hours_with_high_birds_average(num_of_birds: float = 40, num_of_days: int = 30) -> str:
    average_counts = hours_with_high_birds_average(num_of_birds, num_of_days)
    if not average_counts:
        message = 'There are no information'
    else:
        message = 'The times when there were a high birds average:\n'
    for key in average_counts:
        message += f'{key}:00-{key+1}:00     {average_counts[key]}'
    return message


def hours_with_high_birds_average(num_of_birds: float, num_of_days: int = 30) -> dict:
    """
    Returns the hours in the last days, where the average number of birds per hour is higher than num_of_birds
    """
    hour_counts = get_num_of_birds_per_hour(num_of_days)
    average_counts = {hour: counts/num_of_days for hour, counts in hour_counts.items()
                      if counts/num_of_days >= num_of_birds}
    return average_counts


def get_num_of_birds_per_hour(num_of_days: int = 30) -> dict:
    """
    The function gets a number, and sums up the number of birds observed each hour on the above number of days
    :param num_of_days: number of last days
    :return: A dictionary - the keys are the hours, and the values are the number of birds
    """
    birds_data = get_data(datetime.datetime.now() - datetime.timedelta(days=num_of_days + 1),
                          datetime.datetime.now())
    hour_counts = defaultdict(int)
    for entry in birds_data:
        entry_datetime = datetime.datetime.strptime(entry["time"], "%d/%m/%Y %H:%M:%S")
        hour = entry_datetime.hour
        hour_counts[hour] += entry["birds_sum"]
    return hour_counts
