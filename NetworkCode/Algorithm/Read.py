import re
import csv

def read_port_name_info():
    '''
    这个函数是为了消除 数据中港口名称有问题而产生的影响  相当于是做一个规范化
    :return: 返回一个dict key为输入的port name  value为正确的port name
    '''
    # 读取port Name
    PortName = {}

    # 逐行读取csv文档
    with open('../Data/Port/PortInfo.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines[1:]:

        # 去掉行尾的换行符号
        line = line.strip()
        # 切分
        parts = line.split(";")

        # 切分后第一段是港口  第二段是正确的港口信息
        Port = parts[0].strip()
        RightPort = parts[1].strip()

        PortName[Port] = RightPort
    return PortName
def read_remove_port_info():
    '''

    :return: 返回一个list 是已经标记好的错误的port name
    '''
    # 初始化一个空列表来存储港口名称
    ports_list = []

    # 打开文件并读取内容
    with open('../Data/Port/Error_Port.txt', 'r', encoding='utf-8') as file:
        # 逐行读取文件
        for line in file:
            # 去除每行末尾的换行符并添加到列表中
            ports_list.append(str(line.strip()))
    return ports_list
def read_USImpHSCode_Origin():
    '''
    处理原始数据
    :return: 返回一个 dict  key 为 USImpRecordId   value 为 HSCode
    '''
    # 读取 USImpHSCode
    USImpHSCode = dict()

    # 逐行读取csv文档
    with open('D:/PortData/USImpHSCode/panjivaUSImpHSCode.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        try:
            # 去掉行尾的换行符号
            line = line.strip()
            # 切分
            parts = line.split(",")

            # 切分后第一段是交易记录ID  第二段是HSCode
            RecordId = parts[0].strip()
            HScode = parts[1].strip()

            # 使用正则表达式提取前两个数字
            match = re.search(r'\d{1,2}', HScode)

            if match:
                # 将匹配到的字符串转换为整数
                HScode = int(match.group())
            else:
                HScode = None

            USImpHSCode[RecordId] = HScode
        except IndexError as i:
            print(RecordId)
    return USImpHSCode
def save_USImpHSCode(dict_data):
    # 指定要保存的 CSV 文件名
    filename = 'D:/PortData/USImpHSCode/USImpHSCode.csv'

    # 打开文件并写入内容
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # 创建一个 CSV 写入器
        writer = csv.writer(csvfile)

        # 遍历字典的每个键值对
        for key, value in dict_data.items():
            # 将键值对写入 CSV 文件，每个键值对占一行
            writer.writerow([key, value])