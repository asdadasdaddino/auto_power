import sys
import time
import requests
import datetime

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

form_class = uic.loadUiType("untitled.ui")[0]
global userid, userpw, userkey, balance

class Thread(QThread):
    # 초기화 메서드 구현
    def __init__(self, parent): #parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
        super().__init__(parent)
        self.parent = parent #self.parent를 사용하여 WindowClass 위젯을 제어할 수 있다.

    def run(self):
        textbrowser = self.parent.textBrowser
        #쓰레드로 동작시킬 함수 내용 구현
        # 파워볼 결과 파싱할때 가져올 페이지 시작번호
        parse_count = 1
        # 파워볼 라운드번호 초기화
        now_round = 0
        last_round = 0
        while True:
            try:
                #잔고 확인
                response_bal = requests.get("http://point-900.com:8085/auto/api/user_bal?u="+userid+"&k=" + userkey)
                balance = response_bal.json()['more_info']['wallet']
                self.parent.bal_text.setText("현재 잔고 : "+balance+" 원")

                #파워볼 파싱 시작
                current_time = datetime.datetime.now()
                current_day = current_time.strftime("%Y-%m-%d")
                raw_data = 'view=action&action=ajaxPowerballLog&actionType=dayLog&date='+current_day+'&page=' + str(
                    parse_count)
                response_pball = requests.post("https://www.powerballgame.co.kr/", headers={'content-length': '76',
                                                                                      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                                         data=raw_data).json()
                #패턴1 체크/시작
                if self.parent.checkBox_1.isChecked():

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
                                    print("패턴1 베팅")
                                    print()
                                    textbrowser.append(datetime.datetime.now().strftime("[%m-%d %H:%M:%S] ")+"패턴1 직전회차 홀..")
                                    textbrowser.verticalScrollBar().setValue(textbrowser.verticalScrollBar().maximum())

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
                                    print("패턴1 베팅")
                                    textbrowser.append(datetime.datetime.now().strftime(
                                        "[%m-%d %H:%M:%S] ") + "패턴1 직전회차 홀..")
                                    textbrowser.verticalScrollBar().setValue(
                                        textbrowser.verticalScrollBar().maximum())
                time.sleep(100)
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
            # id/pw 검증
            if userid =="" or userpw=="":
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
                        self.textBrowser.append(datetime.datetime.now().strftime("[%m-%d %H:%M:%S] ")+"베팅을 시작합니다.")
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
            self.textBrowser.append(datetime.datetime.now().strftime("[%m-%d %H:%M:%S] ")+"베팅을 정지합니다.")
            self.start_btn.setText("시작")
            if self.Th1.isRunning():
                self.Th1.terminate()
                self.Th1.wait()

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()