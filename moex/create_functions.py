import datetime

HOLIDAY_DAYS = ['2025-05-09', '2025-06-12', '2025-11-04', '2025-12-31']

MIN_START_TIME_FOR_WORKING_DAY = datetime.time(hour=6)
MAX_END_TIME_FOR_WORKING_DAY = datetime.time(hour=23, minute=59, second=59)
MIN_START_TIME_FOR_DAY_OFF = datetime.time(hour=9)
MAX_END_TIME_FOR_DAY_OFF = datetime.time(hour=18, minute=59, second=59)


def parse_start_structure(raw_data: dict) -> list[dict]:
    """Парсинг начальной структуры."""
    start_stracture = []
    columns = raw_data['columns']
    for row in raw_data['data']:
        start_stracture.append(dict(zip(columns, row)))
    return start_stracture


def parse_securities_and_marketdata(raw_data: dict) -> dict:
    """Парсинг securities и marketdata."""
    result_dict = {}
    securities = parse_start_structure(raw_data['securities'])
    marketdata = parse_start_structure(raw_data['marketdata'])
    for block_of_securities in securities:
        result_dict[block_of_securities['SECID']] = {'securities': block_of_securities}
    for block_of_marketdata in marketdata:
        result_dict[block_of_marketdata['SECID']].update({'marketdata': block_of_marketdata})
    return result_dict


def get_day_type(date: datetime):
    """
    Определяет тип дня:
    0 - рабочий день (пн-пт, не праздник)
    1 - выходной (сб-вс, не праздник)
    2 - праздник (в списке HOLIDAY_DAYS)
    """
    if date.strftime('%Y-%m-%d') in HOLIDAY_DAYS:
        return 2
    if date.weekday() >= 5:
        return 1
    return 0


def get_next_valid_start_time(current_datetime: datetime):
    """Получает следующее допустимое время начала с учетом рабочих часов Московской Биржи."""
    while True:
        day_type = get_day_type(current_datetime)

        if day_type == 2:  # Праздник - пропускаем весь день
            # Переходим на начало следующего дня
            current_datetime = current_datetime.replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)
            continue

        # Определяем временные границы для текущего типа дня
        if day_type == 0:  # Рабочий день
            min_time = MIN_START_TIME_FOR_WORKING_DAY
            max_time = MAX_END_TIME_FOR_WORKING_DAY
        else:  # Выходной
            min_time = MIN_START_TIME_FOR_DAY_OFF
            max_time = MAX_END_TIME_FOR_DAY_OFF

        current_time = current_datetime.time()

        # Если текущее время меньше минимального - устанавливаем на минимальное
        if current_time < min_time:
            return current_datetime.replace(hour=min_time.hour, minute=0, second=0)

        # Если текущее время в допустимом диапазоне - возвращаем как есть
        if current_time <= max_time:
            return current_datetime.replace(minute=0, second=0)

        # Иначе переходим на следующий день
        current_datetime = current_datetime.replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)


def set_appropriate_datetime(list_of_costs: list[float], last_date_end: str, predict_starting_with_next_hour: bool):
    last_datetime_end = datetime.datetime.strptime(last_date_end, '%Y-%m-%d %H:%M:%S')

    if predict_starting_with_next_hour:
        next_start_date = (last_datetime_end + datetime.timedelta(hours=1)).replace(minute=0, second=0)
    else:
        next_start_date = last_datetime_end.replace(minute=0, second=0)

    next_start_date = get_next_valid_start_time(next_start_date)
    new_dates = []

    while len(new_dates) < len(list_of_costs):
        day_type = get_day_type(next_start_date)

        if day_type == 2:  # Праздник - пропускаем
            next_start_date = get_next_valid_start_time(next_start_date + datetime.timedelta(hours=1))
            continue

        # Определяем временные границы для текущего типа дня
        if day_type == 0:  # Рабочий день
            min_hour = MIN_START_TIME_FOR_WORKING_DAY.hour
            max_hour = MAX_END_TIME_FOR_WORKING_DAY.hour
        else:  # Выходной
            min_hour = MIN_START_TIME_FOR_DAY_OFF.hour
            max_hour = MAX_END_TIME_FOR_DAY_OFF.hour

        # Проверяем, что текущий час в допустимом диапазоне
        if min_hour <= next_start_date.hour <= max_hour:
            end_time = (next_start_date + datetime.timedelta(hours=1) - datetime.timedelta(seconds=1))
            new_dates.append({
                'begin': next_start_date.strftime('%Y-%m-%d %H:%M:%S'),
                'end': end_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Переходим к следующему часу
        next_start_date += datetime.timedelta(hours=1)

        # Если следующий час выходит за пределы рабочего времени, находим следующее допустимое время
        if next_start_date.hour > max_hour or not (min_hour <= next_start_date.hour <= max_hour):
            next_start_date = get_next_valid_start_time(next_start_date)

    for index, new_date in enumerate(new_dates):
        new_date.update({'close': list_of_costs[index]})

    return new_dates
