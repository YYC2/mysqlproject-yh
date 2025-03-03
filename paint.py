# -*- coding: UTF-8 -*-
import sys
from copy import copy
from urllib import parse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from sqlalchemy import create_engine
from utils import *
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



sel = "select * from {}"
max_id="select max(id) from {}"
delete="delete from {} where id={}"
ins= "insert into {} {} values {};"
col = "select * from information_schema.COLUMNS where table_name='{}';"
recordnum = "select count(*) from {}"
upd = "update {} set {} where id={};"
conditionselect = "select * from {} where {}"
distinctselect = "select DISTINCT({}) from {}"

sel_geometry = "select p_ss_y as '压力面-y', p_ps_z as '压力面-z', p_ps_y as '吸力面-y',p_ss_z as '吸力面-y' from geometry where cascades= '{}'"

sel_inlet_boundary = "select dspan_in as 'h/H', dv2_in as 'Po-Pc2' from inlet_boundary where cascades= '{}' and re = {} and wake_f = '{}'"

sel_zw_midspan = "select dax_chord  as 'z/CX', mid_cp  as 'Cp' from zw_midspan where cascades= '{}' and re = {} and wake_f = '{}'"

sel_outlet_loss_midspan = "select dpitch_mid  as 'y/Pitch', mid_cp0  as 'Cp0' from outlet_loss_midspan where cascades= '{}' and re = {} and wake_f = '{}'"

sel_outlet_loss = "select dpitch_out  as 'y/Pitch', dspan_out  as 'h/H', out_cp0 as 'Cp0' from outlet_loss where cascades= '{}' and re = {} and wake_f = '{}'"

