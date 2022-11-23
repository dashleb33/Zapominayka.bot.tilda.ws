import matplotlib.pyplot as plt
import datetime
import sqlite3
from PIL import Image, ImageDraw, ImageFont

def statistic_vernih(id, answ):
    base = sqlite3.connect('all_in_one_base.db')
    cur = base.cursor()
    tema = cur.execute(f'SELECT theme FROM questions_base WHERE "{answ}" == right_answer').fetchall()

    tema = tema[0]
    tema = tema[0]
    #print(tema)


    print(id, answ)
    base = sqlite3.connect('all_in_one_base.db')
    base.execute(
        'CREATE TABLE IF NOT EXISTS statistic_chislo_vernih_otvetov (id text, verno integer, neverno integer, datee text, otvet text, tematika text)')
    base.commit()
    cur = base.cursor()
    y = datetime.datetime.now()
    y = y.strftime('%d.%m.%y')
    cur.execute('INSERT INTO statistic_chislo_vernih_otvetov VALUES (?, ?, ?, ?, ?, ?)', (id, 1, 0, y, answ, tema))
    base.commit()
    base.close()

def statistic_nevernih(id, answ):
    base = sqlite3.connect('all_in_one_base.db')
    cur = base.cursor()
    tema = cur.execute(f'SELECT theme FROM questions_base WHERE "{answ}" == right_answer').fetchall()

    tema = tema[0]
    tema = tema[0]
    # print(tema)

    print(id, answ)
    base = sqlite3.connect('all_in_one_base.db')
    base.execute('CREATE TABLE IF NOT EXISTS statistic_chislo_vernih_otvetov (id text, verno integer, neverno integer, datee text, otvet text, tematika text)')
    base.commit()
    cur = base.cursor()
    y = datetime.datetime.now()
    y = y.strftime('%d.%m.%y')
    cur.execute('INSERT INTO statistic_chislo_vernih_otvetov VALUES (?, ?, ?, ?, ?, ?)', (id, 0, 1, y, answ, tema))
    base.commit()
    base.close()

def grafiki(id):
    print(id)
    base = sqlite3.connect('all_in_one_base.db')
    cur = base.cursor()
    date = cur.execute(f'SELECT DISTINCT datee FROM statistic_chislo_vernih_otvetov WHERE "{id}" == id').fetchall()#Получили уникальные даты для каждого пользователя
    date = str(date)
    date = date.replace('[', '').replace(',', '').replace('(', '').replace(')', '').replace(']', '').replace("'", '').split(
        ' ')
    date_itog = date
    date_itog1 = date
    #print(date)

    ordinata_itog = []
    ordinata = []
    for i in date:
        date = cur.execute(f'SELECT verno FROM statistic_chislo_vernih_otvetov WHERE verno == 1 and datee == "{i}" and "{id}" == id').fetchall()#Получили верные ответы для каждого пользователя за все дни
        ordinata.append(date)
    for i in ordinata:
        i = str(i)
        i = i.replace('[', '').replace(',', '').replace('(', '').replace(')', '').replace(']', '').replace("'", '').split(
        ' ')
        el = len(i)
        #print(i)
        #print(el)
        ordinata_itog.append(el)
    #print(ordinata_itog)

    ordinata_itog_vse = []
    ordinata_vse = []
    for i in date_itog1:
        date = cur.execute(f'SELECT verno FROM statistic_chislo_vernih_otvetov WHERE (verno == 1 OR verno == 0) and datee == "{i}" and "{id}" == id').fetchall()  # Получили все ответы для каждого пользователя за все дни
        ordinata_vse.append(date)
    for i in ordinata_vse:
        i = str(i)
        i = i.replace('[', '').replace(',', '').replace('(', '').replace(')', '').replace(']', '').replace("'",'').split(' ')
        el = len(i)
        # print(i)
        # print(el)
        ordinata_itog_vse.append(el)
    #print(ordinata_itog_vse)
    base.close()




    try:
        ax = plt.figure(figsize=(10, 8), dpi=80)
        plt.grid()
        plt.plot(date_itog, ordinata_itog_vse, marker='D', markerfacecolor='r', color=(0, 0, 0), alpha=0.4)
        foo = Image.open(f'fotochki/AvatarUser{id}.jpg')
        foo = foo.resize((100, 100))
        foo.save(f'fotochki/AvatarUser{id}.jpg', optimize=True, quality=195)
        im = plt.imread(f'fotochki/AvatarUser{id}.jpg')
        ax.figure.figimage(im, ax.bbox.xmax // 1 - im.shape[0] // 1, ax.bbox.ymax // 1 - im.shape[1] // 1,
                           alpha=0.8)
        plt.tick_params(axis='y', which='major', labelsize=16)
        plt.tick_params(axis='x', which='major', labelsize=12)
        plt.xticks(rotation=90)
        plt.ylabel("Всего ответов/верных ответов", fontsize=16)
        plt.fill_between(date_itog, ordinata_itog, color='#00ffff')
        plt.savefig(f'fotochki/Result{id}.jpg')

        plt.show()
        return 'ok'
    except:
        ax = plt.figure(figsize=(10, 8), dpi=80)
        plt.grid()
        plt.plot(date_itog, ordinata_itog_vse, marker='D', markerfacecolor='r', color=(0, 0, 0), alpha=0.4)
        foo = Image.open(f'fotochki/AvatarUser.jpg')
        foo = foo.resize((100, 100))
        foo.save(f'fotochki/AvatarUser.jpg', optimize=True, quality=195)
        im = plt.imread(f'fotochki/AvatarUser.jpg')
        ax.figure.figimage(im, ax.bbox.xmax // 1 - im.shape[0] // 1, ax.bbox.ymax // 1 - im.shape[1] // 1,
                           alpha=0.8)
        plt.tick_params(axis='y', which='major', labelsize=16)
        plt.tick_params(axis='x', which='major', labelsize=12)
        plt.xticks(rotation=90)
        plt.ylabel("Всего ответов/верных ответов", fontsize=16)
        plt.fill_between(date_itog, ordinata_itog, color='#00ffff')
        plt.savefig(f'fotochki/Result.jpg')

        #plt.show()
        return 'ok'

