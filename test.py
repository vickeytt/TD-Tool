import time
from func_timeout import func_set_timeout, FunctionTimedOut
@func_set_timeout(5)
def mytest2():
    print("Start")
    for i in range(1, 10):
        print("%d seconds have passed" % i)
        time.sleep(2)
if __name__ == '__main__':
    try:
        mytest2()
    except FunctionTimedOut as e:
        print('mytest2:::', e)