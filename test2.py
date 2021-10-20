import datetime
import requests

current_time = datetime.datetime.now()
current_day = current_time.strftime("%Y-%m-%d")
raw_data = 'view=action&action=ajaxPowerballLog&actionType=dayLog&date=' + current_day + '&page=1'
response_pball = requests.post("https://www.powerballgame.co.kr/", headers={'content-length': '76',
                                                                            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                               data=raw_data).json()

print(raw_data)
print(response_pball['content'])
print(len(response_pball['content']))
print(response_pball['content'][0])

print(datetime.datetime.now().strftime("%m-%d %H:%M:%S"))

print(response_pball['content'][0]['number'].split(','))
print(response_pball['content'][0]['number'].split(',')[0])