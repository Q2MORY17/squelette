"""
main.py is used for quick testing without GUI.
When ran, it is possible to interact with the entire system from CLI or shell
"""

from launcher import *
import threading

def main():

    lnchr = Launcher()

    # reset_thread = threading.Thread(name = 'reset_thread', target = lnchr.reset_encoders)
    # reset_thread.start()
    # reset_event = threading.Event()

    testThread = threading.Thread(name = 'testThread', target = lnchr.testBuf)
    testThread.start()
    testEvent = threading.Event()

    # wait_thread = threading.Thread(name = 'wait_thread', target = lnchr.case.bufferarithmetic)
    # wait_thread.start()

    # light_thread = threading.Thread(name = 'light_thread', target = lnchr.lights)
    # light_thread.start()

    # print(lnchr.launch.down())
    # print(lnchr.motors)
    # print(lnchr.case.up(), config.case_closed)
    # print(lnchr.case.down(), config.case_closed)
    # print(lnchr.case.stop())
    # print(lnchr.stop_all())
    # print(lnchr.pitch.position_absolute())
    # print(lnchr._launch.position_absolute())
    # print(lnchr.prepare())
##    while True:
##        user_choice = int(input("make your selection \n1 => PREPARE\n2 => LAUNCH\n3 => MOUNT\n4 => TEST\n5 => EXIT"))
##        if user_choice == 1:
##            print(lnchr.prepare())
##        elif user_choice == 2:
##            print(lnchr.launch())
##        elif user_choice == 3:
##            print(lnchr.mount())
##        elif user_choice == 4:
##            print(lnchr.testBuf())
##        elif user_choice == 5:
##            print("exiting now")
##            break

if __name__ == '__main__':
    main()
