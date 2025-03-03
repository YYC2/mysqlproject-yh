# -*- coding: UTF-8 -*-
from urllib import parse
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from copy import copy
import sys
import pymysql
from sqlalchemy import create_engine

import paint
import windows  # 这个是可以单独运行的窗口
from utils import create_table,USER_PASSWORD,USER_NAME,ADDRESS

TABLE_NAME = 'exp_input_param'


def sql_condition(cols, values, type):
    if type == 'select':
        conj = 'and'
    else :
        conj = ','
    param = "'"
    sql_cond = ""
    if len(values[0]) == 1 :
        for index, c in enumerate(cols):
            # if (isinstance(values[index][0], int) or isinstance(values[index][0], float)) and type == 'select':
            #     param = ""
            sql_cond = sql_cond + c + '=' + param + str(values[index][0]) + param
            if index != len(cols) - 1 :
                sql_cond = sql_cond +' '+ conj + ' '
    else:
        for index, c in enumerate(cols):
            sql_cond = sql_cond + c + 'in' + '('
            for i, v in enumerate(values[index]):
                # if (isinstance(v, int) or isinstance(v, float)) and type == 'select':
                #     param = ""
                sql_cond = sql_cond + param + str(v) + param
                if i != len(values[index]) - 1 :
                    sql_cond = sql_cond +' '+ ',' + ' '
                else:
                    sql_cond = sql_cond + ')'
            if index != len(cols) - 1 :
                sql_cond = sql_cond +' '+ conj + ' '

    return sql_cond

# ins="insert into my_project (pressure, velity) values ('{}','{}');"
delete="delete from {} where id={}"
ins= "insert into {} {} values {};"
sel="select * from {}"
col = "select * from information_schema.COLUMNS where table_name='{}';"
recordnum = "select count(*) from {}"
upd = "update {} set {} where id={};"
conditionselect = "select * from {} where {}"
distinctselect = "select DISTINCT({}) from {}"

sel_geometry = "select p_ss_y, p_ps_z, p_ps_y,p_ss_z from geometry where cascades= '{}'"

sel_inlet_boundary = "select dspan_in, dv2_in from inlet_boundary where cascades= '{}' and re = {} and wake_f = '{}'"

sel_zw_midspan = "select dax_chord, mid_cp from zw_midspan where cascades= '{}' and re = {} and wake_f = '{}'"

sel_outlet_loss_midspan = "select dpitch_mid, mid_cp0 from outlet_loss_midspan where cascades= '{}' and re = {} and wake_f = '{}'"

sel_outlet_loss = "select dpitch_out, dspan_out, out_cp0 from outlet_loss where cascades= '{}' and re = {} and wake_f = '{}'"



def getCursor():
    """
    :return: 返回操作数据库的cursor
    """
    conn = pymysql.connect(host=ADDRESS  # 连接名称,默认127.0.0.1
                           , user=USER_NAME  # 用户名
                           , passwd=USER_PASSWORD  # 密码
                           , port=3306  # 端口,默认为3306
                           , db='igouwu'  # 数据库名称
                           , charset='utf8'  # 字符编码
                           )
    # conn = pymysql.connect(host='10.51.57.46'  # 连接名称,默认127.0.0.1
    #                        , user='cicsp'  # 用户名
    #                        , passwd='cicsp@123.abc'  # 密码
    #                        , port=3306  # 端口,默认为3306
    #                        , db='cicsp'  # 数据库名称
    #                        , charset='utf8'  # 字符编码
    #                        )
    return conn

def ExecuSQL(argv):
    """
    执行数据库的语句,但是没有返回值
    :param argv:
    """
    conn=getCursor()
    cur = conn.cursor()  # 生成游标对象
    cur.execute(argv)  # 执行SQL语句
    conn.commit()
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接

def getData(argv):
    """
    执行数据库的语句,有返回值
    :param argv:
    """
    conn = getCursor()
    cur = conn.cursor()  # 生成游标对象
    cur.execute(argv)  # 执行SQL语句
    data = cur.fetchall()  # 通过fetchall方法获得数据
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接
    return data

