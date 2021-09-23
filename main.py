# This is a sample Python script.
import time

import requests
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
global parse_result, now_round, last_round
parse_result = {}
now_round = 0
last_round = 0

def parse_start():
    #전역으로 사용할 변수 지정
    global parse_result, now_round, last_round
    parse_count = 1
    #전체 프로세스 반복
    while True:
        raw_data = 'view=action&action=ajaxPowerballLog&actionType=dayLog&date=2021-09-23&page=' + str(parse_count)
        response = requests.post("https://www.powerballgame.co.kr/",headers={'content-length':'76','content-type':'application/x-www-form-urlencoded; charset=UTF-8'},data=raw_data).json()
        if last_round == int(response['content'][0]['round']):
            #print(last_round)
            #print(int(response['content'][0]['round']))
            print("패스")
            time.sleep(10)
            continue
        while response['endYN']=='N':
            if parse_count == 1:
                last_round = int(response['content'][0]['round'])
            for contents in response['content']:
                parse_result[contents['round']] = contents['powerballOddEven']
            parse_count += 1
            raw_data = 'view=action&action=ajaxPowerballLog&actionType=dayLog&date=2021-09-23&page=' + str(parse_count)
            response = requests.post("https://www.powerballgame.co.kr/", headers={'content-length': '76',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'},data=raw_data).json()
        print(last_round)
        print(now_round)
        print(parse_result)
        if last_round == now_round:
            print('결과처리')
        parse_count = 1
        now_round = last_round + 1
        time.sleep(10)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
