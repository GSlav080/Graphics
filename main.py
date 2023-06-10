from logging import root
from math import *
from tkinter import *
import sympy as sy




def correct_coordinats(senter, coordinat, delta):
    x0, y0 = senter
    x, y = coordinat
    deltaX, deltaY = delta
    if (x < x0):
        x = -(x0 - x) / deltaX
    elif (x > x0):
        x = (x - x0) / deltaX
    else:
        x = 0
    if (y > y0):
        y = -(y0 - y) / deltaX
    elif (y < y0):
        y = (y - y0) / deltaX
    else:
        y = 0
    return [x, y]


def in_coordinats(senter, coordinat, delta):
    x, y = coordinat
    deltaX, deltaY = delta
    if (x < 0):
        x = senter[0] + x * deltaX
    elif (x >= 0):
        x = senter[0] + x * deltaX
    if (y >= 0):
        y = (senter[1] - y * deltaX)
    elif (y < 0):
        y = (senter[1] - y * deltaX)
    return [x, y]


def Senter(x0=(root.winfo_screenwidth() - 100), y0=(root.winfo_screenheight() - 100), N=5, graphs=False):
    canv = Canvas(root, width=x0, height=y0, bg="white")
    canv.create_line(0, y0 / 2, x0, y0 / 2, width=2, arrow=LAST, fill='black')
    canv.create_line(x0 / 2, y0, x0 / 2, 0, width=2, arrow=LAST, fill='black')
    canv.create_text(x0 / 2 + 8, y0 / 2 + 6, text=str(0), fill="blue", font=("Helvectica", "15"))

    x0, y0 = x0 / 2, y0 / 2
    w = (root.winfo_screenwidth() - 100) / 2
    h = (root.winfo_screenheight() - 100) / 2
    w0 = w // (N * 2 + 1)
    if (graphs):
        h0 = h // (N * 2 + 1)
    else:
        h0 = w // (N * 2 + 1)
    mini_alpha = w0 / 5
    for i in range(0, N + 1):
        for j in range(1, 6):
            canv.create_line(x0 + w0 * i + mini_alpha * j, -3 + y0, x0 + w0 * i + mini_alpha * j, 3 + y0, width=0.1,
                             fill='black')
            canv.create_line(x0 - w0 * i - mini_alpha * j, -3 + y0, x0 - w0 * i - mini_alpha * j, 3 + y0, width=0.1,
                             fill='black')
            canv.create_line(-3 + x0, y0 + h0 * i + mini_alpha * j, 3 + x0, y0 + h0 * i + mini_alpha * j, width=0.1,
                             fill='black')
            canv.create_line(-3 + x0, y0 - h0 * i - mini_alpha * j, 3 + x0, y0 - h0 * i - mini_alpha * j, width=0.1,
                             fill='black')
        if (i != 0):
            canv.create_line(x0 + w0 * i, -3 + y0, x0 + w0 * i, 3 + y0, width=2, fill='black')
            canv.create_text(x0 + w0 * i, -13 + y0, text=str(i), fill="blue", font=("Helvectica", "10"))

            canv.create_line(x0 - w0 * i, -3 + y0, x0 - w0 * i, 3 + y0, width=2, fill='black')
            canv.create_text(x0 - w0 * i, -13 + y0, text=str(-i), fill="blue", font=("Helvectica", "10"))

            canv.create_line(-3 + x0, y0 + h0 * i, 3 + x0, y0 + h0 * i, width=0.5, fill='black')
            canv.create_text(13 + x0, y0 + h0 * i, text=str(-i), fill="blue", font=("Helvectica", "10"))

            canv.create_line(-3 + x0, y0 - h0 * i, 3 + x0, y0 - h0 * i, width=0.5, fill='black')
            canv.create_text(13 + x0, y0 - h0 * i, text=str(i), fill="blue", font=("Helvectica", "10"))

    delta_x = w0
    delta_y = h0
    mn = [[x0 - w0 * N, y0], [x0 + w0 * N, y0]]
    return [x0, y0], canv, [delta_x, delta_y], mn


def f1(x):
    return x ** 3 - 8 * x + 1


