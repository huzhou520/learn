# import sys, os
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)
# print(sys.path)
# print(BASE_DIR)
# from conf import settings
# import agent
from core import agent


class CommandHandler(object):

    def __init__(self, sys_argv):
        self.sys_argv = sys_argv
        print(sys_argv)
        if len(self.sys_argv) < 2:
            exit(self.help_msg())
        self.direction_excute()

    def direction_excute(self):
        """判断用户输入的指令，然后执行对应的程序"""

        input_direct = self.sys_argv[1]
        print(f"Received direction from command line=> {input_direct}")
        if hasattr(self, input_direct):
            func = getattr(self, input_direct)
            return func()
        else:
            print("A direction is not present. 请检查.")
            self.help_msg()

    def help_msg(self):
        """使用方法提示信息"""

        valid_commands = """
            start       启动Agent
            stop        停止Agent
        """
        exit(valid_commands)

    def start(self):
        """执行开启agent的相关步骤"""

        agent_handler_obj = agent.AgentHandler()
        agent_handler_obj.forever_run()

    def stop(self):
        """关闭agent"""
        pass


# print(settings.configs)


