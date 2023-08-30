from collections import defaultdict
import datetime
from db.utils_for_data import get_data


def hour_with_most_birds(num_of_days: int) -> [int, float]:
    birds_data = get_data(datetime.datetime.now() - datetime.timedelta(days=num_of_days + 1),
                          datetime.datetime.now())
    hour_counts = defaultdict(int)
    for entry in birds_data:
        entry_datetime = datetime.datetime.strptime(entry["time"], "%d/%m/%Y %H:%M:%S")
        hour = entry_datetime.hour
        hour_counts[hour] += entry["birds_sum"]
    most_birds_hour = max(hour_counts, key=hour_counts.get)

    return most_birds_hour, hour_counts[most_birds_hour]/30


def api_hour_with_most_birds(num_of_days: int = 30) -> str:
    most_birds_hour, average_most_birds = hour_with_most_birds(num_of_days)
    message = f'The time when there were the most birds in the last {num_of_days} days: {most_birds_hour}:00 - {most_birds_hour + 1}:00\n' \
              f'The average number of birds observed at this hour: {average_most_birds}'
    return message


def main():
    print(api_hour_with_most_birds())


if __name__ == "__main__":
    main()