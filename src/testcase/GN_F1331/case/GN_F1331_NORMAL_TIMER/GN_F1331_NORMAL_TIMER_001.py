# coding=utf-8
from src.testcase.GN_F1331.WidgetOperation import *


class GNF1331NormalTimer1(WidgetOperation):
    @case_run(False)
    def run(self):
        self.case_module = u"APP功能测试"  # 用例所属模块
        self.case_title = u'上层循环定时'  # 用例名称
        self.zentao_id = 1216  # 禅道ID

    # 用例动作
    def case(self):
        self.choose_home_device(conf["MAC"][self.app][self.device_mac])

        self.delete_out_date_timer()

        self.set_power("main_button_off")

        self.input_serial_command("power", "set_cycle_timer", "launch_cycle_timer_on", "launch_cycle_timer_off")

        self.widget_click(self.page["control_device_page"]["up_timer"],
                          self.page["up_timer_page"]["title"])

        now = time.strftime("%H:%M")

        delay_time_1, delay_time_2 = ["delay", "00:01"], ["delay", "00:01"]
        tmp = self.create_cycle_timer("up_timer_page", now, delay_time_1, delay_time_2, u"永久循环")
        start_time_1, set_time_1, start_time_2, set_time_2 = tmp[0]

        while True:
            if time.time() > set_time_2 + 10:
                break
            print(time.time())
            time.sleep(1)

        #####
        btn_state_list = self.check_serial_button_state()  # 开关
        set_cycle_timer_list = self.check_serial_set_cycle_timer()  # 定时设置
        launch_cycle_timer_on_list = self.check_serial_launch_cycle_timer_on()  # 定时执行开
        launch_cycle_timer_off_list = self.check_serial_launch_cycle_timer_off()  # 定时执行关

        # 设置
        set_cycle_timer = set_cycle_timer_list[0]
        set_cycle_timer_id = set_cycle_timer[1]
        set_cycle_timer_times = set_cycle_timer[2]
        result = [start_time_1 - 15 <= set_cycle_timer[0] <= start_time_1 + 15,
                  set_cycle_timer_times == "255"]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (set_cycle_timer, result))
        # 执行开→关
        launch_cycle_timer = launch_cycle_timer_off_list[0]
        launch_cycle_timer_id = launch_cycle_timer[1]
        launch_cycle_timer_times = launch_cycle_timer[2]
        result = [set_time_1 - 15 <= launch_cycle_timer[0] <= set_time_1 + 15,
                  launch_cycle_timer_id == set_cycle_timer_id,
                  launch_cycle_timer_times == set_cycle_timer_times]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (launch_cycle_timer, result))
        # 执行关→开
        launch_cycle_timer = launch_cycle_timer_on_list[0]
        launch_cycle_timer_id = launch_cycle_timer[1]
        launch_cycle_timer_times = launch_cycle_timer[2]
        result = [set_time_2 - 15 <= launch_cycle_timer[0] <= set_time_2 + 15,
                  launch_cycle_timer_id == set_cycle_timer_id,
                  launch_cycle_timer_times == set_cycle_timer_times]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (launch_cycle_timer, result))

        # 开关
        # 初始开关
        btn_state = btn_state_list[0]
        btn_all_layer = btn_state[1]
        result = [start_time_1 - 15 <= btn_state[0] <= start_time_1 + 15,
                  btn_all_layer == "100"]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (btn_state, result))
        # 开→关开关
        btn_state = btn_state_list[1]
        btn_all_layer = btn_state[1]
        result = [set_time_1 - 15 <= btn_state[0] <= set_time_1 + 15,
                  btn_all_layer == "000"]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (btn_state, result))
        # 关→开开关
        btn_state = btn_state_list[2]
        btn_all_layer = btn_state[1]
        result = [set_time_2 - 15 <= btn_state[0] <= set_time_2 + 15,
                  btn_all_layer == "100"]
        if False in result:
            raise TimeoutException("device state error, current: %s, result: %s" % (btn_state, result))