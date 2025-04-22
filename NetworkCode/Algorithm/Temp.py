import matplotlib.pyplot as plt

# 定义颜色列表
colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

# 创建一个新的图形
plt.figure(figsize=(10, 4))

# 遍历颜色列表并绘制每个颜色的条形图
for i, color in enumerate(colors):
    plt.bar(i, 1, color=color)

# 设置x轴的刻度标签
plt.xticks(ticks=range(len(colors)), labels=colors)

# 添加图例
plt.legend(colors)

# 添加标题和轴标签
plt.title('Color Display')
plt.xlabel('Color Index')
plt.ylabel('Value')

# 显示图形
plt.show()