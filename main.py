import converter
from tkinter import *
import sys

from multiprocessing import Process


converter.intro()
converter.run()
root = Tk()

# root.bind("<space>", lambda event: root.destroy())

root.withdraw()  # скрыть окно
print('In the work...')
root.mainloop()  # Цикл сообщений
