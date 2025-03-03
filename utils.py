# -*-coding:GBK-*-
import pymysql

USER_NAME = 'root'
USER_PASSWORD ='123456'
ADDRESS = '127.0.0.1'

# USER_NAME = 'yc2'
# USER_PASSWORD ='555578'
# ADDRESS = '192.168.122.129'

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


def getCursor():
    conn = pymysql.connect(host=ADDRESS  # 连接名称，默认127.0.0.1
                           , user=USER_NAME  # 用户名
                           , passwd=USER_PASSWORD  # 密码
                           , port=3306  # 端口，默认为3306
                           , db='igouwu'  # 数据库名称
                           , charset='utf8'  # 字符编码
                           )
    return conn

def getCursor_datebase():
    conn = pymysql.connect(host=ADDRESS  # 连接名称，默认127.0.0.1
                           , user=USER_NAME  # 用户名
                           , passwd=USER_PASSWORD  # 密码
                           , port=3306  # 端口，默认为3306
                           , charset='utf8'  # 字符编码
                           )
    return conn

def ExecuSQL_datebase(argv):
    conn=getCursor_datebase()
    cur = conn.cursor()  # 生成游标对象
    cur.execute(argv)  # 执行SQL语句
    conn.commit()
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接

def ExecuSQL(argv):
    conn=getCursor()
    cur = conn.cursor()  # 生成游标对象
    cur.execute(argv)  # 执行SQL语句
    conn.commit()
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接

def getData(argv):
    conn = getCursor()
    cur = conn.cursor()  # 生成游标对象
    cur.execute(argv)  # 执行SQL语句
    data = cur.fetchall()  # 通过fetchall方法获得数据
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接
    return data

def create_table():
    ExecuSQL_datebase(sql0)
    ExecuSQL(sql1)
    ExecuSQL(sql2)
    ExecuSQL(sql3)
    ExecuSQL(sql4)
    ExecuSQL(sql5)
    ExecuSQL(sql6)

sql0 = "CREATE DATABASE IF NOT EXISTS `igouwu`;"

sql1 = '''CREATE TABLE IF NOT EXISTS `exp_input_param` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `cascades` varchar(100) DEFAULT NULL COMMENT '叶型',
  `re` varchar(100) DEFAULT NULL COMMENT '雷诺数(Re)',
  `wake_f` varchar(100) DEFAULT NULL COMMENT '尾迹扫掠频率(F)',
  `chord` decimal(15,2) DEFAULT NULL COMMENT '弦长(mm)',
  `ax_chord` decimal(15,2) DEFAULT NULL COMMENT '轴向弦长(mm)',
  `pitch` decimal(15,2) DEFAULT NULL COMMENT '栅距(mm)',
  `span` decimal(15,2) DEFAULT NULL COMMENT '叶高(mm)',
  `in_angle` decimal(15,2) DEFAULT NULL COMMENT '几何进气角(°)',
  `out_angle` decimal(15,2) DEFAULT NULL COMMENT '几何出气角(°)',
  `zw` decimal(15,2) DEFAULT NULL COMMENT '载荷系数',
  `loss` decimal(15,4) DEFAULT NULL COMMENT '载荷系数',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COMMENT='叶栅实验数据表';'''


sql2 = '''CREATE TABLE IF NOT EXISTS `geometry` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `cascades` varchar(100) DEFAULT NULL COMMENT '叶型',
  `p_ps_y` decimal(15,10) DEFAULT NULL COMMENT '叶栅几何压力面-y',
  `p_ps_z` decimal(15,10) DEFAULT NULL COMMENT '叶栅几何压力面-z',
  `p_ss_y` decimal(15,10) DEFAULT NULL COMMENT '叶栅几何吸力面-y',
  `p_ss_z` decimal(15,10) DEFAULT NULL COMMENT '叶栅几何吸力面-z',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=330 DEFAULT CHARSET=utf8mb4 COMMENT='叶栅几何数据表';'''


sql3 = '''CREATE TABLE IF NOT EXISTS `inlet_boundary` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `cascades` varchar(100) DEFAULT NULL COMMENT '叶型',
  `re` varchar(100) DEFAULT NULL COMMENT '雷诺数(Re)',
  `wake_f` varchar(100) DEFAULT NULL COMMENT '尾迹扫掠频率(F)',
  `dspan_in` decimal(15,10) DEFAULT NULL COMMENT '进口边界h/H',
  `dv2_in` decimal(15,4) DEFAULT NULL COMMENT '进口边界Po-Pc2',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2164 DEFAULT CHARSET=utf8mb4 COMMENT='进口边界数据表';'''


sql4 = '''CREATE TABLE IF NOT EXISTS `zw_midspan` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `cascades` varchar(100) DEFAULT NULL COMMENT '叶型',
  `re` varchar(100) DEFAULT NULL COMMENT '雷诺数(Re)',
  `wake_f` varchar(100) DEFAULT NULL COMMENT '尾迹扫掠频率(F)',
  `dax_chord` decimal(15,10) DEFAULT NULL COMMENT '叶中载荷分布z/CX',
  `mid_cp` decimal(15,10) DEFAULT NULL COMMENT '叶中载荷分布Cp',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=308 DEFAULT CHARSET=utf8mb4 COMMENT='叶中载荷分布数据表';'''


sql5 = '''CREATE TABLE IF NOT EXISTS `outlet_loss` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `cascades` varchar(100) DEFAULT NULL COMMENT '叶型',
  `re` varchar(100) DEFAULT NULL COMMENT '雷诺数(Re)',
  `wake_f` varchar(100) DEFAULT NULL COMMENT '尾迹扫掠频率(F)',
  `dpitch_out` decimal(15,10) DEFAULT NULL COMMENT '截面总压损失y/Pitch',
  `dspan_out` decimal(15,10) DEFAULT NULL COMMENT '截面总压损失h/H',
  `out_cp0` decimal(15,10) DEFAULT NULL COMMENT '截面总压损失Cp0',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19658 DEFAULT CHARSET=utf8mb4 COMMENT='出口40%位置截面总压损失分布数据表';'''

sql6 = '''CREATE TABLE IF NOT EXISTS `outlet_loss_midspan` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `cascades` varchar(100) DEFAULT NULL COMMENT '叶型',
  `re` varchar(100) DEFAULT NULL COMMENT '雷诺数(Re)',
  `wake_f` varchar(100) DEFAULT NULL COMMENT '尾迹扫掠频率(F)',
  `dpitch_mid` decimal(15,10) DEFAULT NULL COMMENT '叶中总压损失y/Pitch',
  `mid_cp0` decimal(15,10) DEFAULT NULL COMMENT '叶中总压损失Cp0',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2959 DEFAULT CHARSET=utf8mb4 COMMENT='出口40%位置叶中总压损失分布';'''