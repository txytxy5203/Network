

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

