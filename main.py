import converter
from tkinter import *
import sys
import Service.Service_convertor
import win32serviceutil
import win32service
import win32event
import servicemanager
from multiprocessing import Process



converter.run()
root = Tk()

# root.bind("<space>", lambda event: root.destroy())

root.withdraw()  # скрыть окно
print('In the work...')
root.mainloop()  # Цикл сообщений