# statistic1(1)
#grafiki(1366944590)

def razdel(id, t):
    print(t)
    m = ["страна-столица", "даты, история РФ", "правовые абревиатуры", "флаг-страна"]
    base = sqlite3.connect('all_in_one_base.db')
    cur = base.cursor()
    date = cur.execute(
        f'SELECT DISTINCT datee FROM statistic_chislo_vernih_otvetov WHERE "{id}" == id AND "{t}" == tematika').fetchall()  # Получили уникальные даты для каждого пользователя
    date = str(date)
    date = date.replace('[', '').replace(',', '').replace('(', '').replace(')', '').replace(']', '').replace("'",
                                                                                                             '').split(
        ' ')
    date_itog = date
    date_itog1 = date
    #print(date)

    ordinata_itog = []
    ordinata = []
    for i in date:
        date = cur.execute(
            f'SELECT verno FROM statistic_chislo_vernih_otvetov WHERE verno == 1 and datee == "{i}" and "{id}" == id and "{t}" = tematika').fetchall()  # Получили верные ответы для каждого пользователя за все дни
        ordinata.append(date)
    for i in ordinata:
        i = str(i)
        i = i.replace('[', '').replace(',', '').replace('(', '').replace(')', '').replace(']', '').replace("'",
                                                                                                           '').split(
            ' ')
        el = len(i)
        # print(i)
        # print(el)
        ordinata_itog.append(el)
    #print(ordinata_itog)

    ordinata_itog_vse = []
    ordinata_vse = []

    for i in date_itog1:
        date = cur.execute(
            f'SELECT verno FROM statistic_chislo_vernih_otvetov WHERE datee == "{i}" and "{id}" == id and "{t}" == tematika').fetchall()  # Получили все ответы для каждого пользователя за все дни
        ordinata_vse.append(date)

    #print(ordinata_vse)
    for i in ordinata_vse:
        i = str(i)
        i = i.replace('[', '').replace(',', '').replace('(', '').replace(')', '').replace(']', '').replace("'",
                                                                                                           '').split(
            ' ')
        el = len(i)
        # print(i)
        # print(el)
        ordinata_itog_vse.append(el)
    #print(ordinata_itog_vse)
    base.close()

    try:
        ax = plt.figure(figsize=(10, 8), dpi=80)
        plt.grid()
        plt.plot(date_itog, ordinata_itog_vse, marker='D', markerfacecolor='r', color=(0, 0, 0), alpha=0.4)
        foo = Image.open(f'fotochki/AvatarUser{id}.jpg')
        foo = foo.resize((100, 100))
        foo.save(f'fotochki/AvatarUser{id}.jpg', optimize=True, quality=195)
        im = plt.imread(f'fotochki/AvatarUser{id}.jpg')
        ax.figure.figimage(im, ax.bbox.xmax // 1 - im.shape[0] // 1, ax.bbox.ymax // 1 - im.shape[1] // 1,
                           alpha=0.8)
        plt.tick_params(axis='y', which='major', labelsize=16)
        plt.tick_params(axis='x', which='major', labelsize=12)
        plt.xticks(rotation=90)
        plt.ylabel(f"Всего ответов/верных ответов по теме {t}", fontsize=16)
        plt.fill_between(date_itog, ordinata_itog, color='#00ffff')
        plt.savefig(f'fotochki/ResultPoTeme.jpg')

        plt.show()
        return 'ok'
    except:
        ax = plt.figure(figsize=(10, 8), dpi=80)
        plt.grid()
        plt.plot(date_itog, ordinata_itog_vse, marker='D', markerfacecolor='r', color=(0, 0, 0), alpha=0.4)
        foo = Image.open(f'fotochki/AvatarUser.jpg')
        foo = foo.resize((100, 100))
        foo.save(f'fotochki/AvatarUser.jpg', optimize=True, quality=195)
        im = plt.imread(f'fotochki/AvatarUser.jpg')
        ax.figure.figimage(im, ax.bbox.xmax // 1 - im.shape[0] // 1, ax.bbox.ymax // 1 - im.shape[1] // 1,
                           alpha=0.8)
        plt.tick_params(axis='y', which='major', labelsize=16)
        plt.tick_params(axis='x', which='major', labelsize=12)
        plt.xticks(rotation=90)
        plt.ylabel(f"Всего ответов/верных ответов по теме {t}", fontsize=16)
        plt.fill_between(date_itog, ordinata_itog, color='#00ffff')
        plt.savefig(f'fotochki/ResultPoTeme.jpg')

        # plt.show()
        return 'ok'


#razdel(1366944590, "флаг-страна")