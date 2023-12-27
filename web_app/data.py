import os
import json

with open(os.getcwd() + "/data/names.json", "r", encoding="utf-8") as f:
    names_data = json.load(f)

with open(os.getcwd() + "/data/phones.json", "r", encoding="utf-8") as f:
    phones_data = json.load(f)

with open(os.getcwd() + "/data/states.json", "r", encoding="utf-8") as f:
    states_data = json.load(f)

month_map = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec'
}
