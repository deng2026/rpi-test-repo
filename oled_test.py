#!/usr/bin/env python3
# 纯Python驱动0.96寸I2C OLED屏（128x64），无需字体文件
import smbus2
import time

# OLED屏参数
I2C_ADDR = 0x3C  # 若扫描到0x3D则改为0x3D
WIDTH = 128
HEIGHT = 64
I2C_BUS = 1

# 初始化I2C总线
bus = smbus2.SMBus(I2C_BUS)

# OLED屏基础指令（SSD1306芯片）
def oled_write_cmd(cmd):
    bus.write_byte_data(I2C_ADDR, 0x00, cmd)

def oled_write_data(data):
    bus.write_byte_data(I2C_ADDR, 0x40, data)

# 初始化OLED屏
def oled_init():
    oled_write_cmd(0xAE)  # 关闭显示
    oled_write_cmd(0x20)  # 设置内存寻址模式
    oled_write_cmd(0x10)
    oled_write_cmd(0xB0)  # 设置页地址
    oled_write_cmd(0xC8)  # 行扫描方向
    oled_write_cmd(0x00)  # 设置列起始地址低4位
    oled_write_cmd(0x10)  # 设置列起始地址高4位
    oled_write_cmd(0x40)  # 设置显示起始行
    oled_write_cmd(0x81)  # 对比度设置
    oled_write_cmd(0xFF)
    oled_write_cmd(0xA1)  # 段重映射
    oled_write_cmd(0xA6)  # 正常显示
    oled_write_cmd(0xA8)  # 设置多路复用率
    oled_write_cmd(0x3F)
    oled_write_cmd(0xA4)  # 显示全部开启
    oled_write_cmd(0xD3)  # 设置显示偏移
    oled_write_cmd(0x00)
    oled_write_cmd(0xD5)  # 设置时钟分频
    oled_write_cmd(0xF0)
    oled_write_cmd(0xD9)  # 设置预充电周期
    oled_write_cmd(0x22)
    oled_write_cmd(0xDA)  # 设置COM引脚配置
    oled_write_cmd(0x12)
    oled_write_cmd(0xDB)  # 设置VCOMH
    oled_write_cmd(0x20)
    oled_write_cmd(0x8D)  # 启用电荷泵
    oled_write_cmd(0x14)
    oled_write_cmd(0xAF)  # 开启显示

# 清屏
def oled_clear():
    for page in range(8):
        oled_write_cmd(0xB0 + page)
        oled_write_cmd(0x00)
        oled_write_cmd(0x10)
        for _ in range(128):
            oled_write_data(0x00)

# 绘制单个字符（8x16点阵，内置字库，无需外部字体）
# 仅支持数字/字母/简单符号
CHAR_TABLE = {
    '0': [0x3E,0x51,0x49,0x45,0x3E],
    '1': [0x00,0x42,0x7F,0x40,0x00],
    '2': [0x42,0x61,0x51,0x49,0x46],
    '3': [0x22,0x41,0x49,0x49,0x36],
    '4': [0x18,0x14,0x12,0x7F,0x10],
    '5': [0x27,0x45,0x45,0x45,0x39],
    '6': [0x3C,0x4A,0x49,0x49,0x30],
    '7': [0x01,0x71,0x09,0x05,0x03],
    '8': [0x36,0x49,0x49,0x49,0x36],
    '9': [0x06,0x49,0x49,0x29,0x1E],
    'A': [0x7C,0x12,0x11,0x12,0x7C],
    'B': [0x7F,0x49,0x49,0x49,0x36],
    'C': [0x3E,0x41,0x41,0x41,0x22],
    'D': [0x7F,0x41,0x41,0x22,0x1C],
    'E': [0x7F,0x49,0x49,0x49,0x41],
    ' ': [0x00,0x00,0x00,0x00,0x00]
}

def draw_char(x, y, char):
    if char not in CHAR_TABLE:
        char = ' '
    data = CHAR_TABLE[char]
    for i in range(5):
        oled_write_cmd(0xB0 + y)
        oled_write_cmd((x+i) & 0x0F)
        oled_write_cmd(0x10 | ((x+i) >> 4))
        oled_write_data(data[i])

# 绘制字符串（x:0-128, y:0-7）
def draw_string(x, y, string):
    for i, char in enumerate(string):
        draw_char(x + i*6, y, char)

# 主函数
if __name__ == '__main__':
    try:
        oled_init()
        oled_clear()
        
        # 黄色区域（y=0）
        draw_string(2, 0, "OLED TEST")
        # 蓝色区域（y=2）
        draw_string(2, 2, "128x64 I2C")
        # 实时时间（y=4）
        while True:
            draw_string(2, 4, time.strftime("%H:%M:%S"))
            time.sleep(1)
            # 清空时间行（避免重叠）
            draw_string(2, 4, "     ")
    
    except KeyboardInterrupt:
        oled_clear()
        bus.close()
        print("测试结束，已清屏")
