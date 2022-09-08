# coding:utf-8
import PyQt5
import pyperclip
import sys
import ClipTool
from PyQt5.QtWidgets import QApplication, QMainWindow
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtGui, QtWidgets
from tools import *
from FunPatterns import *
import FunPatterns
class ClipBoardThread(QThread):
    """
    异步获取剪切板到控件上
    """
    clipboard_signal = pyqtSignal(str)

    def __init__(self):
        super(ClipBoardThread, self).__init__()

    def get_clipborad(self):
        """获取剪贴板数据"""
        return pyperclip.paste()


    def run(self):
        """开始记录"""
        while True:
            recent_clipborad = self.get_clipborad()
            while True:
                # txt 存放当前剪切板文本
                clipborad = self.get_clipborad()
                # 剪切板内容和上一次对比如有变动，再进行内容判断，判断后如果发现有指定字符在其中的话，再执行替换
                if clipborad != recent_clipborad:
                    recent_clipborad = clipborad  # 没查到要替换的子串，返回None
                    self.clipboard_signal.emit(recent_clipborad)
                    break
                    # 检测间隔（延迟0.2秒）
                time.sleep(0.2)

class MainDialog(QMainWindow):


    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.ui = ClipTool.Ui_MainWindow()
        self.ui.setupUi(self)

        # 添加快捷添加控件
        patterns=get_module_functions(FunPatterns)
        self.ui.pushButton_patterns=[]
        i=0
        for pattern in patterns:
            i+=1
            pushButton_pattern=QtWidgets.QPushButton(self.ui.centralwidget)
            font = QtGui.QFont()
            font.setPointSize(12)
            pushButton_pattern.setFont(font)
            # pushButton_pattern.setMaximumWidth(100)  # 设置宽度
            # pattern="\n".join(cut_data_ave(pattern,6))
            pushButton_pattern.setText(pattern)
            pushButton_pattern.setShortcut('Ctrl+'+str(i))
            pushButton_pattern.clicked.connect(lambda: self.str_change_pattern(self.sender().text()))
            self.ui.verticalLayout_patterns.addWidget(pushButton_pattern)
            self.ui.pushButton_patterns.append(pushButton_pattern)


        # 绑定按键响应
        self.ui.lineEdit_cmd.textChanged.connect(self.command2)
        self.ui.lineEdit_cmd.returnPressed.connect(self.command)
        # 绑定线程响应
        self.cbthread=ClipBoardThread()
        self.cbthread.clipboard_signal.connect(self.get_clipboard)
        self.cbthread.start()


    def str_change_pattern(self,pattern):
        history=self.ui.plainTextEdit_history.toPlainText()
        paste_str=self.ui.plainTextEdit_paste.toPlainText()
        if not paste_str:return
        paste_str=paste_str.replace("\n","\\n")
        info=eval(pattern+"('"+paste_str+"')")
        if not isinstance(info,str):
            pyperclip.copy("pattern返回格式不是字符串！")
            return
        pyperclip.copy(info)
        self.ui.plainTextEdit_history.setPlainText(history+"\n"+info)


    def command(self):
        command_str=self.ui.lineEdit_cmd.text()
        if command_str in ["clear","c"]:
            self.ui.plainTextEdit_history.setPlainText("")
        self.ui.lineEdit_cmd.setText("")

    def command2(self):
        msg = self.ui.lineEdit_cmd.text()  # 首先在这里拿到文本框内容
        # 这里写后续工作可能用到的方法
        return


    def get_clipboard(self,info):
        self.ui.plainTextEdit_paste.setPlainText(info)


# 添加快捷输入，源字符串加另一个字符串，即改变字符串格式


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.setWindowFlags(PyQt5.QtCore.Qt.WindowMinimizeButtonHint |  # 使能最小化按钮
                         PyQt5.QtCore.Qt.WindowCloseButtonHint |  # 使能关闭按钮
                         PyQt5.QtCore.Qt.WindowStaysOnTopHint)  # 窗体总在最前端
    myDlg.show()


    sys.exit(myapp.exec_())