def f2(x):
    return -12 * sin(x) - 10 * cos(x)


def graph(center, func, otr, delta, canv, alpha=0.01, color="black"):
    start_x = correct_coordinats(center, otr[0], delta)[0]
    end_x = correct_coordinats(center, otr[1], delta)[0]
    Flag = True
    while (start_x < end_x):
        if (Flag):
            try:
                x1, y1 = in_coordinats(center, [start_x, func(start_x)], delta)
                Flag = False
            except:
                pass
        try:
            x0, y0 = x1, y1
            x1, y1 = in_coordinats(center, [start_x + alpha, func(start_x + alpha)], delta)
            canv.create_line(x0, y0, x1, y1, width=2, fill=color)
        except:
            pass
        start_x += alpha
    return canv


def yravn(f1, f2, center, otr, delta, canv, alpha=0.001):
    start_x = correct_coordinats(center, otr[0], delta)[0]
    end_x = correct_coordinats(center, otr[1], delta)[0]
    x1, x2, y1, y2 = 0, 0, 0, 0
    otvets = set()
    while (start_x < end_x):
        try:
            y1 = f1(start_x)
        except:
            pass
        try:
            y2 = f2(start_x)
        except:
            pass
        try:
            y1 = round(y1, 3)
            y2 = round(y2, 3)
        except:
            pass
        if (abs(y1 - y2) <= 0.0065):
            otvets.add(start_x)
            x, y = in_coordinats(center, [start_x, y1], delta)
            canv.create_line(x - 3, y, x + 3, y, width=5, fill='red')
        start_x = round(start_x + alpha, 3)

    return canv, sorted(otvets)


def shtrih(f1, f2, center, delta, canv, otvets, color="grey", alpha=0.1):
    if (len(otvets) == 0):
        return 0
    start_x = otvets[0]
    end_x = otvets[-1]
    x1, x2, y1, y2 = 0, 0, 0, 0
    S = 0

    while (start_x < end_x):
        try:
            y1 = f1(start_x)
            S += f1(start_x + alpha / 2)

        except:
            pass
        try:
            y2 = f2(start_x)
            S -= f2(start_x + alpha / 2)

            x, y1 = in_coordinats(center, [start_x, y1], delta)
            x, y2 = in_coordinats(center, [start_x, y2], delta)
            canv.create_line(x, y1, x, y2, width=1, fill=color)
        except:
            pass
        start_x = start_x + alpha
    S *= alpha
    return S


def draw_point(canvas, coor, center, delta, radius=0.1, color='green'):
    x, y = coor
    canvas.create_oval(in_coordinats(center, [x - radius, y - radius], delta),
                       in_coordinats(center, [x + radius, y + radius], delta), fill=color)


def draw_line(canvas, point1, point2, center, delta, color='black', width=1):
    x1, y1 = in_coordinats(center, point1, delta)
    x2, y2 = in_coordinats(center, point2, delta)
    canvas.create_line(x1, y1, x2, y2, fill=color, width=width)


import math


def steiner_point_thre(p1, p2, p3):

    m1 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    m2 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
    m3 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
    x = (p1[0] + p2[0] + p3[0] + m1[0] + m2[0] + m3[0]) / 6
    y = (p1[1] + p2[1] + p3[1] + m1[1] + m2[1] + m3[1]) / 6
    print(x, y)
    return (x, y)

def steiner_point_four(A, B, C, D):
    global steiner_point
    min_sum_length = math.inf
    optimal_steiner_point = None

    # Перебор всех возможных троек точек
    for triplet in [(A, B, C), (A, B, D), (A, C, D), (B, C, D)]:
        # Нахождение точки Штейнера для текущей тройки
        steiner_point = steiner_point_thre(*triplet)
        print(triplet)

        # Вычисление суммарной длины отрезков
        sum_length = math.dist(A, steiner_point) + math.dist(B, steiner_point) + math.dist(C, steiner_point) + math.dist(D, steiner_point)

        # Обновление оптимального результата, если текущая суммарная длина меньше
        if sum_length < min_sum_length:
            min_sum_length = sum_length
            optimal_steiner_point = steiner_point

    return optimal_steiner_point


