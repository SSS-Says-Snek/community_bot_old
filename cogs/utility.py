import json

WIFI_ONLINE = 27000
WIFI_OFFLINE = 79200


def string2fraction(fraction_str):
    try:
        return float(fraction_str)
    except ValueError:
        num, denominator = fraction_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        fraction = float(num) / float(denominator)
        return whole - fraction if whole < 0 else whole + fraction


def sec_since_midnight(now):
    return (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()


def sec_to_time(seconds: float) -> tuple:
    return_thing = []
    quot, remainder = divmod(seconds, 3600)
    return_thing.append(quot)
    quot2, remainder2 = divmod(remainder, 60)
    return_thing.append(quot2)
    return_thing.append(remainder2)
    return tuple(return_thing)


def get_json_data(fp, key_to_key=None):
    if key_to_key:
        with open(fp) as read_json:
            return json.load(read_json)[key_to_key]
    else:
        with open(fp) as read_json:
            return json.load(read_json)
