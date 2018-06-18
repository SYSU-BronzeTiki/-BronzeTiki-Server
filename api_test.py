
import requests
import re
from bs4 import BeautifulSoup
import json

url = "http://119.29.13.173:8080/api"

# # # new goal
# # try:
# #     subTaskList = []
# #     subTaskList.append({'step': 1, 'days': 720, 'taskTitle': '存首期', 'taskContent': '存5000元', \
# #                         'frequency': 30, 'beginDate': '2018-01-01', 'endDate': '2018-12-31'})
# #     subTaskList.append({'step': 2, 'days': 720, 'taskTitle': '供房子', 'taskContent': '存5000元', \
# #                         'frequency': 30, 'beginDate': '2019-01-01', 'endDate': '2019-12-31'})
# #     payload = {'message-type': 'new_goal', 'username': 'test', 'goalTitle': 'I will make a GF in new year.', \
# #                'goalType': 'emotion', 'days': 31, 'beginDate': '2018-01-01', 'endDate': '2018-12-31', 'step': str(subTaskList)}
# #     #print(payload['step'])
# #     r = requests.post(url6, data=payload)
# #     print(r.text)
# # except:
# #     print("error login")

# # day card
# try:
#     # finishedCard = False : uncheck
#     payload = {'message-type': 'new_card', 'username': 'test', 'taskId': 7, 'day': '2018-01-01', 'finishedCard': True}
#     r = requests.post(url6, data=payload)
#     print(r.text)
# except:
#     print("error card-task")

# # del day task
# try:
#     payload = {'message-type': 'del_task', 'username': 'test', 'taskId': 7, 'day': '2018-01-02'}
#     r = requests.post(url6, data=payload)
#     print(r.text)
# except:
#     print("error del")

# # index
# try:
#     payload = {'message-type': 'query_index', 'username': 'test', 'day': '2018-01-03'}
#     r = requests.post(url6, data=payload)
#     print(r.text)
# except:
#     print("error query index")

# # time shaft
# try:
#     payload = {'message-type': 'query_time_shaft', 'username': 'test'}
#     r = requests.post(url6, data=payload)
#     print(r.text)
# except:
#     print("error query time shaft")

# # moment
# try:
#     payload = {'message-type': 'query_moment', 'username': 'test'}
#     r = requests.post(url6, data=payload)
#     print(r.text)
# except:
#     print("error query moment")
