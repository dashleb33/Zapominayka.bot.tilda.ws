import sqlite3
import random as r


async def db_start():
    global conn, cursor
    conn = sqlite3.connect('all_in_one_base.db', check_same_thread=False)
    cursor = conn.cursor()


async def save_user_in_base(user_id: int, user_name: str, user_surname: str, username: str):
        user = cursor.execute(f"SELECT * FROM user_id_base WHERE user_id = '{user_id}'").fetchone()
        if not user:
            cursor.execute('INSERT INTO user_id_base (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                           (user_id, user_name, user_surname, username))
            conn.commit()
        else:
            print('user in base')


async def select_all_themes_from_base():
    all_themes = cursor.execute('SELECT DISTINCT theme FROM questions_base').fetchall()
    all_themes = [i[0] for i in all_themes]
    print(all_themes)
    return all_themes


async def select_questions_for_theme(chosen_theme):
    cursor.execute(f"SELECT question_id, question, right_answer, link FROM questions_base WHERE theme = '{chosen_theme}'")
    dict_ques_answ = cursor.fetchall()
    r.shuffle(dict_ques_answ)
    return dict_ques_answ


async def show_my_rule(us_id, question_id):
    user_rule_from_base = cursor.execute(f"SELECT mnemonic_rule FROM user_rules_2 WHERE user_id = "
                                         f"'{us_id}' AND question_id = '{question_id}'").fetchone()
    if not user_rule_from_base:
        return False
    user_rule_from_base = str(*user_rule_from_base)
    return user_rule_from_base


async def select_everything_for_rule(question):
    cursor.execute(f"SELECT question_id, question, right_answer FROM questions_base WHERE question = '{question}'")
    row_with_question_from_base = cursor.fetchone()
    return row_with_question_from_base


async def show_all_my_rules(chosen_theme, us_id):
    all_rules = cursor.execute(f"SELECT question, right_answer, mnemonic_rule "
                               f"FROM questions_base INNER JOIN user_rules_2 "
                               f"ON questions_base.question_id = user_rules_2.question_id "
                               f"WHERE mnemonic_rule IS NOT NULL "
                               f"AND theme = '{chosen_theme}'"
                               f"AND user_id = '{us_id}'").fetchall()
    return all_rules


async def update_my_rule(pravilo, us_id, question_id):
    cursor.execute(f"UPDATE user_rules_2 SET mnemonic_rule == ? WHERE user_id  == ? AND question_id  == ? ",
                   (pravilo, us_id, question_id))
    conn.commit()


async def create_my_rule(us_id, question_id, pravilo):
    cursor.execute('INSERT INTO user_rules_2 (user_id, question_id, mnemonic_rule) VALUES (?, ?, ?)',
                   (us_id, question_id, pravilo))
    conn.commit()

async def is_there_question_in_base(quest_to_create_rule, chosen_theme):
    cursor.execute(f"SELECT question_id "
                   f"FROM questions_base "
                   f"WHERE question = '{quest_to_create_rule}' "
                   f"AND theme = '{chosen_theme}' ")
    is_there_this_question = cursor.fetchone()
    return is_there_this_question


async def take_question_formulate(chosen_theme):
    cursor.execute(f"SELECT question_for_theme "
                   f"FROM theme_question "
                   f"WHERE theme = '{chosen_theme}'")
    take_question_itog = str(*cursor.fetchone())
    return take_question_itog


