# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import os, re, pyperclip, datetime
from IndexFiles import MySqlite
from Icon import *
from PyQt5 import QtCore, QtGui, QtWidgets


# iyzyi, 去除单元格虚框
class NoFocusItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        if option.state & QtWidgets.QStyle.State_HasFocus:
            # 取消虚线框
            option.state = option.state ^ QtWidgets.QStyle.State_HasFocus
        super(NoFocusItemDelegate, self).paint(painter, option, index)


# iyzyi，重写tablewidget
class MyQTableWidget(QtWidgets.QTableWidget):
    row_select_status = []
    isDouble = False
    myMouseClickSignal = QtCore.pyqtSignal(QtCore.QModelIndex)
    myMouseDoubleClickSignal = QtCore.pyqtSignal(QtCore.QModelIndex)

    def __init__(self, parent=None):
        super(MyQTableWidget, self).__init__(parent)

    def get_click_row(self, event):
        gp = event.globalPos()
        tp = self.viewport().mapFromGlobal(gp)
        item = self.indexAt(tp)
        return item if item.isValid() else None

    def mouseDoubleClickEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            self.isDouble = True
            item = self.get_click_row(e)
            if item:
                self.myMouseDoubleClickSignal.emit(item)

    def mousePressEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            item = self.get_click_row(e)
            QtCore.QTimer.singleShot(200, lambda:self.__judge_click(item))

    # 防止双击事件必然触发单击事件
    def __judge_click(self, item):
        #单击
        if self.isDouble == False:
            if item:
                self.myMouseClickSignal.emit(item)
        #双击
        else:
            self.isDouble = False

    def change_row_color(self, row):
        for col in range(self.columnCount()):
            self.item(row, col).setBackground(QtGui.QColor(135, 206, 255))

    def reset_row_color(self, row):
        for col in range(self.columnCount()):
            self.item(row, col).setBackground(QtGui.QColor(255, 255, 255))

    def get_selectd_rows(self):
        selected_rows = []
        for row, status in enumerate(self.row_select_status):
            if status:
                selected_rows.append(row)
        return selected_rows


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(960, 660)
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap("./logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon = iconFromBase64(icon_base64)
        Dialog.setWindowIcon(icon)
        self.lineEdit_Filter = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Filter.setGeometry(QtCore.QRect(70, 20, 341, 20))
        self.lineEdit_Filter.setObjectName("lineEdit_Filter")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 24, 54, 12))
        self.label.setObjectName("label")
        self.pushButton_SearchFiles = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchFiles.setGeometry(QtCore.QRect(520, 20, 75, 23))
        self.pushButton_SearchFiles.setObjectName("pushButton_SearchFiles")
        self.tableWidget_SearchResult = MyQTableWidget(Dialog)                                              #iyzyi，防止双击事件必然触发单击事件
        self.tableWidget_SearchResult.setGeometry(QtCore.QRect(6, 80, 948, 371))
        self.tableWidget_SearchResult.setMinimumSize(QtCore.QSize(871, 321))
        self.tableWidget_SearchResult.setColumnCount(2)
        self.tableWidget_SearchResult.setObjectName("tableWidget_SearchResult")
        self.tableWidget_SearchResult.setItemDelegate(NoFocusItemDelegate(self.tableWidget_SearchResult))   # iyzyi, 去除单元格虚框
        self.tableWidget_SearchResult.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_SearchResult.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_SearchResult.setHorizontalHeaderItem(1, item)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 458, 61, 20))
        self.label_3.setObjectName("label_3")
        self.tableWidget_RootPath = MyQTableWidget(Dialog)                                                  # iyzyi，防止双击事件必然触发单击事件
        self.tableWidget_RootPath.setGeometry(QtCore.QRect(6, 483, 948, 171))
        self.tableWidget_RootPath.setObjectName("tableWidget_RootPath")
        self.tableWidget_RootPath.setItemDelegate(NoFocusItemDelegate(self.tableWidget_RootPath))           # iyzyi, 去除单元格虚框
        self.tableWidget_RootPath.setColumnCount(5)
        self.tableWidget_RootPath.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_RootPath.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_RootPath.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_RootPath.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_RootPath.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_RootPath.setHorizontalHeaderItem(4, item)
        self.pushButton_BulidFilesIndex = QtWidgets.QPushButton(Dialog)
        self.pushButton_BulidFilesIndex.setGeometry(QtCore.QRect(561, 456, 91, 23))
        self.pushButton_BulidFilesIndex.setObjectName("pushButton_BulidFilesIndex")
        self.label_SearchResultNum = QtWidgets.QLabel(Dialog)
        self.label_SearchResultNum.setGeometry(QtCore.QRect(70, 60, 451, 12))
        self.label_SearchResultNum.setObjectName("label_SearchResultNum")
        self.radioButton_Common = QtWidgets.QRadioButton(Dialog)
        self.radioButton_Common.setGeometry(QtCore.QRect(435, 14, 89, 16))
        self.radioButton_Common.setAutoRepeat(False)
        self.radioButton_Common.setObjectName("radioButton_Common")
        self.radioButton_RegExp = QtWidgets.QRadioButton(Dialog)
        self.radioButton_RegExp.setGeometry(QtCore.QRect(435, 31, 89, 16))
        self.radioButton_RegExp.setObjectName("radioButton_RegExp")
        self.pushButton_SetDefaultSearchPath = QtWidgets.QPushButton(Dialog)
        self.pushButton_SetDefaultSearchPath.setGeometry(QtCore.QRect(662, 456, 91, 23))
        self.pushButton_SetDefaultSearchPath.setObjectName("pushButton_SetDefaultSearchPath")
        self.pushButton_CleanInvalidPath = QtWidgets.QPushButton(Dialog)
        self.pushButton_CleanInvalidPath.setGeometry(QtCore.QRect(864, 456, 91, 23))
        self.pushButton_CleanInvalidPath.setObjectName("pushButton_CleanInvalidPath")
        self.pushButton_DeleteChoosedPath = QtWidgets.QPushButton(Dialog)
        self.pushButton_DeleteChoosedPath.setGeometry(QtCore.QRect(763, 456, 91, 23))
        self.pushButton_DeleteChoosedPath.setObjectName("pushButton_DeleteChoosedPath")
        self.label_BuildingFilesIndex = QtWidgets.QLabel(Dialog)
        self.label_BuildingFilesIndex.setGeometry(QtCore.QRect(85, 458, 421, 20))
        self.label_BuildingFilesIndex.setObjectName("label_BuildingFilesIndex")
        self.lineEdit_Filter.raise_()
        self.label.raise_()
        self.pushButton_SearchFiles.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.tableWidget_RootPath.raise_()
        self.pushButton_BulidFilesIndex.raise_()
        self.tableWidget_SearchResult.raise_()
        self.label_SearchResultNum.raise_()
        self.radioButton_Common.raise_()
        self.radioButton_RegExp.raise_()
        self.pushButton_SetDefaultSearchPath.raise_()
        self.pushButton_CleanInvalidPath.raise_()
        self.pushButton_DeleteChoosedPath.raise_()
        self.label_BuildingFilesIndex.raise_()

        self.db = MySqlite()
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "文件检索 子安专用"))
        self.label.setText(_translate("Dialog", "检索条件"))
        self.pushButton_SearchFiles.setText(_translate("Dialog", "开始检索"))
        item = self.tableWidget_SearchResult.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "类型"))
        item = self.tableWidget_SearchResult.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "路径"))
        self.label_2.setText(_translate("Dialog", "检索结果"))
        self.label_3.setText(_translate("Dialog", "已索引目录"))
        item = self.tableWidget_RootPath.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "目录"))
        item = self.tableWidget_RootPath.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "文件夹数"))
        item = self.tableWidget_RootPath.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "文件数"))
        item = self.tableWidget_RootPath.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "更新日期"))
        item = self.tableWidget_RootPath.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "状态"))
        self.pushButton_BulidFilesIndex.setText(_translate("Dialog", "建立目录索引"))
        self.label_SearchResultNum.setText(_translate("Dialog", "共检索到满足条件的x个文件夹、x个文件"))
        self.radioButton_Common.setText(_translate("Dialog", "普通匹配"))
        self.radioButton_RegExp.setText(_translate("Dialog", "正则匹配"))
        self.pushButton_SetDefaultSearchPath.setToolTip(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.pushButton_SetDefaultSearchPath.setText(_translate("Dialog", "设为默认目录"))
        self.pushButton_CleanInvalidPath.setText(_translate("Dialog", "清理无效目录"))
        self.pushButton_DeleteChoosedPath.setText(_translate("Dialog", "删除选中目录"))
        self.label_BuildingFilesIndex.setText(_translate("Dialog", "正在建立目录索引......"))

        self.iyzyiChangeUI()
        self.iyzyiInitData()

    
    # 控件自适应
    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        frame_w, frame_h = event.size().width(), event.size().height()

        x1 = self.tableWidget_SearchResult.x()
        y1 = self.tableWidget_SearchResult.y()
        w1 = frame_w - x1 * 2
        h1 = int(371 / 542 * (frame_h - 118))
        self.tableWidget_SearchResult.setGeometry(x1, y1, w1, h1)

        x2 = self.tableWidget_RootPath.x()
        y2 = y1 + h1 + 32
        w2 = frame_w - x2 * 2
        h2 = int(171 / 542 * (frame_h - 118))
        self.tableWidget_RootPath.setGeometry(x2, y2, w2, h2)

        self.label_3.setGeometry(self.label_3.x(), y1 + h1 + 7, self.label_3.width(), self.label_3.height())
        self.label_BuildingFilesIndex.setGeometry(self.label_BuildingFilesIndex.x(), y1 + h1 + 7, self.label_BuildingFilesIndex.width(), self.label_BuildingFilesIndex.height())
        self.pushButton_BulidFilesIndex.setGeometry(frame_w - 399, y1 + h1 + 5, self.pushButton_BulidFilesIndex.width(), self.pushButton_BulidFilesIndex.height())
        self.pushButton_SetDefaultSearchPath.setGeometry(frame_w - 298, y1 + h1 + 5, self.pushButton_SetDefaultSearchPath.width(), self.pushButton_SetDefaultSearchPath.height())
        self.pushButton_DeleteChoosedPath.setGeometry(frame_w - 197, y1 + h1 + 5, self.pushButton_DeleteChoosedPath.width(), self.pushButton_DeleteChoosedPath.height())
        self.pushButton_CleanInvalidPath.setGeometry(frame_w - 96, y1 + h1 + 5, self.pushButton_CleanInvalidPath.width(), self.pushButton_CleanInvalidPath.height())

        # 调整列宽
        self.tableWidget_SearchResult.setColumnWidth(1, frame_w-40-19-x1*2)
        self.tableWidget_RootPath.setColumnWidth(0, frame_w-100-100-160-40-19-x2*2)


    def iyzyiChangeUI(self):
        # 检索结果 表格
        # 表格选中一整行
        self.tableWidget_SearchResult.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        # 列宽
        #self.tableWidget_SearchResult.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        #self.tableWidget_SearchResult.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget_SearchResult.setColumnWidth(0, 40)
        self.tableWidget_SearchResult.setColumnWidth(1, 948-40-19)
        # 行宽
        self.tableWidget_SearchResult.verticalHeader().setDefaultSectionSize(24)
        self.tableWidget_SearchResult.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        # 不可编辑
        self.tableWidget_SearchResult.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 绑定双击
        #self.tableWidget_SearchResult.doubleClicked.connect(self.doubleClicked_SearchResultRow)
        self.tableWidget_SearchResult.myMouseDoubleClickSignal.connect(self.doubleClicked_SearchResultRow)
        # 绑定单击
        #self.tableWidget_SearchResult.clicked.connect(self.clicked_SearchResultRow)
        self.tableWidget_SearchResult.myMouseClickSignal.connect(self.clicked_SearchResultRow)
        # 右键菜单
        self.tableWidget_SearchResult.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget_SearchResult.customContextMenuRequested.connect(self.tableWidget_SearchResult_RbuttonMenu)
        # 取消行号表头
        self.tableWidget_SearchResult.verticalHeader().hide()
        # 一直显示竖直滚动条
        self.tableWidget_SearchResult.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)  


        # 已检索目录 表格
        # 表格选中一整行
        self.tableWidget_RootPath.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        # 列宽
        self.tableWidget_RootPath.setColumnWidth(0, 948-100-100-160-40-19)
        self.tableWidget_RootPath.setColumnWidth(1, 100)
        self.tableWidget_RootPath.setColumnWidth(2, 100)
        self.tableWidget_RootPath.setColumnWidth(3, 160)
        self.tableWidget_RootPath.setColumnWidth(4, 40)
        # 行宽
        self.tableWidget_RootPath.verticalHeader().setDefaultSectionSize(24)
        self.tableWidget_RootPath.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        # 不可编辑
        self.tableWidget_RootPath.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 绑定双击
        #self.tableWidget_RootPath.doubleClicked.connect(self.doubleClicked_RootPathRow)
        self.tableWidget_RootPath.myMouseDoubleClickSignal.connect(self.doubleClicked_RootPathRow)
        # 绑定单击
        #self.tableWidget_RootPath.clicked.connect(self.clicked_RootPathRow)
        self.tableWidget_RootPath.myMouseClickSignal.connect(self.clicked_RootPathRow)
        # 取消行号表头
        self.tableWidget_RootPath.verticalHeader().hide()
        # 一直显示竖直滚动条
        self.tableWidget_RootPath.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)  


        # 绑定按钮
        self.pushButton_SearchFiles.clicked.connect(self.onclick_pushButton_SearchFiles)
        self.pushButton_BulidFilesIndex.clicked.connect(self.onclick_pushButton_BulidFilesIndex)
        self.pushButton_SetDefaultSearchPath.clicked.connect(self.onclick_pushButton_SetDefaultSearchPath)
        self.pushButton_DeleteChoosedPath.clicked.connect(self.onclick_pushButton_DeleteChoosedPath)
        self.pushButton_CleanInvalidPath.clicked.connect(self.onclick_pushButton_CleanInvalidPath)

        
        # 初始化 检索条件
        filter_mode = self.db.GetLastFilterMode()
        if filter_mode == 'regexp':
            self.radioButton_RegExp.setChecked(True)
        else:
            self.radioButton_Common.setChecked(True)

        
        # 标签
        self.label_SearchResultNum.setText('')
        self.label_BuildingFilesIndex.setText('')


    def iyzyiInitData(self):
        self.display_root_paths()


    # 刷新显示 已检索目录 表格
    def display_root_paths(self):

        # 清空原有数据
        row_count = self.tableWidget_RootPath.rowCount()
        for i in range(row_count):        
            self.tableWidget_RootPath.removeRow(0)

        # 获取默认检索路径
        default_vol_ids = self.db.GetDefaultSearchPath()

        self.root_paths_vol_id_dict = {}
        self.root_paths_checkbox_dict = {}
        res = self.db.DisplayPaths()
        
        for item in res:
            vol_id, vol_name, vol_path, dirs_num, files_num, update_time, writing = item
            row_count = self.tableWidget_RootPath.rowCount()
            self.root_paths_vol_id_dict[str(row_count)] = vol_id

            # 尾部插入一行
            self.tableWidget_RootPath.insertRow(row_count)
            
            # 设置复选框
            checkbox = QtWidgets.QCheckBox()
            self.root_paths_checkbox_dict[str(row_count)] = checkbox
            self.tableWidget_RootPath.setCellWidget(row_count, 0, checkbox)
            if default_vol_ids:
                if str(vol_id) in default_vol_ids:
                    checkbox.setChecked(True)

            def Item(value, center=True):
                item = QtWidgets.QTableWidgetItem(value)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsSelectable)
                if center:
                    item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                return item

            # 填充相关数据
            self.tableWidget_RootPath.setItem(row_count, 0, Item('   ' + vol_path, False))
            self.tableWidget_RootPath.setItem(row_count, 1, Item(str(dirs_num)))
            self.tableWidget_RootPath.setItem(row_count, 2, Item(str(files_num)))
            self.tableWidget_RootPath.setItem(row_count, 3, Item(str(datetime.datetime.fromtimestamp(update_time))))
            self.tableWidget_RootPath.setItem(row_count, 4, Item(writing))


    # 双击 检索结果 表格的一行时，打开相应文件(夹)
    def doubleClicked_SearchResultRow(self, Item):
        row = Item.row()
        type = self.tableWidget_SearchResult.item(row, 0).text()
        path = self.tableWidget_SearchResult.item(row, 1).text()
        if os.path.exists(path):
            try:
                os.startfile(path)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, '打开{}失败'.format(type), '{}'.format(e), QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.critical(self, '打开{}失败'.format(type), '{} {} 不存在，可能是离线{}'.format(type, path, type), QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)


    # 单击 检索结果 表格的一行时，勾选或取消勾选
    def clicked_SearchResultRow(self, Item):
        row = Item.row()
        if not self.tableWidget_SearchResult.row_select_status[row]:
            self.tableWidget_SearchResult.change_row_color(row)
            self.tableWidget_SearchResult.row_select_status[row] = True
        else:
            self.tableWidget_SearchResult.reset_row_color(row)
            self.tableWidget_SearchResult.row_select_status[row] = False


    # 双击 已索引目录 表格的一行时，显示对应文件夹内的文件（夹）
    def doubleClicked_RootPathRow(self, Item):
        row = Item.row()  # 获取行数
        root_path = self.tableWidget_RootPath.item(row, 0).text().lstrip(' ')
        # if os.path.exists(root_path):
        #     os.startfile(root_path)
        # else:
        #     QtWidgets.QMessageBox.critical(self, '打开索引目录失败', '目录 {} 不存在，可能是离线目录'.format(root_path), QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        
        self.show_files_under_dir_by_path(root_path)


    # 单击 已索引目录 表格的一行时，勾选或取消勾选
    def clicked_RootPathRow(self, Item):
        row = Item.row()
        checkbox = self.root_paths_checkbox_dict[str(row)]
        checkbox.setChecked(not checkbox.isChecked())


    # 开始检索文件
    def onclick_pushButton_SearchFiles(self):
        self.label_SearchResultNum.setText('正在检索中......')
        self.label_SearchResultNum.repaint()

        # 清空原有数据
        self.tableWidget_SearchResult.row_select_status = []
        row_count = self.tableWidget_SearchResult.rowCount()
        for i in range(row_count):        
            self.tableWidget_SearchResult.removeRow(0)
        self.tableWidget_SearchResult.repaint()

        # 检索路径
        root_paths = []
        row_count = self.tableWidget_RootPath.rowCount()
        for i in range(row_count):
            if self.root_paths_checkbox_dict[str(i)].isChecked():
                root_path = self.tableWidget_RootPath.item(i, 0).text().lstrip(' ')
                root_paths.append(root_path)

        # 检索条件
        filter = self.lineEdit_Filter.text()
        
        # 检索模式
        if self.radioButton_RegExp.isChecked():
            filter_mode = 'regexp'
        else:
            filter_mode = 'common'

        result, dirs_num, files_num = self.db.MultiVolSearchFiles(root_paths, filter, filter_mode)

        for item in result:
            file_path, type = item

            # 尾部插入一行
            row_count = self.tableWidget_SearchResult.rowCount()
            self.tableWidget_SearchResult.insertRow(row_count)

            def Item(value, center=True):
                item = QtWidgets.QTableWidgetItem(value)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsSelectable)
                if center:
                    item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                return item

            # 填充相关数据
            self.tableWidget_SearchResult.setItem(row_count, 0, Item('文件' if type=='F' else '目录'))
            self.tableWidget_SearchResult.setItem(row_count, 1, Item(file_path, False))

            self.tableWidget_SearchResult.row_select_status.append(False)

        self.label_SearchResultNum.setText('共检索到满足条件的{}个文件夹、{}个文件'.format(dirs_num, files_num))

        self.db.RecordLastFilterMode(filter_mode)


    # 建立文件索引
    def onclick_pushButton_BulidFilesIndex(self):
        root_path = QtWidgets.QFileDialog.getExistingDirectoryUrl(None, "选择要建立索引的文件夹", QtCore.QUrl("clsid:0AC0837C-BBF8-452A-850D-79D08E667CA7")).toString()
        if not root_path:
            return
        if root_path[:8] == 'file:///':
            root_path = root_path[8:]
        self.label_BuildingFilesIndex.setText('正在建立目录索引......')
        self.label_BuildingFilesIndex.repaint()
        dirs_num, files_num = self.db.BuildFilesIndex(root_path)
        self.display_root_paths()
        self.label_BuildingFilesIndex.setText('')
        QtWidgets.QMessageBox.information(self, '建立文件索引成功', '目录 {} 中共有{}个文件夹，{}个文件'.format(root_path, dirs_num, files_num))


    # 设为默认目录
    def onclick_pushButton_SetDefaultSearchPath(self):
        row_count = self.tableWidget_RootPath.rowCount()
        vol_ids = []
        for i in range(row_count):
            if self.root_paths_checkbox_dict[str(i)].isChecked():
                vol_ids.append(self.root_paths_vol_id_dict[str(i)])
        self.db.SetDefaultSearchPath(vol_ids)


    # 清理无效目录
    def onclick_pushButton_CleanInvalidPath(self):
        self.db.CleanInvalidData()
        self.display_root_paths()

    
    # 删除选中目录
    def onclick_pushButton_DeleteChoosedPath(self):
        root_paths = []
        row_count = self.tableWidget_RootPath.rowCount()
        for i in range(row_count):
            if self.root_paths_checkbox_dict[str(i)].isChecked():
                root_path = self.tableWidget_RootPath.item(i, 0).text().lstrip(' ')
                root_paths.append(root_path)

        if len(root_paths) > 0:
            choice = QtWidgets.QMessageBox.question(self, '是否删除以下索引数据', '\n'.join(root_paths), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if choice == QtWidgets.QMessageBox.Yes:
                for root_path in root_paths:
                    self.db.DeleteFilesIndex(root_path)
                self.display_root_paths()


    # 显示目录下的所有文件（夹）
    def show_files_under_dir_by_path(self, target_path):
        # 清空原有数据
        self.tableWidget_SearchResult.row_select_status = []
        row_count = self.tableWidget_SearchResult.rowCount()
        for i in range(row_count):        
            self.tableWidget_SearchResult.removeRow(0)
        self.tableWidget_SearchResult.repaint()

        # 获取数据
        target_path, result, dirs_num, files_num = self.db.ShowFilesUnderDirByPath(target_path)

        for item in result:
            file_path, type = item

            # 尾部插入一行
            row_count = self.tableWidget_SearchResult.rowCount()
            self.tableWidget_SearchResult.insertRow(row_count)

            def Item(value, center=True):
                item = QtWidgets.QTableWidgetItem(value)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsSelectable)
                if center:
                    item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                return item

            # 填充相关数据
            self.tableWidget_SearchResult.setItem(row_count, 0, Item('文件' if type=='F' else '目录'))
            self.tableWidget_SearchResult.setItem(row_count, 1, Item(file_path, False))

            self.tableWidget_SearchResult.row_select_status.append(False)

        self.label_SearchResultNum.setText('{} 目录下共{}个文件夹，{}个文件'.format(target_path, dirs_num, files_num))


    # 查找结果 右键菜单
    def tableWidget_SearchResult_RbuttonMenu(self, pos):
        # 添加右键菜单
        menu = QtWidgets.QMenu() #实例化菜单
        menu_action = ['显示选中项子文件(夹)', '打开选中项所在文件夹', '打开选中项', '全部勾选', '全部取消勾选', '复制选中项路径', '复制全部检索结果']
        action_show_files_under_dir = menu.addAction(menu_action[0])
        action_open_folder = menu.addAction(menu_action[1])
        action_open_file_or_dir = menu.addAction(menu_action[2])
        action_select_all = menu.addAction(menu_action[3])
        action_deselect_all = menu.addAction(menu_action[4])
        action_copy_path = menu.addAction(menu_action[5])
        action_copy_search_result = menu.addAction(menu_action[6])
        action = menu.exec_(self.mapToGlobal(self.mapFromGlobal(QtGui.QCursor.pos())))


        # 获取选中项
        def get_choiced_paths():
            paths = []
            select_rows = self.tableWidget_SearchResult.get_selectd_rows()
            for row in select_rows:
                path = self.tableWidget_SearchResult.item(row, 1).text()
                paths.append(path)
            return paths
        

        # 获取选中项
        def get_choiced_paths_and_type():
            paths = []
            select_rows = self.tableWidget_SearchResult.get_selectd_rows()
            for row in select_rows:
                path = self.tableWidget_SearchResult.item(row, 1).text()
                type = self.tableWidget_SearchResult.item(row, 0).text()
                paths.append((path, type))
            return paths
        

        # 显示选中项的子文件（夹）
        def action_show_files_under_dir_func():
            paths_and_type = get_choiced_paths_and_type()
            if len(paths_and_type) == 0:
                QtWidgets.QMessageBox.information(self, menu_action[0], '没有选中项', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            elif len(paths_and_type) > 1:
                QtWidgets.QMessageBox.information(self, menu_action[0], '只能选中一项，当前选择的项过多', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            else:
                if paths_and_type[0][1] == '文件':
                    QtWidgets.QMessageBox.information(self, menu_action[0], '选中项必须是目录', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                else:
                    self.show_files_under_dir_by_path(paths_and_type[0][0])


        # 打开所在文件夹
        def action_open_folder_func():
            paths = get_choiced_paths()
            if len(paths) == 0:
                QtWidgets.QMessageBox.information(self, menu_action[1], '没有选中项', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            
            exists_folders = []
            not_exists_folders = []
            for path in paths:
                if len(path) > 3:
                    folder = os.path.dirname(path)
                else:
                    folder = path

                if os.path.exists(folder):
                    exists_folders.append(folder)
                else:
                    not_exists_folders.append(folder)
                
            exists_folders = list(set(list(exists_folders)))
            not_exists_folders = list(set(list(not_exists_folders)))
            
            message = '以下文件夹存在：\n{}\n\n以下文件夹不存在：\n{}\n\n是否继续打开存在的文件夹'.format('\n'.join(exists_folders) if exists_folders else '无', '\n'.join(not_exists_folders) if not_exists_folders else '无')
            choice = QtWidgets.QMessageBox.question(self, menu_action[1], message, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if choice == QtWidgets.QMessageBox.Yes:
                for path in exists_folders:
                    os.startfile(path)

        # 打开文件(夹)
        def action_open_file_or_dir_func():
            paths = get_choiced_paths()
            if len(paths) == 0:
                QtWidgets.QMessageBox.information(self, menu_action[2], '没有选中项', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return

            exists_paths = []
            not_exists_paths = []
            for path in paths:
                if os.path.exists(path):
                    exists_paths.append(path)
                else:
                    not_exists_paths.append(path)

            message = '以下文件(夹)存在：\n{}\n\n以下文件(夹)不存在：\n{}\n\n是否继续打开存在的文件(夹)'.format('\n'.join(exists_paths) if exists_paths else '无', '\n'.join(not_exists_paths) if not_exists_paths else '无')
            choice = QtWidgets.QMessageBox.question(self, menu_action[2], message, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if choice == QtWidgets.QMessageBox.Yes:
                for path in exists_paths:
                    try:
                        os.startfile(path)
                    except Exception as e:
                        QtWidgets.QMessageBox.critical(self, '打开文件(夹)失败', '{}'.format(e), QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

        # 全部勾选
        def action_action_select_all_func():
            row_count = self.tableWidget_SearchResult.rowCount()
            for row in range(row_count):
                self.tableWidget_SearchResult.change_row_color(row)
                self.tableWidget_SearchResult.row_select_status[row] = True

        # 全部取消勾选
        def action_action_deselect_all_func():
            selected_rows = self.tableWidget_SearchResult.get_selectd_rows()
            for row in selected_rows:
                self.tableWidget_SearchResult.reset_row_color(row)
                self.tableWidget_SearchResult.row_select_status[row] = False

        # 复制选中项路径
        def action_copy_path_func():
            paths = get_choiced_paths()
            data = '\n'.join(paths)
            pyperclip.copy(data)

        # 复制全部检索结果
        def action_copy_search_result_func():
            paths = []
            row_count = self.tableWidget_SearchResult.rowCount()
            for i in range(row_count):
                path = self.tableWidget_SearchResult.item(i, 1).text()
                paths.append(path)
            data = '\n'.join(paths)
            pyperclip.copy(data)

        # 操作
        if action == action_show_files_under_dir:
            action_show_files_under_dir_func()
        if action == action_open_folder:
            action_open_folder_func()            
        elif action == action_open_file_or_dir:
        	action_open_file_or_dir_func()
        elif action == action_select_all:
            action_action_select_all_func()
        elif action == action_deselect_all:
            action_action_deselect_all_func()
        elif action == action_copy_path:
            action_copy_path_func()
        elif action == action_copy_search_result:
            action_copy_search_result_func()