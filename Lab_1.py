import os, time
import colorlabels as cl
from multiprocessing import *


def download_bar(scanfiles, choisefile):
    with cl.progress(f'Поиск цели в [{scanfiles[choisefile]}]', mode=cl.PROGRESS_EXPAND):
        time.sleep(6000)


def download_data(data, scanfiles, choisefile, target):
    arr = []
    with open(scanfiles[choisefile], 'r') as file:
        for n, line in enumerate(file, 0):
            if target in line.lower():
                arr.append(line.strip('|').strip('\n').split('|'))
    data.send(arr)


if __name__ == '__main__':

    scanfiles = {}
    with os.scandir(os.getcwd()) as ListOfEntries:
        key = 0
        for entry in ListOfEntries:
            if entry.is_file() and 'txt' in entry.name:
                scanfiles.update({str(key): entry.name})
                key += 1

    print(f'\nОбнаружено {len(scanfiles)} файлов:\n~~~~~~~~~~~~~~~~~~~~~~~~')
    for key, value in scanfiles.items():
        print(f'{key}. {value}')
    print('~~~~~~~~~~~~~~~~~~~~~~~~\n')

    choisefile = cl.question('Выберите файл: ', color=('\033[' + str(36) + 'm'))

    print('\n')

    target = cl.question('Введите таргет: ', color=('\033[' + str(36) + 'm')).lower()

    data, pipe_data = Pipe()

    p1 = Process(target=download_data, args=(pipe_data, scanfiles, choisefile, target,))
    p2 = Process(target=download_bar, args=(scanfiles, choisefile,))

    p1.start()
    p2.start()

    p1.join()
    p2.terminate()
    
    cl.success('COMPLETE!\n', color=('\033[' + str(32) + 'm'))

    data = data.recv()

    if len(data) == 0:
        cl.info('Совпадений не обнаружено!', color=('\033[' + str(31) + 'm'))
    else:
        print('\033[36m            name              fname             phone            uid         nik          wo')
        for i in data:
            print('\033[32m [ ', end='')
            print(*i, sep='  .  ', end='')
            print('\033[32m ]')

    print('\n')
    cl.question('Нажмите ENTER для выхода', color=('\033[' + str(36) + 'm'))
