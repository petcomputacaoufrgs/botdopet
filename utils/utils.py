import datetime
import json

def initialize_date(current_day, interval):
    today = datetime.date.today()
    while current_day < today:
        current_day += datetime.timedelta(days=interval)
    return current_day

def read_file(file_name):
  with open(file_name, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
  return data

def format_date():
  with open('data/interpet_dates.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    dates = data['dates']
  now = datetime.datetime.now()
  actual_date = datetime.datetime(2022, 4, 9)
  for i in dates:
    day, month, year = i.split('/')
    formated_date = datetime.datetime(int(year), int(month), int(day))
    difference = formated_date - now
    if (actual_date - now).days < 0:
      actual_date = formated_date
    if difference <= (actual_date - now):
      actual_date = formated_date  
  return actual_date

def add_new_item_to_dict(offense_list, praise_list):
  dict = {'offenses': offense_list, 'praises': praise_list}
  with open('data/data.json', 'w+', encoding='utf-8') as outfile:
    json.dump(dict, outfile)
