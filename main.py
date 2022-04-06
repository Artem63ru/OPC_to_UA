import converter
from tkinter import *
import sys
import Service


Service.init()
converter.run()

root = Tk()

# root.bind("<space>", lambda event: root.destroy())

root.withdraw()  # скрыть окно
print('In the work...')
root.mainloop()  # Цикл сообщений