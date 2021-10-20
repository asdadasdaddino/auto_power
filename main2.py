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
                current_time = datetime.now()
                current_day = current_time.strftime("%Y-%M-%d")
                raw_data = 'view=action&action=ajaxPowerballLog&actionType=dayLog&date='+current_day+'&page=' + str(
                    parse_count)
                response_pball = requests.post("https://www.powerballgame.co.kr/", headers={'content-length': '76',
                                                                                      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                                         data=raw_data).json()

                time.sleep(1000)
                textbrowser.append("백그라운드 동작중..")
                # textbrowser.verticalScrollBar().setValue(textbrowser.verticalScrollBar().maximum())
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
                        self.textBrowser.append("로그인 성공!")
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
            self.textBrowser.append("정지 클릭")
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