import PySimpleGUI as sg # библиотека интефейса
from numpy import *
import matplotlib.pyplot as plt
import numexpr as ne # Переобразует текст в формулу
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # для перевода графика в формат canvas
import matplotlib # для построения графиков
matplotlib.use('TkAgg')
figure_agg = None # флаг


def draw_area(x, y, F): # для построения плоскости
    Z = ne.evaluate(F) # переводит текст в формулу
    fig = matplotlib.figure.Figure(figsize=(10, 6), dpi=100) # размер графика
    ax = fig.add_subplot(111, projection='3d') # создает 3д график
    ax.plot_surface(x, y, Z, cmap='inferno') # строит график по заданным данным
    ax.legend() # подписи осей
    return fig


def Try_num(tried): # для использования pi и exp
    tried1 = tried.replace('e', str(exp(1)))
    tried1 = tried.replace('pi', str(pi))
    return ne.evaluate(tried1)


def delete_figure_agg(figure_agg): # очистка графика
    figure_agg.get_tk_widget().forget()
    plt.close('all')


def draw_figure(canvas, figure): # отрисовывает график в программе
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


layout_curve = [ # интерфейс кривой
    [sg.Text('Z(t)'),
     sg.InputText(key='-z-', size=(50, 1), default_text='t')],
    [sg.Text('Y(t)'),
     sg.InputText(key='-y-', size=(50, 1), default_text='cos(t)')],
    [sg.Text('X(t)'),
     sg.InputText(key='-x-', size=(50, 1), default_text='sin(t)')],
    [sg.Text('Определите диапозон t')],
    [sg.Text('t(нач):'), sg.InputText(key='-t0-', size=(15, 1), default_text='-2*pi'),
     sg.Text('t(кон):'), sg.InputText(key='-t1-', size=(15, 1), default_text='2*pi')],
    [sg.Button('Вывод кривой')]]


layout_area_param = [ # интерфейс кривой
    [sg.Text('Z(u,v)'),
     sg.InputText(key='-z(uv)-', size=(50, 1), default_text='cos(u)*sin(v)')],
    [sg.Text('Y(u,v)'),
     sg.InputText(key='-y(uv)-', size=(50, 1), default_text='cos(v)*sin(u)')],
    [sg.Text('X(u,v)'),
     sg.InputText(key='-x(uv)-', size=(50, 1), default_text='cos(v)')],
    [sg.Text('Определите диапозон t')],
    [sg.Text('u(нач):'), sg.InputText(key='-u0-', size=(15, 1), default_text='0'),
     sg.Text('u(кон):'), sg.InputText(key='-u1-', size=(15, 1), default_text='2*pi')],
    [sg.Text('v(нач):'), sg.InputText(key='-v0-', size=(15, 1), default_text='0'),
     sg.Text('v(кон):'), sg.InputText(key='-v1-', size=(15, 1), default_text='2*pi')],
    [sg.Button('Вывод  поверхности')]]


layout_area = [ # интерфейс плоскости
    [sg.Text('F(x,y)='),
     sg.InputText(key='-F-', size=(50, 1), default_text='x**2+y**2')],
    [sg.Text('Область последовательности')],
    [sg.Text('По оси x:')],
    [sg.Text('X(нач):'), sg.InputText(key='-x0-', size=(15, 1), default_text='-10'),
     sg.Text('X(кон):'), sg.InputText(key='-x1-', size=(15, 1), default_text='10')],
    [sg.Text('По оси y:')],
    [sg.Text('Y(нач):'), sg.InputText(key='-y0-', size=(15, 1), default_text='-10'),
     sg.Text('Y(кон):'), sg.InputText(key='-y1-', size=(15, 1), default_text='10')],
    [sg.Button('Вывод поверхности')]]





layout = [
    [sg.TabGroup([[sg.Tab('Уравнение поверхности', layout_area)],
                  [sg.Tab('Уравнение параметрической поверхности', layout_area_param)],
                  [sg.Tab('Уравнение кривой', layout_curve)]]),
     sg.Button('Выход')],
    [sg.Canvas(key="-CANVAS-")]]


window = sg.Window('Построение 3D-графиков', layout, element_justification='center', font='Helvetica 10',
                   location=(100, 0))
while True:
    event, values = window.read() # считывает события и значения в форме
    window.refresh() # обновляет изменения в программе
    if event in 'Вывод поверхности': # проверка на событие по нажатии на кнопку вывод поверхности
        F, x0, x1 = values['-F-'], float(Try_num(values['-x0-'])), float(Try_num(values['-x1-']))
        y0, y1 = float(Try_num(values['-y0-'])), float(Try_num(values['-y1-']))
        X, Y = mgrid[x0:x1:0.1, y0:y1:0.1]
        F = F.replace('X', 'x')
        F = F.replace('Y', 'y')
        fig = draw_area(X, Y, F)
        if figure_agg:
            delete_figure_agg(figure_agg)
        figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    if event in 'Вывод  поверхности':
        u0, u1, v0, v1 = float(Try_num(values['-u0-'])), float(Try_num(values['-u1-'])), float(Try_num(values['-v0-'])),\
                         float(Try_num(values['-v1-']))
        u, v = mgrid[u0:u1:0.1, v0:v1:0.1]
        X = ne.evaluate(values['-x(uv)-'] + '+u-u+v-v')
        Y = ne.evaluate(values['-y(uv)-'] + '+u-u+v-v')
        Z = ne.evaluate(values['-z(uv)-'] + '+u-u+v-v')
        fig = matplotlib.figure.Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_wireframe(X, Y, Z)
        if figure_agg:
            delete_figure_agg(figure_agg)
        figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    if event in 'Вывод кривой':
        t0, t1 = float(Try_num(values['-t0-'])), float(Try_num(values['-t1-']))
        t = arange(t0, t1, 0.1)
        X = ne.evaluate(values['-x-']+'+t-t')
        Y = ne.evaluate(values['-y-']+'+t-t')
        Z = ne.evaluate(values['-z-']+'+t-t')
        fig = matplotlib.figure.Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(X, Y, Z)
        if figure_agg:
            delete_figure_agg(figure_agg)
        figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    if event in (None, 'Exit', 'Выход'):
        break