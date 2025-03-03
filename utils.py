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
    conn = pymysql.connect(host=ADDRESS  # �������ƣ�Ĭ��127.0.0.1
                           , user=USER_NAME  # �û���
                           , passwd=USER_PASSWORD  # ����
                           , port=3306  # �˿ڣ�Ĭ��Ϊ3306
                           , db='igouwu'  # ���ݿ�����
                           , charset='utf8'  # �ַ�����
                           )
    return conn

def getCursor_datebase():
    conn = pymysql.connect(host=ADDRESS  # �������ƣ�Ĭ��127.0.0.1
                           , user=USER_NAME  # �û���
                           , passwd=USER_PASSWORD  # ����
                           , port=3306  # �˿ڣ�Ĭ��Ϊ3306
                           , charset='utf8'  # �ַ�����
                           )
    return conn

def ExecuSQL_datebase(argv):
    conn=getCursor_datebase()
    cur = conn.cursor()  # �����α����
    cur.execute(argv)  # ִ��SQL���
    conn.commit()
    cur.close()  # �ر��α�
    conn.close()  # �ر�����

def ExecuSQL(argv):
    conn=getCursor()
    cur = conn.cursor()  # �����α����
    cur.execute(argv)  # ִ��SQL���
    conn.commit()
    cur.close()  # �ر��α�
    conn.close()  # �ر�����

def getData(argv):
    conn = getCursor()
    cur = conn.cursor()  # �����α����
    cur.execute(argv)  # ִ��SQL���
    data = cur.fetchall()  # ͨ��fetchall�����������
    cur.close()  # �ر��α�
    conn.close()  # �ر�����
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
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '����',
  `cascades` varchar(100) DEFAULT NULL COMMENT 'Ҷ��',
  `re` varchar(100) DEFAULT NULL COMMENT '��ŵ��(Re)',
  `wake_f` varchar(100) DEFAULT NULL COMMENT 'β��ɨ��Ƶ��(F)',
  `chord` decimal(15,2) DEFAULT NULL COMMENT '�ҳ�(mm)',
  `ax_chord` decimal(15,2) DEFAULT NULL COMMENT '�����ҳ�(mm)',
  `pitch` decimal(15,2) DEFAULT NULL COMMENT 'դ��(mm)',
  `span` decimal(15,2) DEFAULT NULL COMMENT 'Ҷ��(mm)',
  `in_angle` decimal(15,2) DEFAULT NULL COMMENT '���ν�����(��)',
  `out_angle` decimal(15,2) DEFAULT NULL COMMENT '���γ�����(��)',
  `zw` decimal(15,2) DEFAULT NULL COMMENT '�غ�ϵ��',
  `loss` decimal(15,4) DEFAULT NULL COMMENT '�غ�ϵ��',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '��¼����ʱ��',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '��¼�޸�ʱ��',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COMMENT='Ҷդʵ�����ݱ�';'''


sql2 = '''CREATE TABLE IF NOT EXISTS `geometry` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '����',
  `cascades` varchar(100) DEFAULT NULL COMMENT 'Ҷ��',
  `p_ps_y` decimal(15,10) DEFAULT NULL COMMENT 'Ҷդ����ѹ����-y',
  `p_ps_z` decimal(15,10) DEFAULT NULL COMMENT 'Ҷդ����ѹ����-z',
  `p_ss_y` decimal(15,10) DEFAULT NULL COMMENT 'Ҷդ����������-y',
  `p_ss_z` decimal(15,10) DEFAULT NULL COMMENT 'Ҷդ����������-z',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '��¼����ʱ��',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '��¼�޸�ʱ��',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=330 DEFAULT CHARSET=utf8mb4 COMMENT='Ҷդ�������ݱ�';'''


sql3 = '''CREATE TABLE IF NOT EXISTS `inlet_boundary` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '����',
  `cascades` varchar(100) DEFAULT NULL COMMENT 'Ҷ��',
  `re` varchar(100) DEFAULT NULL COMMENT '��ŵ��(Re)',
  `wake_f` varchar(100) DEFAULT NULL COMMENT 'β��ɨ��Ƶ��(F)',
  `dspan_in` decimal(15,10) DEFAULT NULL COMMENT '���ڱ߽�h/H',
  `dv2_in` decimal(15,4) DEFAULT NULL COMMENT '���ڱ߽�Po-Pc2',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '��¼����ʱ��',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '��¼�޸�ʱ��',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2164 DEFAULT CHARSET=utf8mb4 COMMENT='���ڱ߽����ݱ�';'''


sql4 = '''CREATE TABLE IF NOT EXISTS `zw_midspan` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '����',
  `cascades` varchar(100) DEFAULT NULL COMMENT 'Ҷ��',
  `re` varchar(100) DEFAULT NULL COMMENT '��ŵ��(Re)',
  `wake_f` varchar(100) DEFAULT NULL COMMENT 'β��ɨ��Ƶ��(F)',
  `dax_chord` decimal(15,10) DEFAULT NULL COMMENT 'Ҷ���غɷֲ�z/CX',
  `mid_cp` decimal(15,10) DEFAULT NULL COMMENT 'Ҷ���غɷֲ�Cp',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '��¼����ʱ��',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '��¼�޸�ʱ��',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=308 DEFAULT CHARSET=utf8mb4 COMMENT='Ҷ���غɷֲ����ݱ�';'''


sql5 = '''CREATE TABLE IF NOT EXISTS `outlet_loss` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '����',
  `cascades` varchar(100) DEFAULT NULL COMMENT 'Ҷ��',
  `re` varchar(100) DEFAULT NULL COMMENT '��ŵ��(Re)',
  `wake_f` varchar(100) DEFAULT NULL COMMENT 'β��ɨ��Ƶ��(F)',
  `dpitch_out` decimal(15,10) DEFAULT NULL COMMENT '������ѹ��ʧy/Pitch',
  `dspan_out` decimal(15,10) DEFAULT NULL COMMENT '������ѹ��ʧh/H',
  `out_cp0` decimal(15,10) DEFAULT NULL COMMENT '������ѹ��ʧCp0',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '��¼����ʱ��',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '��¼�޸�ʱ��',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19658 DEFAULT CHARSET=utf8mb4 COMMENT='����40%λ�ý�����ѹ��ʧ�ֲ����ݱ�';'''

sql6 = '''CREATE TABLE IF NOT EXISTS `outlet_loss_midspan` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '����',
  `cascades` varchar(100) DEFAULT NULL COMMENT 'Ҷ��',
  `re` varchar(100) DEFAULT NULL COMMENT '��ŵ��(Re)',
  `wake_f` varchar(100) DEFAULT NULL COMMENT 'β��ɨ��Ƶ��(F)',
  `dpitch_mid` decimal(15,10) DEFAULT NULL COMMENT 'Ҷ����ѹ��ʧy/Pitch',
  `mid_cp0` decimal(15,10) DEFAULT NULL COMMENT 'Ҷ����ѹ��ʧCp0',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '��¼����ʱ��',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '��¼�޸�ʱ��',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2959 DEFAULT CHARSET=utf8mb4 COMMENT='����40%λ��Ҷ����ѹ��ʧ�ֲ�';'''