import matplotlib.pyplot as plt
import datetime
import sqlite3
from PIL import Image, ImageDraw, ImageFont

def statistic1(m):
    base = sqlite3.connect('all_in_one_base.db')
    base.execute('CREATE TABLE IF NOT EXISTS statistic_chislo_polsovateley (datee text PRIMARY KEY, amount integer)')
    base.commit()
    cur = base.cursor()
    len1 = cur.execute('SELECT id FROM user_id_base').fetchall()
    len1 = len(len1)
    #print(len1)
    data_today = datetime.datetime.now()
    data_today = data_today.strftime('%d.%m.%y')
    #print(data_today)
    try:
        cur.execute('INSERT INTO statistic_chislo_polsovateley VALUES (?, ?)', (data_today, len1))
        base.commit()
        print(f'Число пользователей за {data_today} успешно занесено')
    except:
        print(f'Число пользователей за {data_today} уже занесено')

    x = cur.execute('SELECT datee FROM statistic_chislo_polsovateley').fetchall()
    x = str(x)
    x = x.replace('[', '').replace(',', '').replace('(', '').replace(')', '').replace(']', '').replace("'", '').split(' ')
    abscissa = x
    #print(x)


    y = cur.execute('SELECT amount FROM statistic_chislo_polsovateley').fetchall()
    y = str(y)
    y = y.replace('[', '').replace(',', '').replace('(', '').replace(')', '').replace(']', '').split(' ')
    ordinata = []
    for i in y:
        i = int(i)
        ordinata.append(i)
    base.close()
    #print(ordinata)
    try:
        ax = plt.figure(figsize=(10, 8), dpi=80)
        plt.grid()
        plt.plot(abscissa, ordinata, linestyle='-.', marker='D', markerfacecolor='r', color=(0, 0, 0), alpha=0.4)
        foo = Image.open(f'fotochki/AvatarUser{m}.jpg')
        foo = foo.resize((100, 100))
        foo.save(f'fotochki/AvatarUser{m}.jpg', optimize=True, quality=195)
        im = plt.imread(f'fotochki/AvatarUser{m}.jpg')
        ax.figure.figimage(im, ax.bbox.xmax // 1 - im.shape[0] // 1, ax.bbox.ymax // 1 - im.shape[1] // 1,
                           alpha=0.8)
        plt.tick_params(axis='y', which='major', labelsize=16)
        plt.tick_params(axis='x', which='major', labelsize=12)
        plt.xticks(rotation=90)
        plt.ylabel("Число пользователей", fontsize=16)
        plt.fill_between(abscissa, ordinata, color='#00ffff')
        plt.savefig(f'fotochki/AmountUsers{m}.jpg')
        #plt.show()



        return 'ok'
    except:
        ax = plt.figure(figsize=(10, 8), dpi=80)
        plt.grid()
        plt.plot(abscissa, ordinata, linestyle='-.', marker='D', markerfacecolor='r', color=(0, 0, 0), alpha=0.4)
        foo = Image.open(f'fotochki/AvatarUser.jpg')
        foo = foo.resize((100, 100))
        foo.save(f'fotochki/AvatarUser.jpg', optimize=True, quality=195)
        im = plt.imread(f'fotochki/AvatarUser.jpg')
        ax.figure.figimage(im, ax.bbox.xmax // 1 - im.shape[0] // 1, ax.bbox.ymax // 1 - im.shape[1] // 1,
                           alpha=0.8)
        plt.tick_params(axis='y', which='major', labelsize=16)
        plt.tick_params(axis='x', which='major', labelsize=12)
        plt.xticks(rotation=90)
        plt.ylabel("Число пользователей", fontsize=16)
        plt.fill_between(abscissa, ordinata, color='#00ffff')
        plt.savefig('fotochki/AmountUsers.jpg')
        # plt.show()


#statistic1(1)
