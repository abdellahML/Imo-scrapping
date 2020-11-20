from Ebubekir import ImportFromImmoweb, MyThread

if __name__ == "__main__":
    """Call every class in this main for a better code"""

    final_list = []

    """I'm using 10 thread to accelerate the process"""
    thread = MyThread(1, 18)
    thread_2 = MyThread(18, 35)
    thread_3 = MyThread(35, 52)
    thread_4 = MyThread(52, 69)
    thread_5 = MyThread(69, 86)
    thread_6 = MyThread(86, 103)
    thread_7 = MyThread(103, 120)
    thread_8 = MyThread(120, 137)
    thread_9 = MyThread(137, 154)
    thread_10 = MyThread(154, 168)

    thread.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()
    thread_5.start()
    thread_6.start()
    thread_7.start()
    thread_8.start()
    thread_9.start()
    thread_10.start()

    home_list = thread.run()
    home_list_2 = thread_2.run()
    home_list_3 = thread_3.run()
    home_list_4 = thread_4.run()
    home_list_5 = thread_5.run()
    home_list_6 = thread_6.run()
    home_list_7 = thread_7.run()
    home_list_8 = thread_8.run()
    home_list_9 = thread_9.run()
    home_list_10 = thread_10.run()

    """Add each list of property to the final_list"""
    final_list.extend(home_list)
    final_list.extend(home_list_2)
    final_list.extend(home_list_3)
    final_list.extend(home_list_4)
    final_list.extend(home_list_5)
    final_list.extend(home_list_6)
    final_list.extend(home_list_7)
    final_list.extend(home_list_8)
    final_list.extend(home_list_9)
    final_list.extend(home_list_10)