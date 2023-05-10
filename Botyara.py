# Библиотека для работы с вводом-выводом
from io import BytesIO

# Библиотека для работы с числами
import numpy as np

# Библиотека для отрисовки графика
import matplotlib.pyplot as plt

# Библиотека для работы бота
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# Библиотека, содержащая математические функции
import math

# Секретный ключ для уравления ботом
TOKEN = '5899998025:AAEhp2PVTvtrUdY63cIRBdjz_vvrotlZb7c'


# Функция отрисовки графика по заданной функции
async def plot_function(message: types.Message):
    try:
        """ Разбиваем сообщение на y= и все остальное, присваиваем fun_expr все, что после y=
        и удаляем лишние пробелы функцией strip() """
        fun_expr = message.text.split('=')[1].strip()
        """ Передаем fun_expr в функцию mathStr для преобразования ^ > ** и тд. 
        т.е к корректному с точки зрения питона синтаксису"""
        fun_expr = await mathStr(fun_expr)

        """ Проверяем если ли в нашем выражении функции, которые не вычисляются при x < 0 
        Если нет - создаем массив равномерно распределенных точек в кол-ве 1000 от -10 до 10 
        Если да - от 0 до 10"""
        if not "sqrt" in fun_expr:
            x_values = np.linspace(-10, 10, 1000)
        else:
            x_values = np.linspace(0, 10, 1000)
        """ Создаем список значений функции и вычисляем в каждой точке x 
        Вычисляет функция fun, туда мы передаем наше выражение и точку"""
        y_values = []
        for x in x_values:
            y_values.append(await fun(fun_expr, x))

        """ Получаем объекты графика и оси """
        fig, ax = plt.subplots()
        """ Рисуем график """
        ax.plot(x_values, y_values)
        """ Цвет и толщина осей """
        ax.axhline(0, color='black', lw=0.5)
        ax.axvline(0, color='black', lw=0.5)
        """ Название графика """
        ax.set_title(f'График функции {fun_expr}')
        """ Отображение y и x """
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        """ Включаем координатную сетку """
        ax.grid(True)

        """ Создаем буффер в памяти функцией  BytesIO(), далее помещаем туда
        наш график функции в формате png."""
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        """ Ставим указатель буфера на начало графика """
        buffer.seek(0)

        """ Отправляем график пользователю """
        await message.answer_photo(buffer)

        """ Закрываем объект графика, чтобы он не занимал память """
        plt.close(fig)
    except:
        """ В случае какой-либо ошибки отправляем сообщение о ней"""
        await message.answer('Invalid input. Please send a function in the form y=f(x).')
        return


""" Функция для вычисления значений функций в каждой точке графика """
async def fun(func_expr, x):
    variables = {"x": x, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan}
    return eval(func_expr, variables)


""" Функция замены в выражении для конкретного синтаксиса """
async def mathStr(func_expr):
    func_expr = func_expr.replace('^', '**')
    print(func_expr)
    return func_expr


""" Обработчик команды /start
    Отправляет пользователю сообщение. """
async def start_handler(message: types.Message):
    await message.answer("Hi! Send me a function to plot.")


""" Запуск бота """
if __name__ == '__main__':
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML) # Создаем объект бота
    dp = Dispatcher(bot)   # Создаем объект диспетчера для управления ботом
    dp.register_message_handler(start_handler, commands=['start']) # Добавляем обработку команды /start
    """ Добавляем обработку любого сообщения, которое будет передваться в plot_function"""
    dp.register_message_handler(plot_function, content_types=types.ContentTypes.TEXT)
    """ Запуска слушателя сообщений """
    executor.start_polling(dp, skip_updates=True)

""" Пока программа запущена бот работает. """