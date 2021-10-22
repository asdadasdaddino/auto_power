import sys
import os
import time
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

import requests
import datetime

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon

form_class = uic.loadUiType(resource_path("untitled.ui"))[0]
global userid, userpw, userkey, balance, now_round, last_round, bet_list
now_round = 0
last_round = 0
bet_list = []

class Thread(QThread):
    # 초기화 메서드 구현
    def __init__(self, parent): #parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
        super().__init__(parent)
        self.parent = parent #self.parent를 사용하여 WindowClass 위젯을 제어할 수 있다.

    def run(self):
        global userid, userpw, userkey, balance, now_round, last_round, bet_list
        textbrowser = self.parent.textBrowser
        #쓰레드로 동작시킬 함수 내용 구현
        # 파워볼 라운드번호 초기화
        while True:
            try:
                time.sleep(3)
                #잔고 확인
                response_bal = requests.get("http://point-900.com:8085/auto/api/user_bal?u="+userid+"&k=" + userkey)
                balance = response_bal.json()['more_info']['wallet']
                self.parent.bal_text.setText("현재 잔고 : "+balance+" 원")

                # 배팅 내역 확인
                if len(bet_list) > 0:
                    self.parent.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                    self.parent.tableWidget.horizontalHeader().setSectionResizeMode(
                        QHeaderView.ResizeToContents)
                    self.parent.tableWidget.setColumnCount(5)
                    self.parent.tableWidget.setRowCount(len(bet_list))
                    self.parent.tableWidget.setHorizontalHeaderLabels([" 회차 ", " 패턴 ", "홀/짝", " 금액 ", " 결과 "])
                    for i in range(len(bet_list)):
                        for j in range(5):
                            self.parent.tableWidget.setItem(i, j, QTableWidgetItem(bet_list[i][j]))

                #파워볼 파싱 시작
                current_time = datetime.datetime.now()
                current_day = current_time.strftime("%Y-%m-%d")
                raw_data = 'view=action&action=ajaxPowerballLog&actionType=dayLog&date='+current_day+'&page=1'
                response_pball_req = requests.post("https://www.powerballgame.co.kr/", headers={'content-length': '76',
                                                                                      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                                         data=raw_data)
                if response_pball_req.status_code == 200:
                    response_pball = response_pball_req.json()
                else:
                    continue
                #이미 확인한 회차인지 판별
                now_round = response_pball['content'][0]['round']
                if now_round == last_round:
                    continue

                #배팅내역에 있다면 결과 처리
                for bet in bet_list:
                    if now_round == bet[0] and bet[4] == '':
                        if bet[2] == response_pball['content'][0]['numberOddEven']:
                            bet[4] = '적중'
                        else:
                            bet[4] = '미적중'

                # 배팅 내역 확인
                if len(bet_list) > 0:
                    self.parent.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                    self.parent.tableWidget.horizontalHeader().setSectionResizeMode(
                        QHeaderView.ResizeToContents)
                    self.parent.tableWidget.setColumnCount(5)
                    self.parent.tableWidget.setRowCount(len(bet_list))
                    self.parent.tableWidget.setHorizontalHeaderLabels([" 회차 ", " 패턴 ", "홀/짝", " 금액 ", " 결과 "])
                    for i in range(len(bet_list)):
                        for j in range(5):
                            self.parent.tableWidget.setItem(i, j, QTableWidgetItem(bet_list[i][j]))

                #패턴1 체크/시작
                if self.parent.checkBox_1.isChecked():
                    if not self.parent.betmoney_1.text().isnumeric():
                        textbrowser.append(datetime.datetime.now().strftime("[%m-%d %H:%M:%S] ") + "경고!! 패턴1 배팅금액을 확인해주세요.")
                        textbrowser.verticalScrollBar().setValue(textbrowser.verticalScrollBar().maximum())
                        time.sleep(10)
                        continue
                    else:
                        bet_money = self.parent.betmoney_1.text()
                    #최근결과 포함 6회차의 결과 필요
                    if len(response_pball['content']) > 6:
                        ball_list = response_pball['content'][0]['number'].split(',')
                        ball_list2 = response_pball['content'][1]['number'].split(',')
                        ball_list3 = response_pball['content'][2]['number'].split(',')
                        ball_list4 = response_pball['content'][3]['number'].split(',')
                        ball_list5 = response_pball['content'][4]['number'].split(',')
                        ball_list6 = response_pball['content'][5]['number'].split(',')

                        #(3차 조건) 마지막 회차의 왼쪽합/오른쪽합이 홀/홀: 인 경우
                        if (int(ball_list[0]) + int(ball_list[1])) % 2 == 1 and (int(ball_list[3]) + int(ball_list[4])) % 2 == 1:
                            left_sum = (int(ball_list2[0]) + int(ball_list3[0]) + int(ball_list4[0]) + int(
                                ball_list5[0]) + int(ball_list2[1]) + int(ball_list3[1]) + int(ball_list4[1]) + int(
                                ball_list5[1]))
                            right_sum = (int(ball_list2[3]) + int(ball_list3[3]) + int(ball_list4[3]) + int(
                                ball_list5[3]) + int(ball_list2[4]) + int(ball_list3[4]) + int(ball_list4[4]) + int(
                                ball_list5[4]))
                            # (2차 조건) 짝/짝:홀 인 경우
                            if left_sum%2 == 0 and right_sum%2 == 0 and response_pball['content'][0]['numberOddEven'] == 'odd':
                                left_sum1 = (int(ball_list6[0]) + int(ball_list3[0]) + int(ball_list4[0]) + int(
                                    ball_list5[0]) + int(ball_list6[1]) + int(ball_list3[1]) + int(ball_list4[1]) + int(
                                    ball_list5[1]))
                                right_sum1 = (int(ball_list6[3]) + int(ball_list3[3]) + int(ball_list4[3]) + int(
                                    ball_list5[3]) + int(ball_list6[4]) + int(ball_list3[4]) + int(ball_list4[4]) + int(
                                    ball_list5[4]))
                                # (1차 조건) 홀/홀:홀 or 짝/짝:짝 인 경우
                                if (left_sum1 % 2 == 0 and right_sum1 % 2 == 0 and response_pball['content'][1][
                                    'numberOddEven'] == 'even') or (
                                        left_sum1 % 2 == 1 and right_sum1 % 2 == 1 and response_pball['content'][1][
                                    'numberOddEven'] == 'odd'):
                                    # 모든 조건 만족 홀 배팅
                                    bet_round = int(now_round) + 1
                                    response_bet = requests.get(
                                        "http://point-900.com:8085/api/bet?userid=" + userid + "&key=" + userkey + "&gm=PWB&tdate="+current_time.strftime("%Y%m%d")+"&rno="+str(bet_round)+"&origin=auto&pp5="+str(bet_money)).json()
                                    if response_bet['comment'] == 'ok':
                                        #배팅내역 추가
                                        bet_list.append([str(bet_round), '패턴1', 'odd', bet_money, ''])
                                        textbrowser.append(datetime.datetime.now().strftime("[%m-%d %H:%M:%S] ")+"패턴1 매칭. "+str(bet_round)+"회차 홀 "+bet_money+"원 배팅 완료.")
                                        textbrowser.verticalScrollBar().setValue(textbrowser.verticalScrollBar().maximum())
                                        last_round = now_round
                                    else:
                                        #배팅 실패 오류 확인
                                        textbrowser.append(
                                            datetime.datetime.now().strftime("[%m-%d %H:%M:%S] ") + "패턴1 매칭 / 배팅실패. 이유: "+response_bet['comment'])
                                        textbrowser.verticalScrollBar().setValue(
                                            textbrowser.verticalScrollBar().maximum())
                                        pass

                        # (3차 조건-2) 마지막 회차의 왼쪽합/오른쪽합이 짝/짝: 인 경우
                        if (int(ball_list[0]) + int(ball_list[1])) % 2 == 0 and (
                                int(ball_list[3]) + int(ball_list[4])) % 2 == 0:
                            left_sum = (int(ball_list2[0]) + int(ball_list3[0]) + int(ball_list4[0]) + int(
                                ball_list5[0]) + int(ball_list2[1]) + int(ball_list3[1]) + int(
                                ball_list4[1]) + int(
                                ball_list5[1]))
                            right_sum = (int(ball_list2[3]) + int(ball_list3[3]) + int(ball_list4[3]) + int(
                                ball_list5[3]) + int(ball_list2[4]) + int(ball_list3[4]) + int(
                                ball_list4[4]) + int(
                                ball_list5[4]))
                            # (2차 조건) 홀/홀:짝 인 경우
                            if left_sum % 2 == 1 and right_sum % 2 == 1 and response_pball['content'][0][
                                'numberOddEven'] == 'even':
                                left_sum1 = (int(ball_list6[0]) + int(ball_list3[0]) + int(
                                    ball_list4[0]) + int(
                                    ball_list5[0]) + int(ball_list6[1]) + int(ball_list3[1]) + int(
                                    ball_list4[1]) + int(
                                    ball_list5[1]))
                                right_sum1 = (int(ball_list6[3]) + int(ball_list3[3]) + int(
                                    ball_list4[3]) + int(
                                    ball_list5[3]) + int(ball_list6[4]) + int(ball_list3[4]) + int(
                                    ball_list4[4]) + int(
                                    ball_list5[4]))
                                # (1차 조건) 홀/홀:홀 or 짝/짝:짝 인 경우
                                if (left_sum1 % 2 == 0 and right_sum1 % 2 == 0 and
                                    response_pball['content'][1][
                                        'numberOddEven'] == 'even') or (
                                        left_sum1 % 2 == 1 and right_sum1 % 2 == 1 and
                                        response_pball['content'][1][
                                            'numberOddEven'] == 'odd'):
                                    # 모든 조건 만족 짝 배팅
                                    bet_round = int(now_round) + 1
                                    response_bet = requests.get(
                                        "http://point-900.com:8085/api/bet?userid=" + userid + "&key=" + userkey + "&gm=PWB&tdate=" + current_time.strftime(
                                            "%Y%m%d") + "&rno=" + str(bet_round) + "&origin=auto&pp6=" + str(
                                            bet_money)).json()
                                    if response_bet['comment'] == 'ok':
                                        # 배팅내역 추가
                                        bet_list.append([str(bet_round), '패턴1', 'even', bet_money, ''])
                                        textbrowser.append(
                                            datetime.datetime.now().strftime("[%m-%d %H:%M:%S] ") + "패턴1 매칭. " + str(
                                                bet_round) + "회차 짝 " + bet_money + "원 배팅 완료.")
                                        textbrowser.verticalScrollBar().setValue(
                                            textbrowser.verticalScrollBar().maximum())
                                        last_round = now_round
                                    else:
                                        # 배팅 실패 오류 확인
                                        textbrowser.append(
                                            datetime.datetime.now().strftime(
                                                "[%m-%d %H:%M:%S] ") + "패턴1 매칭 / 배팅실패. 이유: " + response_bet['comment'])
                                        textbrowser.verticalScrollBar().setValue(
                                            textbrowser.verticalScrollBar().maximum())
                                        continue

                #패턴2 체크/시작
                if self.parent.checkBox_2.isChecked():
                    if not self.parent.betmoney_2.text().isnumeric():
                        textbrowser.append(datetime.datetime.now().strftime(
                            "[%m-%d %H:%M:%S] ") + "경고!! 패턴2 배팅금액을 확인해주세요.")
                        textbrowser.verticalScrollBar().setValue(
                            textbrowser.verticalScrollBar().maximum())
                        time.sleep(10)
                        continue
                    else:
                        bet_money = self.parent.betmoney_2.text()
                    # 최근결과 포함 1회차의 결과 필요
                    if len(response_pball['content']) > 1:
                        ball_list = response_pball['content'][0]['number'].split(',')

                        # (조건) 마지막 회차 홀 인 경우
                        if response_pball['content'][0]['numberOddEven'] == 'odd':
                            # 모든 조건 만족 짝 배팅
                            bet_round = int(now_round) + 1
                            response_bet = requests.get(
                                "http://point-900.com:8085/api/bet?userid=" + userid + "&key=" + userkey + "&gm=PWB&tdate=" + current_time.strftime(
                                    "%Y%m%d") + "&rno=" + str(
                                    bet_round) + "&origin=auto&pp6=" + str(bet_money)).json()
                            if response_bet['comment'] == 'ok':
                                # 배팅내역 추가
                                bet_list.append([str(bet_round), '패턴2', 'even', bet_money, ''])
                                textbrowser.append(datetime.datetime.now().strftime(
                                    "[%m-%d %H:%M:%S] ") + "패턴2 매칭. " + str(
                                    bet_round) + "회차 짝 " + bet_money + "원 배팅 완료.")
                                textbrowser.verticalScrollBar().setValue(
                                    textbrowser.verticalScrollBar().maximum())
                                last_round = now_round
                            else:
                                # 배팅 실패 오류 확인
                                textbrowser.append(
                                    datetime.datetime.now().strftime(
                                        "[%m-%d %H:%M:%S] ") + "패턴2 매칭 / 배팅실패. 이유: " +
                                    response_bet['comment'])
                                textbrowser.verticalScrollBar().setValue(
                                    textbrowser.verticalScrollBar().maximum())
                                pass

                        # (조건) 마지막 회차 짝 인 경우
                        if response_pball['content'][0]['numberOddEven'] == 'even':
                            # 모든 조건 만족 홀 배팅
                            bet_round = int(now_round) + 1
                            response_bet = requests.get(
                                "http://point-900.com:8085/api/bet?userid=" + userid + "&key=" + userkey + "&gm=PWB&tdate=" + current_time.strftime(
                                    "%Y%m%d") + "&rno=" + str(
                                    bet_round) + "&origin=auto&pp5=" + str(bet_money)).json()
                            if response_bet['comment'] == 'ok':
                                # 배팅내역 추가
                                bet_list.append([str(bet_round), '패턴2', 'odd', bet_money, ''])
                                textbrowser.append(datetime.datetime.now().strftime(
                                    "[%m-%d %H:%M:%S] ") + "패턴2 매칭. " + str(
                                    bet_round) + "회차 홀 " + bet_money + "원 배팅 완료.")
                                textbrowser.verticalScrollBar().setValue(
                                    textbrowser.verticalScrollBar().maximum())
                                last_round = now_round
                            else:
                                # 배팅 실패 오류 확인
                                textbrowser.append(
                                    datetime.datetime.now().strftime(
                                        "[%m-%d %H:%M:%S] ") + "패턴2 매칭 / 배팅실패. 이유: " +
                                    response_bet['comment'])
                                textbrowser.verticalScrollBar().setValue(
                                    textbrowser.verticalScrollBar().maximum())
                                pass
                time.sleep(10)
            except:
                pass

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # 백그라운드에서 돌아갈 쓰레드 하나 생성
        self.Th1 = Thread(self)

        #기능을 연결하는 코드
        self.start_btn.clicked.connect(self.start_btn_Function)


    #start_btn이 눌리면 작동할 함수
    def start_btn_Function(self):
        global userid, userpw, userkey, balance
        userid = self.input_id.text()
        userpw = self.input_pw.text()
        if self.start_btn.text() == "시작":
            # 시간검사(유료)
            if int(datetime.datetime.now().strftime("%m%d")) > 1120:
                QMessageBox.critical(self, "네트워크 오류", "제품등록을 확인해주세요.")
            # id/pw 검증
            elif userid =="" or userpw=="":
                QMessageBox.critical(self,"로그인 오류","ID/PW를 입력해주세요.")

            # 로그인 시작
            else:
                response_login = requests.get(
                    "http://point-900.com:8085/auto/api/user_auth?u="+userid+"&p="+userpw+"&v=1.4.1")
                if response_login.status_code == 200:
                    response_login_data = response_login.json()
                    # 로그인 상태 확인
                    if response_login_data['code'] != 1:
                        QMessageBox.critical(self, "로그인 실패", "ID/PW를 확인해주세요.")
                    else:
                        self.textBrowser.append(datetime.datetime.now().strftime("[%m-%d %H:%M:%S] ")+"배팅을 시작합니다.")
                        userkey = response_login_data['more_info']['key']
                        self.start_btn.setText("정지")
                        if self.Th1.isRunning():
                            self.Th1.terminate()
                            self.Th1.wait()
                            self.Th1.start()
                        else:
                            self.Th1.start()
                else:
                    QMessageBox.critical(self, "사이트 접속 실패", "사이트 상태를 확인해주세요.")

        else:
            self.textBrowser.append(datetime.datetime.now().strftime("[%m-%d %H:%M:%S] ")+"배팅을 정지합니다.")
            self.start_btn.setText("시작")
            if self.Th1.isRunning():
                self.Th1.terminate()
                self.Th1.wait()

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    myWindow.setWindowTitle("파워볼 패턴 오토프로그램")
    myWindow.setWindowIcon(QIcon(resource_path('auto.png')))
    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()