import psycopg2
import pandas as pd
import random
from textblob import TextBlob

try:
	conn = psycopg2.connect(
	database = 'dictionary',
	user = 'postgres',
	host = 'localhost'
	)
except Exception as e:
	raise e

cur = conn.cursor()


def insert_into_table():
    eng_word = input("Enter English word: ")
    ukr_word = input("Enter Ukrainian word: ")
    table = "dict"
    cur.execute("INSERT INTO {}(english_word, ukrainian_word) VALUES('{}', '{}');".format(table, eng_word, ukr_word))
    conn.commit()
    return "Done!\nSuccessfully entered data in the table!"


def select_from_table():
    answer = []
    cur.execute('SELECT * FROM dict')
    rows = cur.fetchall()
    for row in rows:
        print(row)
        answer.append(row)
    return answer


def translate(word):
    lang_detect_word = TextBlob(word).detect_language()
    if lang_detect_word == 'uk' or lang_detect_word == 'ru':
        cur.execute(r"SELECT ukrainian_word,english_word FROM dict WHERE ukrainian_word = '{}';".format(word.lower()))
    else:
        cur.execute(r"SELECT english_word, ukrainian_word FROM dict WHERE english_word = '{}';".format(word.lower()))
    row = cur.fetchone()
    return row


def change_word():
    word_id = input('Enter id: ')
    cur.execute('select * from dict where id = {};'.format(word_id))
    print(cur.fetchone())
    eng_word = input("Enter English word: ")
    ukr_word = input("Enter Ukrainian word: ")
    cur.execute("UPDATE dict SET english_word = '{}', ukrainian_word = '{}' WHERE id = {};".format(eng_word.lower(), ukr_word.lower(), word_id))
    conn.commit()
    cur.execute('select * from dict where id = {};'.format(word_id))
    return cur.fetchone()
 

def task():
    number = int(input('Enter the number of words: '))
    cur.execute('SELECT * FROM dict')
    rows = cur.fetchall()
    words = []
    for row in rows:
        words.append(row[1])
        words.append(row[2])
    #print(words)
    for _ in range(number):
        question_word = random.choice(words)
        #print('question_word: ', question_word)
        #print(translate(question_word))
        answer_word = input('Translate word {}: '.format(question_word))
        translate_word = translate(question_word)
        if (answer_word==translate_word[0] or answer_word==translate_word[1]) and (question_word!=answer_word):
            print('RIGHT')
        else:
            print('WRONG')
            print(translate(question_word))


def show():
    print('\n')
    print('1. Select all from dictionary')
    print('2. Insert into dictionary')
    print('3. Translate')
    print('4. Change word')
    print('5. Task')
    print('6. Exit')
    print('\n')

if __name__=='__main__':
    action = None
    while action != 'exit':
        show()
        action = int(input('Enter action (number): '))
        if action == 1: 
            select_from_table()
        elif action == 2:
            print(insert_into_table())
        elif action == 3:
            word = input('Enter word: ')
            print(translate(word))
        elif action == 4:
            print(change_word())
        elif action == 5:
            task()
        elif action == 6:
            action = 'exit'



