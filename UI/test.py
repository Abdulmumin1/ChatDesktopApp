from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit,
                             QVBoxLayout, QFrame, QMainWindow, QHBoxLayout, QLabel, QScrollArea, QTextEdit)
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
import json
import os
# import client


# my_name = input()
# client = client.Client()
# name_req = client.client.recv(1024).decode('ascii')
# print(name_req)
# client.client.send(my_name.encode('ascii'))

colors = {
    'primary': '#000F14',
}


scroll_var = """QScrollBar::vertical{width:6px;}
        QScrollBar::handle:vertical{background:#333; min-height:0px;}
        QScrollBar::handle:vertical:active{background:gray; border-radius:5px;}
        QScrollBar::add-line:vertical{height:0px;}
        QScrollBar::sub-line:vertical{height:0px;}
        """
scroll_hor = """QScrollBar::horizontal{height:6px;}
        QScrollBar::handle:horizontal{background:#333; min-height:0px;}
        QScrollBar::handle:horizontal:active{background:gray; border-radius:5px;}
        QScrollBar::add-line:horizontal{height:0px;}
        QScrollBar::sub-line:horizontal{height:0px;}
        """


class Worker(QObject):
    finished = pyqtSignal(str)
    alerts = pyqtSignal(str)

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.continue_run = True

    def receive_msg(self):
        while self.continue_run:
            msg = client.client.recv(1024).decode('ascii')
            print(msg)
            # if not msg:
            #     self.continue_run = False
            if not msg:
                self.alerts.emit('Error')
                self.continue_run = False
            if msg.startswith(':gg$#'):
                self.alerts.emit(msg[5:])
            else:
                print(msg)
                self.finished.emit(msg)


class Chats(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f'background:{colors["primary"]}; border:0px;')
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)

    def append_msg(self, you, widget):

        self.layout.addWidget(
            widget, alignment=Qt.AlignLeft if you else Qt.AlignRight)


class ChatMsg(QFrame):
    def __init__(self, data):
        super().__init__()
        name, message = data.split('::43$*()')
        color = '#D0F7F7' if name == my_name else '#222'
        self.setStyleSheet(
            'height:auto; border-radius:6px; background:;')

        layout = QVBoxLayout()

        sender = QLabel(text=name)
        msg = QLabel(
            text=message)

        msg.setWordWrap(True)

        layout.addWidget(sender)
        layout.addWidget(msg)
        layout.addStretch(1)
        self.setLayout(layout)


class MsgBox(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('max-height:120px;')
        layout = QHBoxLayout()
        chat_frame = Chats()

        self.msg = QTextEdit()
        # 5A6362
        # D0F7F7
        self.msg.setStyleSheet(
            f'border:0px; border-bottom:1px solid teal;  background:{colors["primary"]};')
        self.send_btn = QPushButton(
            text='send', clicked=self.send_msg)

        self.send_btn.setStyleSheet(
            'background:teal;  width:60px;border-radius:11px; padding:4px;')

        layout.addWidget(self.msg)
        layout.addWidget(self.send_btn)
        self.setLayout(layout)

    def send_msg(self):
        pass
        # print('send')
        # client.client.send(
        #     f"{my_name}::43$*(){self.msg.toPlainText()}".encode('ascii'))
        # print('sent')


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(f'background:{colors["primary"]};')

        main_frame = QFrame()
        main_layout = QVBoxLayout(main_frame)

        self.chat_frame = Chats()
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(
            "QScrollArea{border:0px;}"+scroll_hor+scroll_var)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.chat_frame)

        msg_box = MsgBox()

        main_layout.addWidget(scroll_area)
        main_layout.addWidget(msg_box)
        self.setCentralWidget(main_frame)

    #     self.thread = QThread()
    #     self.worker = Worker()
    #     self.worker.moveToThread(self.thread)

    #     self.thread.started.connect(self.worker.receive_msg)

    #     self.worker.alerts.connect(self.display_alerts)
    #     self.worker.finished.connect(self.display_msg)

    # def display_msg(self, message):
    #     msg = ChatMsg(message)
    #     self.chat_frame.append_msg(
    #         True if my_name != message.split('::43$*()')[0] else False, msg)

    # def display_alerts(self, alert):
    #     print(alert)

    # def closeEvent(self, event):
    #     client.client.close()
    #     self.thread.quit()
    #     self.worker.deleteLater()
    #     self.thread.deleteLater()
    #     print('closed')


def main():
    app = QApplication([])
    if os.path.exists('state.json'):

        data = json.load('state.json')
        try:
            win = data.cls
        except:
            win = Main()
    else:
        win = Main()
    # win.thread.start()
    win.show()
    app.exec_()


def pnew():
    print(new)


new = 'abdul'
if __name__ == '__main__':
    pnew()
    # main()
    # json.dumps(open('state.json', 'w'), {'cls': Main()})
