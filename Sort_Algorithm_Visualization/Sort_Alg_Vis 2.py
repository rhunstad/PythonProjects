from tkinter import messagebox, Tk, Canvas, Frame, BOTH
from random import randint
from time import time, sleep
import timeit
from xlwt import Workbook
import xlsxwriter
import os
import numpy as np


def main():
    series = ([])
    entry = ""
    count = 1
    print("Enter the sort algorithms below to compare their computational time. \n")
    for i in range(2):
    while entry != 'x':
        entry = input("Algorithm #%s ('s' = selection sort, 'b' = bubble sort'): " % count)
        if entry == 'b':
            entry = 'bubble_sort'
            series += [entry]
        elif entry == 's':
            entry = 'selection_sort'
            series += [entry]
        count += 1

    start = int(input("Size of lists, start: "))
    end = int(input("Size of lists, end: "))
    cap = int(input("Max random value: "))

    x = np.arange(start, end, 1)
    y = ([])
    count = 0
    totitem = (len(series) * (end-start))

    percent = int(totitem/100)

    load_start = time()
    for i in range(len(series)):
        y_val = ([])
        for j in range(int(start), int(end), 1):
            seq = ([])
            for k in range(j):
                seq += [randint(0, cap)]
            begin = time()
            eval('Algo.%s(%s)' % (series[i], seq))
            finish = time()
            diff = (finish - begin) * 1000000
            y_val += [diff]
            count += 1
            if count % (percent*5) == 0:
                loaded = ((count * 100)/totitem)
                elapsed = time() - load_start
                remaining = round(abs(elapsed/loaded * (100-loaded)), 2)
                unit = 'seconds'
                if 60 < remaining < 120:
                    remaining = round(remaining/60, 0)
                    if remaining == 2:
                        unit = 'minutes'
                    else:
                        unit = 'minute'
                elif remaining >= 120:
                    remaining = round(remaining/60, 0)
                    unit = 'minutes'
                print('----%s%s complete (remaining: %s %s)----' % (loaded, '%', remaining, unit))
        y += [y_val]
    write_xl(x, y, series)


def write_xl(x, y, series):

    workbook = xlsxwriter.Workbook('algorithms.xlsx')
    ws = workbook.add_worksheet(name='Algo')
    chart1 = workbook.add_chart({'type': 'scatter', 'subtype': 'smooth'})
    x_data = "=Algo!$A$1:$A$%s" % len(x)
    ws.write_column('A1', x)

    for i in range(len(y)):
        ws.write_column(0, i+1, y[i])
        # y_data = "=Algo!$B$1:$B$%s" % len(y[i])
        y_data = ['Algo', 0, i+1, len(y[i]), i+1]
        chart1.add_series({
            "name": series[i],
            "categories": x_data,
            "values": y_data,
        })
    chart1.set_title({'name': 'Time complexity'})
    chart1.set_x_axis({'name': 'List size'})
    chart1.set_y_axis({'name': 'Clock time (%ss)' % u"\u03BC"})
    chart1.set_size({'x_scale': 2, 'y_scale': 2})
    chart1.set_style(3)
    ws.insert_chart(0, len(series)+5, chart1)
    workbook.close()


class Algo(object):
    @staticmethod
    def bubble_sort(seq):
        is_sorted = False
        while not is_sorted:
            is_sorted = True
            for i in range(len(seq) - 1, 0, -1):
                if seq[i] < seq[i - 1]:
                    n = seq[i - 1]
                    seq[i - 1] = seq[i]
                    seq[i] = n
                    is_sorted = False
        return seq

    @staticmethod
    def selection_sort(seq):
        for i in range(0, len(seq) - 1):
            m = i
            for j in range(i + 1, len(seq)):
                if seq[j] < seq[m]:
                    m = j
            n = seq[m]
            seq[m] = seq[i]
            seq[i] = n
        return seq

    @staticmethod
    def merge_sort(seq, s):
        # Takes sequence seq, divides it such that the smallest sub-unit that is being sorted is 2^s

        unit = 2**s
        sort_complete = 0
        # Same thing as below, keep increasing the size of the unit combining n units 1&2, 3&4, 5&6, etc...
        # Once you get to combine all the units up to n-1 and n, where len(n) != len(n-1), sort and combine.
        # If number of units is odd, sort the "heel" n, and merge it with the n-1/n-2 combined unit.
        # If even, sort the heel 'n' and merge it with n-1.

        while unit < len(seq)/2:
            while sort_complete < len(seq):
                if not sort_complete + unit >= len(seq):
                    heel = unit
                else:
                    heel = len(seq) % unit
                a = ([])
                for i in range(sort_complete, sort_complete+unit):
                    a += seq[i]
                b = ([])
                for i in range(sort_complete, sort_complete + unit + heel):
                    b += seq[i]
                a = Algo.selection_sort(a)
                b = Algo.selection_sort(b)
                c = Algo.merge(a, b)

                for i in range(sort_complete, sort_complete + unit + heel):
                    seq[i] = c[i]

            # do stuff to handle the heel
            # update unit
            # sort_complete = 0

    @staticmethod
    def merge(a, b):
        c = a, b
        return c

    @staticmethod
    def fib(n):
        # 1 / (9999999999999999999999998999999999999999999999999) gives the fibonacci sequence squished between 0's
        # That is 24 9's on either side of an 8
        fib = (0, 1)
        if n == 0:
            return None
        elif n == 1:
            return 0
        elif n == 2:
            return fib
        else:
            for i in range(2, n):
                n_sub_i = (fib[i-1] + fib[i-2])
                fib += (n_sub_i,)
        return fib


if __name__ == '__main__':
    """
    n = ""
    while n != -1:
        n = input("How many fibonacci numbers: ")
        fib_n = Algo.fib(n)
        print(fib_n)
    """
    main()
    import subprocess
    FileName = "algorithms.xlsx"
    subprocess.call(['open', FileName])

