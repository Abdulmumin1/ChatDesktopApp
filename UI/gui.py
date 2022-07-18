from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit,
                             QVBoxLayout, QFrame, QMainWindow, QHBoxLayout, QLabel, QScrollArea, QTextEdit)
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
import threading
import time


import client as cl
from utils import break_sentence, json_constructor
import json

colors = {
    'primary': '#011110',
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
            msg = client.client.recv(1024).decode('utf-8')
            print(msg)
            if not msg:
                self.alerts.emit('Error')
                self.continue_run = False

            msg_json = json.loads(msg)
            if msg_json['type'] == 'alert':
                self.alerts.emit(msg_json['message'])
            elif msg_json['type'] == 'message':
                self.finished.emit(msg)


class Chats(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f'background:{colors["primary"]}; border:0px;')
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)
        self.layout.addStretch(1)

    def append_msg(self, you, widget):
        self.layout.insertWidget(self.layout.count()-1,
                                 widget, alignment=Qt.AlignLeft if you else Qt.AlignRight)


class AlertFrame(QFrame):
    def __init__(self, msg):
        super().__init__()
        layout = QHBoxLayout()

        self.setStyleSheet(
            'QFrame{background:#011110; border:1.2px solid teal;' +
            'margin-left:7px; margin-right:7px; border-radius:6px;}')

        label = QLabel(f'<em>{msg}!</em>')
        label.setStyleSheet('border:0;')
        close_ = QPushButton('x', clicked=self.deleteLater)
        close_.setStyleSheet(f'border:0; background:{colors["primary"]}')
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(close_)

        self.setLayout(layout)


class ChatMsg(QFrame):
    def __init__(self, sender, message):
        super().__init__()
        """message frame"""

        # load the json data that is passed

        name = sender
        message = message

        colors = (('#D0F7F7', 'black', 'teal'),
                  ('#242627', 'white', '#D0F7F7'))
        color = colors[0] if name == my_name else colors[1]
        text_color = color[1]
        sender_color = color[2]

        # color = 'blue' if name == sender else 'gray'
        frame_style = f'border-radius:7px; background:{color[0]}; color:{text_color};'
        self.setStyleSheet('QFrame{'+frame_style+'}')
        layout = QVBoxLayout()
        # set username to you if it the senders message
        sender = QLabel(text=name if name != my_name else 'You.')
        sender.setStyleSheet(f'color:{sender_color};')
        message = break_sentence(message)
        msg = QLabel(text=message)
        msg.setWordWrap(True)

        layout.addWidget(sender)
        layout.addWidget(msg)
        layout.addStretch(1)
        self.setLayout(layout)


class MsgBox(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('max-height:50px;')

        layout = QHBoxLayout()
        chat_frame = Chats()

        self.msg = QTextEdit()

        self.msg.setStyleSheet(
            'QTextEdit{border:0px; border-bottom:2px solid teal; border-radius:2px; background:#011110;}'+scroll_var+scroll_hor)
        self.msg.setPlaceholderText('message -> Html tags can also be used')

        self.msg.setCursorWidth(5)
        self.msg.setFocus()
        # self.msg.setMaximumWidth(70)
        # self.msg.cursorWidth(3)

        attachment = QPushButton('📌')

        self.send_btn = QPushButton(
            text='⇛', clicked=self.send_msg)

        self.send_btn.setStyleSheet(
            'background:teal;  width:60px;border-radius:11px; font-size:22px;padding:6px;')

        layout.addWidget(self.msg)
        layout.addWidget(attachment, alignment=Qt.AlignRight)
        layout.addWidget(self.send_btn, alignment=Qt.AlignRight)
        self.setLayout(layout)

    def send_msg(self):
        message = self.msg.toPlainText()
        if message:
            data = json_constructor('message', message, sender=my_name)
            client.client.send(
                bytes(data, encoding='utf-8'))

            self.msg.setPlainText('')
            self.msg.setFocus()


class JoinFrame(QFrame):

    def __init__(self):
        super().__init__()
        self.start_thread = None
        self.change_frame = None

        layout = QVBoxLayout()
        ip_addr = QLineEdit()
        ip_addr.setMaxLength(16)
        ip_addr.setPlaceholderText('Enter IP address')

        username = QLineEdit()
        username.setMaxLength(20)
        username.setPlaceholderText('Enter username!')

        self.join_button = QPushButton(
            text='Join', clicked=lambda: self.join_(username.text(), ip_addr.text()))

        layout.addStretch(1)
        layout.addWidget(ip_addr)
        layout.addWidget(username)
        layout.addWidget(self.join_button, )
        layout.addStretch(1)

        self.setLayout(layout)

    def join_(self, name, ip):
        if not (name and ip):
            return
        # set username and ip address to datas entered
        # start the recieve message thread
        # change the frame to chat frame and discard this frame
        global client, my_name
        my_name = name
        try:
            client = cl.Client(ip)
        except:
            return
        name_req = client.client.recv(1024).decode('ascii')
        client.client.send(name.encode('utf-8'))

        self.start_thread()
        self.change_frame()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f'background:{colors["primary"]}; color:white;')

        # display join frame
        joinframe = JoinFrame()

        # callbacks functions
        joinframe.start_thread = self.create_threads
        joinframe.change_frame = self.initChatUI

        self.setCentralWidget(joinframe)

    def initChatUI(self):
        main_frame = QFrame()
        self.main_layout = QVBoxLayout(main_frame)

        # Chats frame
        self.chat_frame = Chats()
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(
            "QScrollArea{border:0px;}"+scroll_hor+scroll_var)
        scroll_area.setWidgetResizable(True)
        # scroll_area.horizontalScrollBar().setDisabled(True)
        scroll_area.setWidget(self.chat_frame)

        # message inputs frame
        msg_box = MsgBox()

        self.main_layout.addWidget(scroll_area)
        self.main_layout.addWidget(msg_box)

        self.setCentralWidget(main_frame)

    def create_threads(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.receive_msg)

        self.worker.alerts.connect(self.display_alerts)
        self.worker.finished.connect(self.display_msg)
        self.thread.start()

    def display_msg(self, message):
        # decompose the message
        message = json.loads(message)

        msg = ChatMsg(message['sender'], message['message'])
        # True if you are not the sender else false
        # this is to align the message either at the left or right

        AlignLeft = True
        if message['sender'] == my_name:
            AlignLeft = False
        self.chat_frame.append_msg(AlignLeft, msg)

    def display_alerts(self, alert):
        # display the alert frame and start a thread to wait for
        # some seconds and get rid of the alert frame
        alertFrame = AlertFrame(alert)

        athread = threading.Thread(target=self.kill_alert, args=(alertFrame,))
        athread.start()

        self.main_layout.insertWidget(0, alertFrame)

    def kill_alert(self, frame):
        time.sleep(3)
        frame.hide()
        frame.deleteLater()

    def closeEvent(self, event):
        # destroy threads and close client on window close
        if client:
            # send a leave signal
            message = json.dumps({'type': 'leave'})
            client.client.send(bytes(message, encoding='utf-8'))

            client.client.close()
            # self.athread.
            self.worker.continue_run = False
            self.thread.quit()
            self.worker.deleteLater()
            self.thread.deleteLater()
        print('closed')


def main():
    app = QApplication([])
    win = Main()

    # win.thread.start()
    win.show()
    app.exec_()


if __name__ == '__main__':
    my_name = None
    ip_addr = None
    client = None

    main()
