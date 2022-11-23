import time

import matplotlib.pyplot as plt
import datetime
import sqlite3
from PIL import Image, ImageDraw, ImageFont


def skolko_raz_zahodil_base(m):
    base = sqlite3.connect('all_in_one_base.db')
    base.execute('CREATE TABLE IF NOT EXISTS statistic_admin_vden (id TEXT, today1, today2)')
    base.commit()
    cur = base.cursor()
    data_today = datetime.datetime.now()
    data_today = data_today.strftime('%d.%m.%y')
    data_today_sek = time.time()
    #print(data_today_sek)
    #print(data_today)
    cur.execute('INSERT INTO statistic_admin_vden VALUES (?, ?, ?)', (m, data_today, data_today_sek))
    base.commit()
    base.close()


    #1668781030681.251   1668781034368.3623

def skolko_raz_zahodil(fir): #Число заходов в день для каждого пользователя
    if len(fir) == 8:
        print(fir)
        n = str(fir)
        base = sqlite3.connect('all_in_one_base.db')
        cur = base.cursor()
        vse_id = cur.execute(f'SELECT DISTINCT id FROM statistic_admin_vden WHERE today1 == "{n}"').fetchall()
        vse_id = str(vse_id)
        vse_id = vse_id.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '').split(' ')
        slovar = {}
        kolvo = {}
        for i in vse_id:
            vse_vremi = cur.execute(f'SELECT today2 FROM statistic_admin_vden WHERE (id == "{i}" and today1 == "{n}") ').fetchall()
            #print(vse_vremi)
            vse_vremi = str(vse_vremi)
            vse_vremi = vse_vremi.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', '').replace("'", '').split(' ')
            vse_vremi_float = []
            #print(vse_vremi)
            for j in vse_vremi:
                j1 = float(j)
                j1 = round(j1, 0)
                j1 = int(j1)
                vse_vremi_float.append(j1)
                #print(j1)
            b = 1
            for j1 in vse_vremi_float:
                if vse_vremi_float.index(j1) != 0 and j1 - vse_vremi_float[vse_vremi_float.index(j1) - 1] > 5:
                    b+=1
            kolvo[i] = b
        print(kolvo)

        return kolvo

    else:
        a_fir = fir.split(' ')[0]
        b_fir = fir.split(' ')[1]
        print(a_fir)
        print(b_fir)
        base = sqlite3.connect('all_in_one_base.db')
        cur = base.cursor()
        vse_id = cur.execute(f'SELECT DISTINCT id FROM statistic_admin_vden WHERE (today1 >= "{a_fir}" and today1 <= "{b_fir}")').fetchall()
        #print(vse_id)
        vse_id = str(vse_id)
        vse_id = vse_id.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', '').replace(
            "'", '').split(' ')
        #print(vse_id)
        slovar = {}
        kolvo = {}
        for i in vse_id:
            vse_vremi = cur.execute(
                f'SELECT today2 FROM statistic_admin_vden WHERE (id == "{i}" and (today1 >= "{a_fir}") and today1 <= "{b_fir}") ').fetchall()
            #print(vse_vremi)
            vse_vremi = str(vse_vremi)
            vse_vremi = vse_vremi.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',',
                                                                                                              '').replace(
                "'", '').split(' ')
            vse_vremi_float = []
            # print(vse_vremi)
            for j in vse_vremi:
                j1 = float(j)
                j1 = round(j1, 0)
                j1 = int(j1)
                vse_vremi_float.append(j1)
                # print(j1)
            b = 2
            for j1 in vse_vremi_float:
                if vse_vremi_float.index(j1) != 0 and j1 - vse_vremi_float[vse_vremi_float.index(j1) - 1] > 5:
                    b += 1
            kolvo[i] = b
        print(kolvo)

        return kolvo

#skolko_raz_zahodil('18.11.22 19.11.22')