class Example(QWidget):
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)
        allbox = QHBoxLayout()
        #数据展示框
        hhbox_x = QHBoxLayout()
        hhbox = QHBoxLayout()  # 横向布局
        hhbox_1=QHBoxLayout()
        #画图数据框
        pbox=QHBoxLayout()
        pbox_1=QHBoxLayout()
        vbox=QVBoxLayout()
        vbox_1=QVBoxLayout()
        self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(USER_NAME, parse.quote_plus(USER_PASSWORD), ADDRESS, '3306', 'igouwu'))

        self.cascades = 'PackB'
        self.re = 25000
        self.wake_f =  '定常'

        self.paint_table_name = "geometry"
        self.paint_columns_name = [c[3] for c in getData(col.format(self.paint_table_name))]
        test = []
        for c in self.paint_columns_name:
            if c not in ['id', 'cascades', 're', 'wake_f', 'create_time','update_time']:
                test.append(c)
        self.paint_columns_name = test
        self.paint_columns_num = len(self.paint_columns_name)
        self.paint_records_num = getData(recordnum.format(self.paint_table_name))[0][0]
        self.table_1 = QTableWidget()
        self.table_sitting_paint(sel_geometry.format(self.cascades))

        self.geometry=QPushButton("叶栅几何")
        self.inlet_boundary=QPushButton("进口边界")
        self.zw_midspan=QPushButton("叶中载荷分布")
        self.outlet_loss=QPushButton("出口40%位置截面总压损失")
        self.outlet_loss_midspan = QPushButton("出口40%位置叶中总压损失")

        self.geometry.clicked.connect(self.show_geometry)
        self.inlet_boundary.clicked.connect(self.show_inlet_boundary)
        self.zw_midspan.clicked.connect(self.show_zw_midspan)
        self.outlet_loss.clicked.connect(self.show_outlet_loss)
        self.outlet_loss_midspan.clicked.connect(self.show_outlet_loss_midspan)


        # self.table_name = 'my_project'
        self.table_name = TABLE_NAME
        self.columns_name = [c[3] for c in getData(col.format(self.table_name))]
        self.columns_num = len(self.columns_name)
        self.records_num = getData(recordnum.format(self.table_name))[0][0]

        self.displayList = []
        self.saveList = []
        self.table = QTableWidget()

        self.addItem=QPushButton("添加数据")
        self.searchItem=QPushButton("刷新数据")
        self.deleteItem = QPushButton("删除数据")
        self.saveItem=QPushButton("保存数据")


        self.comboBox1 = QComboBox()
        self.comboBox2 = QComboBox()
        self.comboBox3 = QComboBox()
        self.comboBox4 = QComboBox()
        self.initcombox()
        self.pushButton = QPushButton("上传文件")
        self.filterButton = QPushButton("筛选")
        self.paintButton = QPushButton("绘图")
        self.pushButton.clicked.connect(self.click_find_file_path)
        self.filterButton.clicked.connect(self._filter)
        self.paintButton.clicked.connect(self._paint)

        self.flag = 1
        self.table_sitting()
        hhbox_x.addWidget(self.pushButton)
        hhbox_x.addWidget(self.comboBox1)
        hhbox_x.addWidget(self.comboBox2)
        hhbox_x.addWidget(self.comboBox3)
        hhbox_x.addWidget(self.comboBox4)
        hhbox_x.addWidget(self.filterButton)
        hhbox_x.addWidget(self.paintButton)
        hhbox.addWidget(self.table)  # 把表格加入布局
        hhbox_1.addWidget(self.addItem)
        hhbox_1.addWidget(self.searchItem)
        hhbox_1.addWidget(self.deleteItem)
        hhbox_1.addWidget(self.saveItem)
        vbox.addLayout(hhbox_x)
        vbox.addLayout(hhbox)
        vbox.addLayout(hhbox_1)

        pbox.addWidget(self.geometry)
        pbox.addWidget(self.inlet_boundary)
        pbox.addWidget(self.zw_midspan)
        pbox.addWidget(self.outlet_loss)
        pbox.addWidget(self.outlet_loss_midspan)
        pbox_1.addWidget(self.table_1)
        vbox_1.addLayout(pbox)
        vbox_1.addLayout(pbox_1)
        allbox.addLayout(vbox)
        allbox.addLayout(vbox_1)
        self.setLayout(allbox)  # 创建布局
        self.setWindowTitle("数据库—表格")
        self.setWindowIcon(QIcon("icon.png"))

        self.connecter()

        self.resize(1080, 800)
        self.show()

    def click_find_file_path(self):
        # 设置文件扩展名过滤,同一个类型的不同格式如xlsx和xls 用空格隔开
        directory = QFileDialog.getOpenFileName(None, "选取文件","./", "All Files (*);;Text Files (*.txt)")
        if directory[0] is None or len(directory[0]) == 0:
            pass
        else:
            print(directory[0])
            self.data_upload(directory[0])
            self.initcombox()
            self.flag = 0

    def initcombox(self):
        self.comboBox1.clear()
        self.comboBox2.clear()
        self.comboBox3.clear()
        self.comboBox4.clear()
        self.comboBox1.addItem('叶型', 0)
        self.comboBox2.addItem('雷诺数', 0)
        self.comboBox3.addItem('尾迹/封严实验工况', 0)
        self.comboBox4.addItem('载荷系数', 0)
        self.comboBox1.addItem('---', 1)
        self.comboBox2.addItem('---', 1)
        self.comboBox3.addItem('---', 1)
        self.comboBox4.addItem('---', 1)
        cascades = [i[0] for i in getData(distinctselect.format("cascades", self.table_name))]
        re = [i[0] for i in getData(distinctselect.format("re", self.table_name))]
        wake_f = [i[0] for i in getData(distinctselect.format("wake_f", self.table_name))]
        zw = [str(i[0]) for i in getData(distinctselect.format("zw", self.table_name))]
        for index, item in enumerate(cascades):
            self.comboBox1.addItem(item, index +2)
        for index, item in enumerate(re):
            self.comboBox2.addItem(item, index +2)
        for index, item in enumerate(wake_f):
            self.comboBox3.addItem(item, index +2)
        for index, item in enumerate(zw):
            self.comboBox4.addItem(item, index +2)

    def _filter(self):
        col = []
        values = []
        index = self.comboBox1.currentIndex()
        text = self.comboBox1.itemText(index)
        if text != '---' and text != '叶型':
            col.append('cascades')
            values.append(text)
        index = self.comboBox2.currentIndex()
        text = self.comboBox2.itemText(index)
        if text != '---' and text != '雷诺数' :
            col.append('re')
            values.append(text)
        index = self.comboBox3.currentIndex()
        text = self.comboBox3.itemText(index)
        if text != '---' and text != '尾迹/封严实验工况':
            col.append('wake_f')
            values.append(text)
        index = self.comboBox4.currentIndex()
        text = self.comboBox4.itemText(index)
        if text != '---' and text != '载荷系数':
            col.append('zw')
            values.append(text)
        if len(col) == 0 :
            sql = sel.format(self.table_name)
        else:
            sql = conditionselect.format(self.table_name, sql_condition(col, [[v] for v in values], 'select'))
        print(sql)
        #更新界面
        # self.header = ['']
        # self.displayList = []
        # self.saveList = []
        # data=getData(sql)
        # for index,item in enumerate(data):
        #     self.newLine(index+1,item=item)
        #     self.displayList.append(item)
        # self.saveList=copy(self.displayList)
        # self.table.setRowCount(0)
        # self.table.clearContents()
        self.table_sitting(sql=sql, flag=1)
        # for index,item in enumerate(self.saveList):
        #     self.newLine(index+1,item)
        # self.update()
        self.flag = 1

    def connecter(self):
        self.addItem.clicked.connect(self._addItem)
        self.deleteItem.clicked.connect(self._deleteItem)
        self.searchItem.clicked.connect(self._redraw)
        self.saveItem.clicked.connect(self._saveItem)
        self.table.itemChanged.connect(self._dataChanged)
        self.table.itemClicked.connect(self._drawpaintdata)

    def _drawpaintdata(self):
        columns = [self.table.item(0, i ).text() for i in range(self.columns_num)]
        row_select = self.table.selectedItems()
        if len(row_select) == 0:
            self.show_message("请选中需要展示的参数所在行")
            return
        row= row_select[0].row()
        if row != 0:
            content = [self.table.item(row, i ).text() for i in range(self.columns_num)]
            for i, c in enumerate(columns):
                if c == '叶型':
                    self.cascades = content[i]
                if c == '雷诺数(Re)':
                    self.re = str(content[i])
                if c == '尾迹(F)/封严(PF)实验工况':
                    self.wake_f = content[i]


    def _paint(self):
        """
        一旦检测到数据改变,则进行检查,
        选择添加新数据还是对原数据进行修改
        :return:
        """
        columns = [self.table.item(0, i ).text() for i in range(self.columns_num)]
        row_select = self.table.selectedItems()
        if len(row_select) == 0:
            self.show_message("请选中需要展示的参数所在行")
            return
        row= row_select[0].row()
        content = [self.table.item(row, i ).text() for i in range(self.columns_num)]
        for i, c in enumerate(columns):
            if c == '叶型':
                self.cascades = content[i]
            if c == '雷诺数(Re)':
                self.re = str(content[i])
            if c == '尾迹(F)/封严(PF)实验工况':
                self.wake_f = content[i]
        self.ficture = paint.Paint_Windows(self.cascades, self.re, self.wake_f)
        self.ficture.show()

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
        content = [self.table.item(row, i ).text() if self.table.item(row, i ).text() != '' else 'null' for i in range(self.columns_num)]
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

    def init(self, sql):
        """
        初始化操作
        即从数据库加载数据
        """
        self.displayList = []
        self.saveList = []
        data=getData(sql)
        print("初始化")
        for index,item in enumerate(data):
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
        if self.flag == 0:
            self.init(sql= sel.format(self.table_name))
            self.flag = 1
        else:
            self.initcombox()
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

    def _saveItem(self):
        """
        点击保存需要
        筛选出需要更新的数据
        需要删除的数据
        需要添加的数据
        """
        idList=[int(k[0]) for k in self.saveList]
        _idList=[int(k[0]) for k in self.displayList]
        print("点击保存")
        # print(self.saveList)
        # print(self.displayList)
        for item in self.displayList:
            if item not in self.saveList:
                print("存在修改数据")
                if int(item[0]) not in idList:
                    item = [i if i == 'null' else "'" + str(i) + "'" for i in item]
                    sql=ins.format(self.table_name, '(' + ','.join(self.columns_name[1:-2]) + ')', '(' + ','.join(item[1:-2]) + ')')
                    # sql=ins.format(item[0], item[1], item[2])
                    print(sql)
                    ExecuSQL(sql)
                    print("insert")
                else:
                    item = [i if i == 'null' else "'" + str(i) + "'" for i in item]
                    sql = upd.format(self.table_name, sql_condition(self.columns_name[1:-2], [[v] for v in item][1:-2], 'update'), item[0])
                    print(sql)
                    ExecuSQL(sql)
                    print("update")
        for item in self.saveList:
            if int(item[0]) not in _idList:
                item = [i if i == 'null' else "'" + str(i) + "'" for i in item]
                sql = delete.format(self.table_name, item[0])
                print(sql)
                ExecuSQL(sql)
                print("delete",item)
        self.saveList=copy(self.displayList)

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

    def table_sitting(self,sql=sel.format(TABLE_NAME),flag=1):
        """
        :param flag: 初始化表头和行列数
        """
        self.header = [""]
        name = ['编号', '叶型','雷诺数(Re)','尾迹(F)/封严(PF)实验工况','弦长(mm)','轴向弦长(mm)','栅距(mm)' ,'叶高(mm)','几何进气角(°)','几何出气角(°)','载荷系数','栅后总压损失', '写入时间', '更新时间']
        self.table.setColumnCount(self.columns_num)
        self.table.setRowCount(1)  # 设置表格有两行五列
        for i, c in enumerate(name):
        # for i, c in enumerate(self.columns_name):
            self.table.setItem(0, i, QTableWidgetItem(c))
        # self.table.setItem(0, 0, QTableWidgetItem("学号"))
        # self.table.setItem(0, 1, QTableWidgetItem("名字"))
        # self.table.setItem(0, 2, QTableWidgetItem("出生日期"))
        if flag:
            self.init(sql)

    def init_paint(self, sql):
        """
        初始化操作
        即从数据库加载数据
        """
        self.paint_displayList = []
        self.paint_saveList = []

        data=getData(sql)
        print("初始化")
        self.paint_newLine(0, item = tuple(self.paint_columns_name))
        self.paint_displayList.append(tuple(self.paint_columns_name))
        for index,item in enumerate(data):
            self.paint_newLine(index+1,item=item)
            self.paint_displayList.append(item)
        self.paint_saveList=copy(self.paint_displayList)
        self.table_1.setRowCount(0)
        self.table_1.clearContents()
        # self.table_sitting_paint(sql, paint_table_name = self.paint_table_name, flag=0)
        for index,item in enumerate(self.paint_saveList):
            self.paint_newLine(index,item)
        self.update()

    def paint_newLine(self,num,item=None):
        """
        :param num: 在对应序号处的序号画空白行
        :param item: 输入为对应数据
        """
        # num=self.table_1.rowCount()

        self.table_1.insertRow(num)
        _0= QTableWidgetItem("")
        _0.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        # _1 = QTableWidgetItem("")
        # _2 = QTableWidgetItem("")
        _n = [QTableWidgetItem("") for i in range(self.paint_columns_num - 1)]
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
                _idList=[int(k[0]) for k in self.paint_displayList]
                if _id in _idList:
                    _id = max(_idList) + 1
            _0.setText(str(_id))

        self.table_1.setItem(num, 0, _0)
        for i, n in enumerate(_n):
            self.table_1.setItem(num, i + 1, n)
        # self.table_1.setItem(num, 1, _1)
        # self.table_1.setItem(num, 2, _2)
        self.paint_header.append(str(num))
        self.table_1.setVerticalHeaderLabels(self.paint_header)
        self.update()

    def table_sitting_paint(self, sql, paint_table_name = "geometry", flag=1):
        """
        :param flag: 初始化表头和行列数
        """
        self.paint_table_name = paint_table_name
        self.paint_columns_name = [c[3] for c in getData(col.format(self.paint_table_name))]
        test = []
        for c in self.paint_columns_name:
            if c not in ['id', 'cascades', 're', 'wake_f', 'create_time','update_time']:
                if c == 'p_ss_y':
                    c = '压力面-y'
                if c == 'p_ps_z':
                    c = '压力面-z'
                if c == 'p_ps_y':
                    c = '吸力面-y'
                if c == 'p_ss_z':
                    c = '吸力面-z'
                if c == 'dspan_in' or c == 'dspan_out':
                    c = 'h/H'
                if c == 'dv2_in':
                    c = 'Po-Pc2(Pa)'
                if c == 'dax_chord':
                    c = 'z/CX'
                if c == 'mid_cp':
                    c = 'Cp'
                if c == 'dpitch_mid' or c == 'dpitch_out':
                    c = 'y/Pitch'
                if c == 'mid_cp0' or c == 'out_cp0':
                    c = 'Cp0'
                test.append(c)
        self.paint_columns_name = test
        self.paint_columns_num = len(self.paint_columns_name)
        self.paint_records_num = getData(recordnum.format(self.paint_table_name))[0][0]
        self.paint_header = [""]
        self.table_1.setColumnCount(self.paint_columns_num)
        self.table_1.setRowCount(1)  # 设置表格有两行五列
        for i, c in enumerate(test):
        # for i, c in enumerate(self.paint_columns_name):
            self.table_1.setItem(0, i, QTableWidgetItem(c))
        # self.table_1.setItem(0, 0, QTableWidgetItem("学号"))
        # self.table_1.setItem(0, 1, QTableWidgetItem("名字"))
        # self.table_1.setItem(0, 2, QTableWidgetItem("出生日期"))
        if flag:
            self.init_paint(sql= sql)

    def show_geometry(self):
        self.table_sitting_paint(sel_geometry.format(self.cascades), paint_table_name='geometry')

    def show_inlet_boundary(self):
        self.table_sitting_paint(sel_inlet_boundary.format(self.cascades, self.re, self.wake_f), paint_table_name='inlet_boundary')

    def show_zw_midspan(self):
        self.table_sitting_paint(sel_zw_midspan.format(self.cascades, self.re, self.wake_f), paint_table_name='zw_midspan')

    def show_outlet_loss(self):
        self.table_sitting_paint(sel_outlet_loss.format(self.cascades, self.re, self.wake_f), paint_table_name='outlet_loss')

    def show_outlet_loss_midspan(self):
        self.table_sitting_paint(sel_outlet_loss_midspan.format(self.cascades, self.re, self.wake_f), paint_table_name='outlet_loss_midspan')


    def data_upload(self, path):
        self.one = windows.Upload_Windows(path)
        self.one.show()

    def show_message(self, text):
        QMessageBox.information(self, "提示", text,
                                QMessageBox.Yes) #最后的Yes表示弹框的按钮显示为Yes,默认按钮显示为OK,不填QMessageBox.Yes即为默认


if __name__ == "__main__":
    # upd = "update {} set {} where id={};"
    # a = "pressure = '{}', velity = '{}'"
    # cols = ['pbtrscontractgroup', 'trade_account_id','market_value']
    # values = [['sda'], [1212],[1245]]
    # item = sql_condition(cols, values, 'select')
    # conditionselect = "select * from {} where {}"
    # sql = conditionselect.format('pb_contract_test', item)
    # print(sql)
    # abc = getData(sql)
    create_table()
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap(r"picture.png"))  #启动界面图片地址

    splash.show()
    time.sleep(3)

    dlg = Example()
    splash.finish(dlg)
    sys.exit(app.exec_())



# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     splash = QSplashScreen(QPixmap(r"D:\GUIdemo\fengmian.jpeg"))  #启动界面图片地址
#     splash.show()   #展示启动图片
#     app.processEvents() #防止进程卡死


    # splash.finish(MainWindow)   #关闭启动界面
