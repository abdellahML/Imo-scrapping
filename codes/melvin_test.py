"""
thread1 = RecoverUrlThread(url, 1, 11)
thread2 = RecoverUrlThread(url, 11, 21)
thread3 = RecoverUrlThread(url, 21, 31)
thread4 = RecoverUrlThread(url, 31, 41)
thread5 = RecoverUrlThread(url, 41, 51)

thread1.start()
#res1 = thread1.run()
thread2.start()
#res2 = thread2.run()
thread3.start()
#res3 = thread3.run()
thread4.start()
#res4 = thread4.run()
thread5.start()
#res5 = thread5.run()

thread5.join()

result = res1 + res2 + res3 + res4 + res5
print(result)
print(len(result))
"""