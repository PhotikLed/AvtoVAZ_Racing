from tkinter import *
from tkinter import messagebox as mb

from database_work import *


def tuning_dialog(tun):
    price = get_tun_price(tun)

    Tk().wm_withdraw()  # to hide the main window
    answer = mb.askyesno(
        title="Тюнинг",
        message=f"В действительно хотите улучшить параметр {tun} за {price}?")
    if answer:
        pass



