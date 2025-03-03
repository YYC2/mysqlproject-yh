# -*-coding:utf-8-*-
from urllib import parse
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from copy import copy
import sys
import pandas as pd
from sqlalchemy import create_engine
# from test import getData
from utils import getData, ExecuSQL,USER_NAME,USER_PASSWORD,ADDRESS

#参数
TABLE_NAME ='exp_input_param'
#叶栅几何
GEOMETRY = 'geometry'
#进口边界
INLET_BOUNDARY = 'inlet_boundary'
#出口40%位置叶中总压损失
OUTLET_LOSS_MIDSPAN = 'outlet_loss_midspan'
#叶中载荷分布
ZW_MIDSPAN = 'zw_midspan'
#出口40%位置截面总压损失
OUTLET_LOSS = 'outlet_loss'

#sql
sel = "select * from {}"
sel_max_id="select max(id) from {}"

# getData(max_id.format(table_name))
# def wirte_csv(data,table_name):
#     # engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format('cicsp', parse.quote_plus('cicsp@123.abc'), '10.51.57.46', '3306', 'cicsp'))
#     engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(USER_NAME, parse.quote_plus(USER_PASSWORD), ADDRESS, '3306', 'igouwu'))
#     data = pd.read_sql_query(sel.format(table_name), engine)
#     csv = pd.read_csv('./1.csv')
#     csv.columns = list(data.columns)[:-2]
#     # data.columns
#     csv['id'] = 0 + csv['id']
#     csv.to_sql(table_name,engine,chunksize=100000,index=None,if_exists='append')
#     print('存入成功！')


