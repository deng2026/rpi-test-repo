# 导入所需库：RPi.GPIO（GPIO控制）、time（延时功能）
import RPi.GPIO as GPIO
import time

# 配置核心参数（与接线对应，修改GPIO_PIN需同步调整硬件接线）
LED_PIN = 18  # 控制LED的GPIO引脚（BCM编号，对应物理引脚12）
FLASH_INTERVAL = 1  # LED闪烁间隔，单位：秒（1秒亮/1秒灭）
FLASH_TIMES = 10  # 闪烁总次数（0表示无限闪烁，按Ctrl+C停止）

def init_led():
    """初始化LED引脚"""
    # 设置GPIO编号规则：BCM（树莓派官方推荐，与引脚标注一致）
    GPIO.setmode(GPIO.BCM)
    # 关闭GPIO警告信息（避免重复运行报错）
    GPIO.setwarnings(False)
    # 配置LED_PIN为输出模式（用于向LED发送高低电平信号）
    GPIO.setup(LED_PIN, GPIO.OUT)
    # 初始化LED为熄灭状态（低电平）
    GPIO.output(LED_PIN, GPIO.LOW)
    print("LED初始化完成，引脚：GPIO{}".format(LED_PIN))

def led_flash():
    """LED闪烁功能实现"""
    init_led()  # 先初始化LED
    try:
        if FLASH_TIMES == 0:
            # 无限闪烁模式
            print("LED进入无限闪烁模式，按Ctrl+C停止...")
            while True:
                GPIO.output(LED_PIN, GPIO.HIGH)  # 点亮LED（高电平）
                print("LED → 亮")
                time.sleep(FLASH_INTERVAL)  # 保持亮灯状态
                
                GPIO.output(LED_PIN, GPIO.LOW)   # 熄灭LED（低电平）
                print("LED → 灭")
                time.sleep(FLASH_INTERVAL)  # 保持熄灭状态
        else:
            # 指定次数闪烁模式
            print("LED将闪烁{}次，间隔{}秒...".format(FLASH_TIMES, FLASH_INTERVAL))
            for i in range(1, FLASH_TIMES + 1):
                GPIO.output(LED_PIN, GPIO.HIGH)  # 点亮LED
                print("第{}次闪烁 → LED亮".format(i))
                time.sleep(FLASH_INTERVAL)
                
                GPIO.output(LED_PIN, GPIO.LOW)   # 熄灭LED
                print("第{}次闪烁 → LED灭".format(i))
                time.sleep(FLASH_INTERVAL)
    except KeyboardInterrupt:
        # 按Ctrl+C时，优雅退出程序
        print("\n用户手动停止程序")
    finally:
        # 无论程序正常结束还是异常退出，均清理GPIO资源
        GPIO.output(LED_PIN, GPIO.LOW)  # 确保LED最终处于熄灭状态
        GPIO.cleanup()  # 释放GPIO引脚，避免占用
        print("GPIO资源已清理，程序结束")

# 程序入口（直接运行该文件即可执行）
if __name__ == "__main__":
    led_flash()
