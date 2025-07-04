# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListView, QPushButton, QSizePolicy,
    QTabWidget, QTableView, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(922, 650)
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_11 = QHBoxLayout(self.tab)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_Port = QGroupBox(self.tab)
        self.groupBox_Port.setObjectName(u"groupBox_Port")
        self.groupBox_Port.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.groupBox_Port)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox_Port)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBox_Protocol = QComboBox(self.groupBox_Port)
        self.comboBox_Protocol.addItem("")
        self.comboBox_Protocol.addItem("")
        self.comboBox_Protocol.addItem("")
        self.comboBox_Protocol.addItem("")
        self.comboBox_Protocol.setObjectName(u"comboBox_Protocol")

        self.horizontalLayout.addWidget(self.comboBox_Protocol)

        self.lineEdit_Address = QLineEdit(self.groupBox_Port)
        self.lineEdit_Address.setObjectName(u"lineEdit_Address")

        self.horizontalLayout.addWidget(self.lineEdit_Address)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.groupBox_Port)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(self.groupBox_Port)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_2.addWidget(self.lineEdit_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_ClientID = QLabel(self.groupBox_Port)
        self.label_ClientID.setObjectName(u"label_ClientID")

        self.horizontalLayout_3.addWidget(self.label_ClientID)

        self.lineEdit_6 = QLineEdit(self.groupBox_Port)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.horizontalLayout_3.addWidget(self.lineEdit_6)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.groupBox_Port)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_UserName = QLineEdit(self.groupBox_Port)
        self.lineEdit_UserName.setObjectName(u"lineEdit_UserName")

        self.horizontalLayout_4.addWidget(self.lineEdit_UserName)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_PassWord = QLabel(self.groupBox_Port)
        self.label_PassWord.setObjectName(u"label_PassWord")

        self.horizontalLayout_5.addWidget(self.label_PassWord)

        self.lineEdit_5 = QLineEdit(self.groupBox_Port)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.horizontalLayout_5.addWidget(self.lineEdit_5)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.pushButton_Open = QPushButton(self.groupBox_Port)
        self.pushButton_Open.setObjectName(u"pushButton_Open")

        self.verticalLayout.addWidget(self.pushButton_Open)


        self.verticalLayout_6.addWidget(self.groupBox_Port)

        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listView_Subscription = QListView(self.groupBox_2)
        self.listView_Subscription.setObjectName(u"listView_Subscription")

        self.verticalLayout_2.addWidget(self.listView_Subscription)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.lineEdit_Subscription = QLineEdit(self.groupBox_2)
        self.lineEdit_Subscription.setObjectName(u"lineEdit_Subscription")

        self.horizontalLayout_6.addWidget(self.lineEdit_Subscription)

        self.pushButton_AddSubscription = QPushButton(self.groupBox_2)
        self.pushButton_AddSubscription.setObjectName(u"pushButton_AddSubscription")

        self.horizontalLayout_6.addWidget(self.pushButton_AddSubscription)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.verticalLayout_6.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(self.tab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.textEdit_Send = QTextEdit(self.groupBox_4)
        self.textEdit_Send.setObjectName(u"textEdit_Send")

        self.verticalLayout_5.addWidget(self.textEdit_Send)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.comboBox_Subscription = QComboBox(self.groupBox_4)
        self.comboBox_Subscription.setObjectName(u"comboBox_Subscription")

        self.horizontalLayout_7.addWidget(self.comboBox_Subscription)

        self.pushButton_Send = QPushButton(self.groupBox_4)
        self.pushButton_Send.setObjectName(u"pushButton_Send")

        self.horizontalLayout_7.addWidget(self.pushButton_Send)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)


        self.verticalLayout_6.addWidget(self.groupBox_4)


        self.horizontalLayout_11.addLayout(self.verticalLayout_6)

        self.groupBox_3 = QGroupBox(self.tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.textEdit_Received = QTextEdit(self.groupBox_3)
        self.textEdit_Received.setObjectName(u"textEdit_Received")

        self.verticalLayout_3.addWidget(self.textEdit_Received)


        self.horizontalLayout_11.addWidget(self.groupBox_3)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_11 = QVBoxLayout(self.tab_2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.groupBox_5 = QGroupBox(self.tab_2)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout_18 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_6 = QLabel(self.groupBox_5)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_12.addWidget(self.label_6)

        self.comboBox_model = QComboBox(self.groupBox_5)
        self.comboBox_model.addItem("")
        self.comboBox_model.addItem("")
        self.comboBox_model.addItem("")
        self.comboBox_model.addItem("")
        self.comboBox_model.setObjectName(u"comboBox_model")

        self.horizontalLayout_12.addWidget(self.comboBox_model)


        self.verticalLayout_7.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_9 = QLabel(self.groupBox_5)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_13.addWidget(self.label_9)

        self.doubleSpinBox_1 = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_1.setObjectName(u"doubleSpinBox_1")
        self.doubleSpinBox_1.setMaximum(200.000000000000000)

        self.horizontalLayout_13.addWidget(self.doubleSpinBox_1)


        self.verticalLayout_7.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_10 = QLabel(self.groupBox_5)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_14.addWidget(self.label_10)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setMaximum(1.000000000000000)

        self.horizontalLayout_14.addWidget(self.doubleSpinBox_2)


        self.verticalLayout_7.addLayout(self.horizontalLayout_14)


        self.horizontalLayout_18.addLayout(self.verticalLayout_7)

        self.line = QFrame(self.groupBox_5)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_18.addWidget(self.line)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_11 = QLabel(self.groupBox_5)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_15.addWidget(self.label_11)

        self.doubleSpinBox_3 = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setMaximum(200.000000000000000)

        self.horizontalLayout_15.addWidget(self.doubleSpinBox_3)


        self.verticalLayout_8.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_12 = QLabel(self.groupBox_5)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_16.addWidget(self.label_12)

        self.doubleSpinBox_4 = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_4.setObjectName(u"doubleSpinBox_4")
        self.doubleSpinBox_4.setMaximum(1.000000000000000)

        self.horizontalLayout_16.addWidget(self.doubleSpinBox_4)


        self.verticalLayout_8.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_13 = QLabel(self.groupBox_5)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_17.addWidget(self.label_13)

        self.doubleSpinBox_5 = QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_5.setObjectName(u"doubleSpinBox_5")
        self.doubleSpinBox_5.setMaximum(200.000000000000000)

        self.horizontalLayout_17.addWidget(self.doubleSpinBox_5)


        self.verticalLayout_8.addLayout(self.horizontalLayout_17)


        self.horizontalLayout_18.addLayout(self.verticalLayout_8)


        self.verticalLayout_11.addWidget(self.groupBox_5)

        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 150))
        self.horizontalLayout_21 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.widget_state = QWidget(self.groupBox)
        self.widget_state.setObjectName(u"widget_state")
        self.widget_state.setMinimumSize(QSize(20, 20))

        self.horizontalLayout_21.addWidget(self.widget_state)

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_21.addWidget(self.line_2)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_10.addWidget(self.label_14)

        self.label__MinTemp = QLabel(self.groupBox)
        self.label__MinTemp.setObjectName(u"label__MinTemp")

        self.horizontalLayout_10.addWidget(self.label__MinTemp)


        self.verticalLayout_10.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_15 = QLabel(self.groupBox)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_19.addWidget(self.label_15)

        self.label_MaxTemp = QLabel(self.groupBox)
        self.label_MaxTemp.setObjectName(u"label_MaxTemp")

        self.horizontalLayout_19.addWidget(self.label_MaxTemp)


        self.verticalLayout_10.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_20.addWidget(self.label_16)

        self.label_CenterTemp = QLabel(self.groupBox)
        self.label_CenterTemp.setObjectName(u"label_CenterTemp")

        self.horizontalLayout_20.addWidget(self.label_CenterTemp)


        self.verticalLayout_10.addLayout(self.horizontalLayout_20)


        self.horizontalLayout_21.addLayout(self.verticalLayout_10)


        self.verticalLayout_11.addWidget(self.groupBox)

        self.groupBox_6 = QGroupBox(self.tab_2)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMinimumSize(QSize(0, 250))
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.widget_chart1 = QWidget(self.groupBox_6)
        self.widget_chart1.setObjectName(u"widget_chart1")
        self.widget_chart1.setMinimumSize(QSize(20, 20))

        self.horizontalLayout_9.addWidget(self.widget_chart1)

        self.widget_chart2 = QWidget(self.groupBox_6)
        self.widget_chart2.setObjectName(u"widget_chart2")
        self.widget_chart2.setMinimumSize(QSize(20, 20))

        self.horizontalLayout_9.addWidget(self.widget_chart2)

        self.widget_chart3 = QWidget(self.groupBox_6)
        self.widget_chart3.setObjectName(u"widget_chart3")
        self.widget_chart3.setMinimumSize(QSize(20, 20))

        self.horizontalLayout_9.addWidget(self.widget_chart3)


        self.verticalLayout_9.addLayout(self.horizontalLayout_9)


        self.verticalLayout_11.addWidget(self.groupBox_6)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_12 = QVBoxLayout(self.tab_3)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.tableView = QTableView(self.tab_3)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_12.addWidget(self.tableView)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_4.addWidget(self.tabWidget)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"MQTT Demo", None))
        self.groupBox_Port.setTitle(QCoreApplication.translate("Form", u"MQTT\u8fde\u63a5\u914d\u7f6e", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u670d\u52a1\u5668\uff1a ", None))
        self.comboBox_Protocol.setItemText(0, QCoreApplication.translate("Form", u"mqtt://", None))
        self.comboBox_Protocol.setItemText(1, QCoreApplication.translate("Form", u"mqtts://", None))
        self.comboBox_Protocol.setItemText(2, QCoreApplication.translate("Form", u"ws://", None))
        self.comboBox_Protocol.setItemText(3, QCoreApplication.translate("Form", u"wss://", None))

        self.label_2.setText(QCoreApplication.translate("Form", u"\u7aef\u53e3\uff1a    ", None))
        self.label_ClientID.setText(QCoreApplication.translate("Form", u"Client ID:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u7528\u6237\u540d:    ", None))
        self.label_PassWord.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801:       ", None))
        self.pushButton_Open.setText(QCoreApplication.translate("Form", u"\u8fde\u63a5", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u8ba2\u9605\u5217\u8868", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0\u8ba2\u9605\uff1a", None))
        self.pushButton_AddSubscription.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"\u6d88\u606f\u53d1\u9001", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u4e3b\u9898\uff1a", None))
        self.pushButton_Send.setText(QCoreApplication.translate("Form", u"\u53d1\u9001", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"\u6d88\u606f\u63a5\u6536", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Connection/Debug", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Form", u"\u53c2\u6570\u914d\u7f6e", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u6a21\u5f0f\uff1a", None))
        self.comboBox_model.setItemText(0, QCoreApplication.translate("Form", u"Threshold", None))
        self.comboBox_model.setItemText(1, QCoreApplication.translate("Form", u"TinyML", None))
        self.comboBox_model.setItemText(2, QCoreApplication.translate("Form", u"Integral ", None))
        self.comboBox_model.setItemText(3, QCoreApplication.translate("Form", u"ML+Integral", None))

        self.label_9.setText(QCoreApplication.translate("Form", u"\u9608\u503c1\uff1a", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u9608\u503c2\uff1a", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u9608\u503c3\uff1a", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"\u9608\u503c4\uff1a", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"\u9608\u503c5\uff1a", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u68c0\u6d4b\u7ed3\u679c", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"Min_Temp:", None))
        self.label__MinTemp.setText(QCoreApplication.translate("Form", u"0000", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"Max_Temp:", None))
        self.label_MaxTemp.setText(QCoreApplication.translate("Form", u"0000", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"Center_Temp:", None))
        self.label_CenterTemp.setText(QCoreApplication.translate("Form", u"0000", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Form", u"\u5b9e\u65f6\u6570\u636e", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Info/Control", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"Record", None))
    # retranslateUi