class Upload_Windows(QWidget):
    def __init__(self, df_file_path, parent=None):
        super(Upload_Windows, self).__init__(parent)
        hhbox = QHBoxLayout()  # 横向布局
        hhbox_1=QHBoxLayout()
        vbox=QVBoxLayout()
        self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(USER_NAME, parse.quote_plus(USER_PASSWORD), ADDRESS, '3306', 'igouwu'))

        # self.table_name = 'my_project'
        self.df_file_path = df_file_path
        self.df = pd.read_excel(self.df_file_path, sheet_name='导入参数')

        self.table_name = TABLE_NAME
        self.columns_name = self.df.columns
        self.columns_num = len(self.columns_name)
        self.records_num = self.df.shape[0]

        self.displayList = []
        self.saveList = []
        self.table = QTableWidget()


        self.saveItem=QPushButton("上传数据")
        #是否上传数据成功，0未成功，1成功
        self.flag = 0
        self.table_sitting()
        hhbox.addWidget(self.table)  # 把表格加入布局
        hhbox_1.addWidget(self.saveItem)

        vbox.addLayout(hhbox)
        vbox.addLayout(hhbox_1)
        self.setLayout(vbox)  # 创建布局
        self.setWindowTitle("数据库—表格")
        self.setWindowIcon(QIcon("icon.png"))

        self.connecter()

        self.resize(800, 600)
        self.show()



    def connecter(self):
        self.saveItem.clicked.connect(self._saveData)
        self.table.itemChanged.connect(self._dataChanged)

    def _saveData(self):
        try:
            self._saveParam()
            self._saveGeometry()
            self._saveInletboundary()
            self._saveOutletlossmidspan()
            self._saveZwmidspan()
            self._saveOutletloss()
            self.flag = 1
            self.close()
        except Exception:
            self.flag = 2
            self.close()

    def _saveParam(self):
        # self.data = pd.read_sql_query(sel.format(self.table_name), self.engine)
        # self.df = pd.read_excel(self.df_file_path,sheet_name='导入参数')
        self.df.columns = list(self.df.columns)
        self.df.drop(0, axis=0, inplace=True)
        ExecuSQL("truncate " + self.table_name)
        max_id  = getData(sel_max_id.format(self.table_name))[0][0] if getData(sel_max_id.format(self.table_name))[0][0] is not None else 0
        self.df['id'] = max_id + self.df['id']
        self.df.to_sql(self.table_name, self.engine, chunksize=100000,index=None,if_exists='append')
        print('存入成功！')

    def _saveGeometry(self):
        data = pd.read_excel(self.df_file_path, sheet_name='叶栅几何')
        data.drop(0, axis=0, inplace=True)
        ExecuSQL("truncate " + GEOMETRY)
        table_name = GEOMETRY
        data = data.reset_index()
        data.rename(columns={'index':'id'}, inplace=True)
        max_id  = getData(sel_max_id.format(table_name))[0][0] if getData(sel_max_id.format(table_name))[0][0] is not None else 0
        data['id'] = max_id + data['id']
        data.to_sql(table_name, self.engine, chunksize=100000,index=None,if_exists='append')



    def _saveInletboundary(self):
        data = pd.read_excel(self.df_file_path, sheet_name='进口边界')
        data.drop(0, axis=0, inplace=True)
        ExecuSQL("truncate " + INLET_BOUNDARY)
        table_name = INLET_BOUNDARY
        data = data.reset_index()
        data.rename(columns={'index':'id'}, inplace=True)
        max_id  = getData(sel_max_id.format(table_name))[0][0] if getData(sel_max_id.format(table_name))[0][0] is not None else 0
        data['id'] = max_id + data['id']
        data.to_sql(table_name, self.engine, chunksize=100000,index=None,if_exists='append')

    def _saveOutletlossmidspan(self):
        data = pd.read_excel(self.df_file_path, sheet_name='出口40%位置叶中总压损失')
        data.drop(0, axis=0, inplace=True)
        ExecuSQL("truncate " + OUTLET_LOSS_MIDSPAN)
        table_name = OUTLET_LOSS_MIDSPAN
        data = data.reset_index()
        data.rename(columns={'index':'id'}, inplace=True)
        max_id  = getData(sel_max_id.format(table_name))[0][0] if getData(sel_max_id.format(table_name))[0][0] is not None else 0
        data['id'] = max_id + data['id']
        data.to_sql(table_name, self.engine, chunksize=100000,index=None,if_exists='append')


    def _saveZwmidspan(self):
        data = pd.read_excel(self.df_file_path, sheet_name='叶中载荷分布')
        data.drop(0, axis=0, inplace=True)
        ExecuSQL("truncate " + ZW_MIDSPAN)
        table_name = ZW_MIDSPAN
        data = data.reset_index()
        data.rename(columns={'index':'id'}, inplace=True)
        max_id  = getData(sel_max_id.format(table_name))[0][0] if getData(sel_max_id.format(table_name))[0][0] is not None else 0
        data['id'] = max_id + data['id']
        data.to_sql(table_name, self.engine, chunksize=100000,index=None,if_exists='append')


    def _saveOutletloss(self):
        data = pd.read_excel(self.df_file_path, sheet_name='出口40%位置截面总压损失分布')
        data.drop(0, axis=0, inplace=True)
        ExecuSQL("truncate " + OUTLET_LOSS)
        table_name = OUTLET_LOSS
        data = data.reset_index()
        data.rename(columns={'index':'id'}, inplace=True)
        max_id  = getData(sel_max_id.format(table_name))[0][0] if getData(sel_max_id.format(table_name))[0][0] is not None else 1
        data['id'] = max_id + data['id']
        data.to_sql(table_name, self.engine, chunksize=100000,index=None,if_exists='append')

    def _dataChanged(self):
        """
        一旦检测到数据改变,则进行检查,
        选择添加新数据还是对原数据进行修改
        :return:
        """
        row_select = self.table.selectedItems()
        if len(row_select) == 0:
            return
        row= row_select[0].row()
        content = [self.table.item(row, i ).text() for i in range(self.columns_num)]
        content = tuple(content)
        # content = (self.table.item(row, 0).text(), self.table.item(row, 1).text(),
        #            self.table.item(row, 2).text())

        if row<=len(self.displayList):
            print("修改行",content)
            self.displayList[row-1]=content
        else:
            print("最新行",content)
            self.displayList.append(content)

    def _addItem(self):
        """
        添加空白行按钮的触发事件
        添加后刷新视图
        """
        num = self.table.rowCount()
        self.newLine(num)
        self.update()

    def init(self):
        """
        初始化操作
        即从数据库加载数据
        """

        print("初始化")
        for index,row in self.df.iterrows():
            item = tuple(self.df.iloc[index,:].to_frame().values.flatten('F'))
            self.newLine(index+1,item=item)
            self.displayList.append(item)
        self.saveList=copy(self.displayList)
        self.table.setRowCount(0)
        self.table.clearContents()
        self.table_sitting(flag=0)
        for index,item in enumerate(self.saveList):
            self.newLine(index+1,item)
        self.update()

    def _redraw(self):
        """
        repaint即刷新数据,
        用保存的数据覆盖未保存的数据
        """
        self.table.setRowCount(0)
        self.table.clearContents()
        self.table_sitting(flag=0)
        for index,item in enumerate(self.saveList):
            self.newLine(index+1,item)
        self.update()

    def _deleteItem(self):
        """
        若有选中行,点击删除后即可删除
        :return:
        """
        # ExecuSQL()
        row_select = self.table.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].row()
        if int(id)<=len(self.displayList):
            print("删除一条数据")
            self.displayList.pop(id-1)
            self.header.pop()
            self.table.removeRow(row_select[0].row())
        else:
            print("删除失败")
        self.update()


    def newLine(self,num,item=None):
        """
        :param num: 在对应序号处的序号画空白行
        :param item: 输入为对应数据
        """
        # num=self.table.rowCount()

        self.table.insertRow(num)
        _0= QTableWidgetItem("")
        _0.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        # _1 = QTableWidgetItem("")
        # _2 = QTableWidgetItem("")
        _n = [QTableWidgetItem("") for i in range(self.columns_num - 1)]
        # item=studentInfo()
        if item !=None:
            _0.setText(str(item[0]))
            for i, n in enumerate(_n):
                n.setText(str(item[i + 1]))
            # _1.setText(str(item[1]))
            # _2.setText(str(item[2]))
        else:
            _id = num
            if item == None:
                _idList=[int(k[0]) for k in self.displayList]
                if _id in _idList:
                    _id = max(_idList) + 1
            _0.setText(str(_id))

        self.table.setItem(num, 0, _0)
        for i, n in enumerate(_n):
            self.table.setItem(num, i + 1, n)
        # self.table.setItem(num, 1, _1)
        # self.table.setItem(num, 2, _2)
        self.header.append(str(num))
        self.table.setVerticalHeaderLabels(self.header)
        self.update()

    def table_sitting(self,flag=1):
        """
        :param flag: 初始化表头和行列数
        """
        self.header = [""]
        self.table.setColumnCount(self.columns_num)
        self.table.setRowCount(1)  # 设置表格有两行五列
        # for i, c in enumerate(self.df.iloc[0,:].values.tolist()):
        for i, c in enumerate(self.columns_name):
            self.table.setItem(0, i, QTableWidgetItem(c))
        # self.table.setItem(0, 0, QTableWidgetItem("学号"))
        # self.table.setItem(0, 1, QTableWidgetItem("名字"))
        # self.table.setItem(0, 2, QTableWidgetItem("出生日期"))
        if flag:
            self.init()

    def closeEvent(self, event):  # 关闭窗口触发以下事件
        if self.flag == 1:
            a = QMessageBox.question(self, '退出', '数据上传成功，是否退出?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)  # "退出"代表的是弹出框的标题,"你确认退出.."表示弹出框的内容
        elif self.flag == 2:
            a = QMessageBox.question(self, '退出', '数据有误，请修改数据后重新上传', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)  # "退出"代表的是弹出框的标题,"你确认退出.."表示弹出框的内容
        else:
            a = QMessageBox.question(self, '退出', '数据上传失败或未上传，是否确定退出?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)  # "退出"代表的是弹出框的标题,"你确认退出.."表示弹出框的内容
        if a == QMessageBox.Yes:
            event.accept()  # 接受关闭事件
        else:
            event.ignore()


if __name__ == "__main__":
    # wirte_csv(1, TABLE_NAME)
    app = QApplication(sys.argv)
    dlg = Upload_Windows('./1Ashort_basket2.csv')
    sys.exit(app.exec_())