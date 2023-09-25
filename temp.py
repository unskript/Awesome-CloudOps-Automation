import threading

def f(x=None, y=None):
    print(x,y)

my_dict = {'x':1, 'y':{'z':2, 'a':1}}
t = threading.Thread(target=f, kwargs=my_dict)
t.start()
