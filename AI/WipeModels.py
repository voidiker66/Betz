import os
from os import path

CURRENT_DIR = path.abspath(path.curdir)
NAME_WHEEL = ['Lain','Turing','Tesla','Silver']

for file in os.listdir(CURRENT_DIR + '/Models/Gamma/'):

    os.remove(CURRENT_DIR + '/Models/Gamma/' + file)


for name in NAME_WHEEL:

    os.remove(CURRENT_DIR + f'/Models/{name}/QNet Prime')

    for file in os.listdir(CURRENT_DIR + f'/Models/{name}/Versions/'):

        os.remove(CURRENT_DIR + f'/Models/{name}/Versions/' + file)


print('files deleted')