class Paint_Windows(QWidget):
    def __init__(self, cascades, re, wake_f, parent=None):
        super(Paint_Windows, self).__init__(parent)
        vbox=QVBoxLayout()
        pbox=QHBoxLayout()
        # hpbox_1 = QHBoxLayout()
        # pbox_2=QHBoxLayout()
        self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(USER_NAME, parse.quote_plus(USER_PASSWORD), ADDRESS, '3306', 'igouwu'))

        self.cascades = cascades
        self.re = re
        self.wake_f = wake_f

        # self.paint_table_name = "geometry"
        # self.paint_columns_name = [c[3] for c in getData(col.format(self.paint_table_name))]
        # test = []
        # for c in self.paint_columns_name:
        #     if c not in ['id', 'cascades', 're', 'wake_f', 'create_time','update_time']:
        #         test.append(c)
        # self.paint_columns_name = test
        # self.paint_columns_num = len(self.paint_columns_name)
        # self.paint_records_num = getData(recordnum.format(self.paint_table_name))[0][0]
        # self.table_1 = QTableWidget()
        # self.table_sitting_paint(sel_geometry.format(self.cascades))
        #
        # self.geometry=QPushButton("叶栅几何")
        # self.inlet_boundary=QPushButton("进口边界")
        # self.zw_midspan=QPushButton("叶中载荷分布")
        # self.outlet_loss=QPushButton("出口40%位置截面总压损失")
        # self.outlet_loss_midspan = QPushButton("出口40%位置叶中总压损失")
        #
        # self.geometry.clicked.connect(self.show_geometry)
        # self.inlet_boundary.clicked.connect(self.show_inlet_boundary)
        # self.zw_midspan.clicked.connect(self.show_zw_midspan)
        # self.outlet_loss.clicked.connect(self.show_outlet_loss)
        # self.outlet_loss_midspan.clicked.connect(self.show_outlet_loss_midspan)


        self.gridLayout = QVBoxLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addStretch(1)
        # self.figure = plt.figure(facecolor='#FFD7C4')
        self.figure = plt.figure() # 新建绘图区域
        self.canvas = FigureCanvas(self.figure) # 绘图区域放到图层canvas之中
        self.gridLayout.addWidget(self.canvas)
        self.gridLayout.addStretch(1)# 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）
        self.paint_profile(cascades = cascades)

        self.gridLayout2 = QVBoxLayout()
        self.gridLayout2.addStretch(1)
        self.gridLayout2.setObjectName("gridLayout")


        self.figure1 = plt.figure()  # 新建绘图区域
        self.canvas1 = FigureCanvas(self.figure1)  # 绘图区域放到图层canvas之中
        self.gridLayout2.addWidget(self.canvas1)  # 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）
        self.gridLayout2.addStretch(1)
        self.paint_midspan_loss(cascades = cascades, wake_f = wake_f, re = re)

        self.gridLayout3 = QVBoxLayout()
        self.gridLayout3.addStretch(1)
        self.gridLayout3.setObjectName("gridLayout")


        self.figure2 = plt.figure()  # 新建绘图区域
        self.canvas2 = FigureCanvas(self.figure2)  # 绘图区域放到图层canvas之中
        self.gridLayout3.addWidget(self.canvas2)  # 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）
        self.gridLayout3.addStretch(1)

        self.paint_static_coefficient(cascades = cascades, wake_f = wake_f, re = re)


        pbox.addLayout(self.gridLayout)
        pbox.addLayout(self.gridLayout2)
        pbox.addLayout(self.gridLayout3)
        # hpbox_1.addWidget(self.geometry)
        # hpbox_1.addWidget(self.inlet_boundary)
        # hpbox_1.addWidget(self.zw_midspan)
        # hpbox_1.addWidget(self.outlet_loss)
        # hpbox_1.addWidget(self.outlet_loss_midspan)
        # pbox_2.addWidget(self.table_1)
        vbox.addLayout(pbox)
        # vbox.addLayout(hpbox_1)
        # vbox.addLayout(pbox_2)
        self.setLayout(vbox)  # 创建布局
        self.setWindowTitle("参数绘图")


        self.resize(1800, 600)
        self.show()
    #
    # def show_geometry(self):
    #     self.table_sitting_paint(sel_geometry.format(self.cascades), paint_table_name='geometry')
    #
    # def show_inlet_boundary(self):
    #     self.table_sitting_paint(sel_inlet_boundary.format(self.cascades, self.re, self.wake_f), paint_table_name='inlet_boundary')
    #
    # def show_zw_midspan(self):
    #     self.table_sitting_paint(sel_zw_midspan.format(self.cascades, self.re, self.wake_f), paint_table_name='zw_midspan')
    #
    # def show_outlet_loss(self):
    #     self.table_sitting_paint(sel_outlet_loss.format(self.cascades, self.re, self.wake_f), paint_table_name='outlet_loss')
    #
    # def show_outlet_loss_midspan(self):
    #     self.table_sitting_paint(sel_outlet_loss_midspan.format(self.cascades, self.re, self.wake_f), paint_table_name='outlet_loss_midspan')

    def closeEvent(self, event):  # 关闭窗口触发以下事件
        a = QMessageBox.question(self, '退出', '你确定要退出吗?', QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)  # "退出"代表的是弹出框的标题,"你确认退出.."表示弹出框的内容
        if a == QMessageBox.Yes:
            event.accept()  # 接受关闭事件
        else:
            event.ignore()


    def plot_test(self):
        x = np.arange(1,1000)
        y = x**2
        plt.plot(x,y)
        self.canvas.draw() # 这是关键

    #叶栅几何
    def paint_profile(self, paint_table_name='geometry', cascades = 'PackB'):
        # df = pd.read_excel("./数据模板改.xlsx", sheet_name="叶栅几何")
        df = pd.read_sql_query(sel.format(paint_table_name), self.engine)
        df = df[df['cascades'] == cascades]
        self.plot_profile(df['p_ps_y'].tolist(),df['p_ps_z'].tolist(),df['p_ss_y'].tolist(),df['p_ss_z'].tolist())

    #40%叶中总压损失
    def paint_midspan_loss(self, paint_table_name='outlet_loss_midspan', cascades = 'PackB', wake_f = '定常', re = '25000'):
        # df = pd.read_excel("./数据模板改.xlsx", sheet_name="出口40%位置叶中总压损失")
        df = pd.read_sql_query(sel.format(paint_table_name), self.engine)
        df = df[df['cascades'] == cascades]
        df = df[df['wake_f'] == wake_f]
        df = df[df['re'] == re]
        self.plot_midspan_loss(df['dpitch_mid'].tolist(),df['mid_cp0'].tolist())

    #叶中载荷分布
    def paint_static_coefficient(self, paint_table_name='zw_midspan', cascades = 'PackB', wake_f = '定常', re = '25000'):
        # df = pd.read_excel("./数据模板改.xlsx", sheet_name="叶中载荷分布")
        df = pd.read_sql_query(sel.format(paint_table_name), self.engine)
        df = df[df['cascades'] == cascades]
        df = df[df['wake_f'] == wake_f]
        df = df[df['re'] == re]
        self.plot_static_coefficient(df['dax_chord'].tolist(),df['mid_cp'].tolist())


    #叶栅几何
    def plot_profile(self,zP_PS,yP_PS,zP_SS,yP_SS):
        plt.grid()
        plt.xlabel('z', fontsize=40, fontproperties='Times New Roman', fontweight="bold")
        plt.ylabel('y', fontsize=40, fontproperties='Times New Roman', fontweight="bold")
        plt.title('Geometry', fontweight="bold", fontproperties='Times New Roman',fontsize=23)
        plt.xticks(fontproperties='Times New Roman', size=20)
        plt.yticks(fontproperties='Times New Roman', size=20)
        plt.plot(yP_PS, zP_PS, linewidth=1, color="r", label="Sunction_side")
        plt.plot(yP_SS, zP_SS, linewidth=1, color="b", label="Pressure_side")
        plt.legend(["Sunction side", "Pressure side"], loc="lower left", prop={"family":"Times New Roman", "size": 20})
        self.canvas.draw() # 这是关键
        # plt.show()

    #40%叶中总压损失
    def plot_midspan_loss(self,Dpitch_mid,Mid_Cp0):
        plt.title('Total Pressure Loss Coefficient', fontweight="bold", fontproperties='Times New Roman',fontsize=23)
        plt.grid()
        plt.xlabel('y/Pitch', fontsize=40, fontproperties='Times New Roman', fontweight="bold")
        plt.ylabel('Total Pressure Loss Coefficient', fontsize=40, fontproperties='Times New Roman', fontweight="bold")
        plt.xticks(fontproperties='Times New Roman', size=20)
        plt.yticks(fontproperties='Times New Roman', size=20)
        plt.plot(Dpitch_mid, Mid_Cp0, linewidth=2, color="orange", marker="o",markersize=6)
        self.canvas1.draw() # 这是关键

    #叶中载荷分布
    def plot_static_coefficient(self, Dax_chord,Mid_Cp):
        plt.title('Static Pressure Coefficient', fontweight="bold", fontproperties='Times New Roman',fontsize=23)
        plt.grid()
        plt.xlabel('z/Cx', fontsize=40, fontproperties='Times New Roman', fontweight="bold")
        plt.ylabel('Static Pressure Coefficient', fontsize=40, fontproperties='Times New Roman', fontweight="bold")
        plt.xticks(fontproperties='Times New Roman', size=20)
        plt.yticks(fontproperties='Times New Roman', size=20)
        plt.scatter(Dax_chord,Mid_Cp,color="g", marker="o",s=60)
        self.canvas2.draw() # 这是关键
    #
    #     def _dataChanged(self):
    #         """
    #         一旦检测到数据改变,则进行检查,
    #         选择添加新数据还是对原数据进行修改
    #         :return:
    #         """
    #     row_select = self.table_1.selectedItems()
    #     if len(row_select) == 0:
    #         return
    #     row= row_select[0].row()
    #     content = [self.table_1.item(row, i ).text() if self.table_1.item(row, i ).text() != '' else 'null' for i in range(self.columns_num)]
    #     content = tuple(content)
    #     # content = (self.table_1.item(row, 0).text(), self.table_1.item(row, 1).text(),
    #     #            self.table_1.item(row, 2).text())
    #
    #     if row<=len(self.paint_displayList):
    #         print("修改行",content)
    #         self.paint_displayList[row-1]=content
    #     else:
    #         print("最新行",content)
    #         self.paint_displayList.append(content)
    # #
    #
    # def init_paint(self, sql):
    #     """
    #     初始化操作
    #     即从数据库加载数据
    #     """
    #     self.paint_displayList = []
    #     self.paint_saveList = []
    #
    #     data=getData(sql)
    #     print("初始化")
    #     self.paint_newLine(0, item = tuple(self.paint_columns_name))
    #     self.paint_displayList.append(tuple(self.paint_columns_name))
    #     for index,item in enumerate(data):
    #         self.paint_newLine(index+1,item=item)
    #         self.paint_displayList.append(item)
    #     self.paint_saveList=copy(self.paint_displayList)
    #     self.table_1.setRowCount(0)
    #     self.table_1.clearContents()
    #     # self.table_sitting_paint(sql, paint_table_name = self.paint_table_name, flag=0)
    #     for index,item in enumerate(self.paint_saveList):
    #         self.paint_newLine(index,item)
    #     self.update()
    #
    # def paint_newLine(self,num,item=None):
    #     """
    #     :param num: 在对应序号处的序号画空白行
    #     :param item: 输入为对应数据
    #     """
    #     # num=self.table_1.rowCount()
    #
    #     self.table_1.insertRow(num)
    #     _0= QTableWidgetItem("")
    #     _0.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    #     # _1 = QTableWidgetItem("")
    #     # _2 = QTableWidgetItem("")
    #     _n = [QTableWidgetItem("") for i in range(self.paint_columns_num - 1)]
    #     # item=studentInfo()
    #     if item !=None:
    #         _0.setText(str(item[0]))
    #         for i, n in enumerate(_n):
    #             n.setText(str(item[i + 1]))
    #         # _1.setText(str(item[1]))
    #         # _2.setText(str(item[2]))
    #     else:
    #         _id = num
    #         if item == None:
    #             _idList=[int(k[0]) for k in self.paint_displayList]
    #             if _id in _idList:
    #                 _id = max(_idList) + 1
    #         _0.setText(str(_id))
    #
    #     self.table_1.setItem(num, 0, _0)
    #     for i, n in enumerate(_n):
    #         self.table_1.setItem(num, i + 1, n)
    #     # self.table_1.setItem(num, 1, _1)
    #     # self.table_1.setItem(num, 2, _2)
    #     self.paint_header.append(str(num))
    #     self.table_1.setVerticalHeaderLabels(self.paint_header)
    #     self.update()
    #
    # def table_sitting_paint(self, sql, paint_table_name = "geometry", flag=1):
    #     """
    #     :param flag: 初始化表头和行列数
    #     """
    #     self.paint_table_name = paint_table_name
    #     self.paint_columns_name = [c[3] for c in getData(col.format(self.paint_table_name))]
    #     test = []
    #     for c in self.paint_columns_name:
    #         if c not in ['id', 'cascades', 're', 'wake_f', 'create_time','update_time']:
    #             test.append(c)
    #     self.paint_columns_name = test
    #     self.paint_columns_num = len(self.paint_columns_name)
    #     self.paint_records_num = getData(recordnum.format(self.paint_table_name))[0][0]
    #     self.paint_header = [""]
    #     self.table_1.setColumnCount(self.paint_columns_num)
    #     self.table_1.setRowCount(1)  # 设置表格有两行五列
    #     for i, c in enumerate(self.paint_columns_name):
    #         self.table_1.setItem(0, i, QTableWidgetItem(c))
    #     # self.table_1.setItem(0, 0, QTableWidgetItem("学号"))
    #     # self.table_1.setItem(0, 1, QTableWidgetItem("名字"))
    #     # self.table_1.setItem(0, 2, QTableWidgetItem("出生日期"))
    #     if flag:
    #         self.init_paint(sql= sql)
    #
if __name__ == "__main__":
    # wirte_csv(1, "pb_contract_test")
    app = QApplication(sys.argv)
    dlg = Paint_Windows(cascades = 'PackB', wake_f = '定常', re = 25000)
    sys.exit(app.exec_())

