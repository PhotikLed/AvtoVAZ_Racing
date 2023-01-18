from tkinter import *
from tkinter import messagebox as mb

from database_work import *
from main import *


def tuning_dialog(tun, car):
    price = get_tun_price(tun, car)
    size = get_size_upgrade(tun, car)
    Tk().wm_withdraw()  # Прячем главное окошко
    answer = mb.askyesno(
        title="Тюнинг",
        message=f"В действительно хотите улучшить параметр {tun} на {size} за {price}$?")
    if answer:
        if set_upgrade(tun, car):
            mb.showinfo(
                title="Ура",
                message=f"Параметр {tun} проапгрейджен!!!")
        else:
            mb.showinfo(title="Не ура",
                        message=f"Достигнуто максимальное число апгрейдов для параметра {tun}")
    return
