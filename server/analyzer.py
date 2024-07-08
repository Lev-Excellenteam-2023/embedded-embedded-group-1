from collections import defaultdict
import datetime
from db.utils_for_data import get_data


def hour_with_most_birds(num_of_days: int = 30) -> [int, float]:
    """
    Returns the hour when there were most birds in the last days
    """
    hour_counts = get_num_of_birds_per_hour(num_of_days)
    most_birds_hour = max(hour_counts, key=hour_counts.get)

    return most_birds_hour, hour_counts[most_birds_hour] / num_of_days


def api_hour_with_most_birds(num_of_days: int = 30) -> str:
    """
    Returns a message include the hour when there were most birds in the last days
    :param num_of_days: number of last days
    """
    most_birds_hour, average_most_birds = hour_with_most_birds(num_of_days)
    message = f'During the past {num_of_days} days, the hour with the highest bird activity has been from' \
              f' {most_birds_hour}:00 to {most_birds_hour + 1}:00.\n' \
              f'During this time frame, an average of {average_most_birds} birds have been observed.'
    return message


def api_hours_with_high_birds_average(num_of_birds: float = 5, num_of_days: int = 30) -> str:
    """
    Return a message includes the hours in the last days, when the average number of birds per hour is higher
    than num_of_birds
    :param num_of_birds: number of birds
    :param num_of_days: number of last days
    """
    average_counts = hours_with_high_birds_average(num_of_birds, num_of_days)
    if not average_counts:
        message = f'No hours were found in which there were on average more than {num_of_birds} birds'
    else:
        message = 'The period of heightened bird activity:\n'
    for key in average_counts:
        message += f'{key}:00-{key + 1}:00     {average_counts[key]}'
    return message


def hours_with_high_birds_average(num_of_birds: float, num_of_days: int = 30) -> dict:
    """
    Returns the hours in the last days, when the average number of birds per hour is higher than num_of_birds
    """
    hour_counts = get_num_of_birds_per_hour(num_of_days)
    average_counts = {hour: counts / num_of_days for hour, counts in hour_counts.items()
                      if counts / num_of_days >= num_of_birds}
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


def get_months_in_year_with_lot_of_birds(num_of_birds: int = 100) -> list[int]:
    """
    Returns a list of months with a lot of birds
    """
    birds_data = get_data(datetime.datetime.now() - datetime.timedelta(days=365),
                          datetime.datetime.now())
    month_counts = defaultdict(int)
    for entry in birds_data:
        entry_datetime = datetime.datetime.strptime(entry["time"], "%d/%m/%Y %H:%M:%S")
        month = entry_datetime.month
        month_counts[month] += entry["birds_sum"]
    months = [key for key in month_counts if month_counts[key] >= num_of_birds]
    return months


def report_month_with_lot_of_birds() -> str:
    """
    Returns a report if there may be many birds in the area
    """
    months = get_months_in_year_with_lot_of_birds()
    message = ''
    if datetime.datetime.now().month in months:
        message = 'Note!\nDuring this period there may be many birds in the area!'
    return message


def api_get_data_between_two_times(since: datetime, to: datetime) -> list[dict]:
    """
    Returns data received between 'since' and 'to'
    """
    birds_data = get_data(since, to)
    return birds_data
