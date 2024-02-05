import telebot
from os import listdir
from shutil import rmtree
from pathlib import Path


class User:

    def __init__(self, usid):
        self.usid = usid
        self.menu_pos = self.main
        self.reg_data = ['', '']
        self.task_way = [0, 0, 0]
        self.task_folder = ['', '']
        self.subject = ''
        self.file_counter = 0
        self.nt_load_folder = ''

    # функциональные методы

    def text_check(self, text):
        if '|' in text:
            bot.send_message(self.mes.chat.id, 'Недопустимый символ - "|"')
            return False
        elif '\n' in text:
            bot.send_message(self.mes.chat.id, 'Недопустимый символ - перенос строки')
            return False
        return True


    def text_check2(self, text):
        if '|' in text:
            bot.send_message(self.mes.chat.id, 'Недопустимый символ - "|"')
            return False
        return True


    def show_subs(self):
        ret = ''
        subs_list = listdir('tasks')
        for i in range(len(subs_list)):
            ret += f'\n{i + 1}.{subs_list[i]}'
        return ret


    def show_tasks(self):
        ret = ''
        subs_list = listdir(f'tasks/{listdir("tasks")[self.task_way[0] - 1]}')
        for i in range(len(subs_list)):
            ret += f'\n{i + 1}.{subs_list[i]}'
        return ret

    # основные методы

    def log(self):
        if self.text_check(self.mes.text):
            with open('accs.txt', mode='r', encoding="utf-8") as accs:
                for i in accs.read()[:-1].split('\n'):
                    if i.split('|')[1] == self.mes.text:
                        bot.send_message(self.mes.chat.id, 'Введите пароль')
                        self.reg_data[0] = self.mes.text
                        self.menu_pos = self.log_pass
                        break
                else:
                    bot.send_message(self.mes.chat.id, 'Аккаунт не найден')


    def log_pass(self):
        if self.text_check(self.mes.text):
            with open('accs.txt', mode='r', encoding="utf-8") as accs:
                for i in accs.read()[:-1].split('\n'):
                    line = i.split('|')
                    if line[2] == self.mes.text:
                        bot.send_message(self.mes.chat.id, 'Вход воспроизведен')
                        self.reg_data[1] = self.mes.text
                        if line[0] == 'p':
                            self.menu_pos = self.in_menu
                            self.subject = ''
                            bot.send_message(self.mes.chat.id, '''Выберите пункт:
    
1.Предметы
2.Выход из аккаунта
3.Удаление аккаунта''')
                        else:
                            self.menu_pos = self.t_in_menu
                            self.subject = line[3]
                            self.task_folder[0] = line[3]
                            bot.send_message(self.mes.chat.id, '''Выберите пункт:

1.Добавить работу
2.Удалить работу
3.Результаты учеников
4.Выход из аккаунта''')
                        break
                else:
                    bot.send_message(self.mes.chat.id, 'Пароль неверный')


    def reg(self):
        if self.text_check(self.mes.text):
            with open('accs.txt', mode='r', encoding="utf-8") as accs:
                for i in accs.read()[:-1].split('\n'):
                    if i.split('|')[1] == self.mes.text:
                        bot.send_message(self.mes.chat.id, 'Этот логин уже существует')
                        break
                else:
                    self.reg_data[0] = self.mes.text
                    self.menu_pos = self.reg_pass
                    bot.send_message(self.mes.chat.id, 'Введите пароль')


    def reg_pass(self):
        if self.text_check(self.mes.text):
            self.reg_data[1] = self.mes.text
            with open('accs.txt', mode='r', encoding="utf-8") as accs:
                for i in accs.read()[:-1].split('\n'):
                    if i.split('|')[2] == self.mes.text:
                        bot.send_message(self.mes.chat.id, 'Пароль занят')
                        break
                else:
                    with open('accs.txt', mode='a', encoding="utf-8") as accs:
                        accs.write('p')
                        for i in self.reg_data:
                            accs.write('|' + i)
                        accs.write('\n')
                    self.menu_pos = self.in_menu
                    bot.send_message(self.mes.chat.id, 'Успешная регистрация')
                    bot.send_message(self.mes.chat.id, '''Выберите пункт:

1.Предметы
2.Выход из аккаунта
3.Удаление аккаунта''')


    def acc_del(self):
        with open('accs.txt', 'r', encoding='utf-8') as file:
            wrt = file.read()[:-1]
        with open('accs.txt', 'w', encoding='utf-8') as file:
            lst = wrt.split('\n')
            for a in lst:
                if a.split('|')[1] == self.reg_data[0]:
                    lst.remove(a)
                    wrt = ''
                    for b in lst:
                        ln = b.split('|')
                        wrt += ln[0] + '|' + ln[1] + '|' + ln[2] + '\n'
                    break
            file.write(wrt)
        for sub in listdir('tasks'):
            for task in listdir(f'tasks/{sub}'):
                for point in listdir(f'tasks/{sub}/{task}/res'):
                    with open(f'tasks/{sub}/{task}/res/{point}', 'r', encoding='utf-8') as file:
                        wrt = file.read()[:-1]
                    with open(f'tasks/{sub}/{task}/res/{point}', 'w', encoding='utf-8') as file:
                        lst = wrt.split('\n')
                        for a in lst:
                            if a.split('|')[0] == self.reg_data[0]:
                                lst.remove(a)
                                print(lst)
                                wrt = ''
                                for b in lst:
                                    ln = b.split('|')
                                    wrt += ln[0] + '|' + ln[1] + '\n'
                                    file.write(wrt)
                                break
        self.menu_pos = self.main
        bot.send_message(self.mes.chat.id, 'Аккаунт успешно удален')
        bot.send_message(self.mes.chat.id, '''Выберите пункт:

1.Вход
2.Регистрация учащегося''')


    def in_menu(self):
        if self.mes.text == 'Нзд':
            bot.send_message(self.mes.chat.id, '''Выберите пункт:

1.Предметы
2.Выход из аккаунта
3.Удаление аккаунта''')

        elif self.mes.text == '1':
            self.menu_pos = self.subs
            bot.send_message(self.mes.chat.id, 'Выберите предмет:\n' + self.show_subs())

        elif self.mes.text == '2':
            self.menu_pos = self.main
            bot.send_message(self.mes.chat.id, '''Выберите пункт:

1.Вход
2.Регистрация учащегося''')

        elif self.mes.text == '3':
            self.acc_del()


    def subs(self):
        if self.mes.text == 'Нзд':
            bot.send_message(self.mes.chat.id, 'Выберите предмет:\n' + self.show_subs())
        else:
            self.task_way[0] = int(self.mes.text)
            bot.send_message(self.mes.chat.id, 'Выберите работу:\n' + self.show_tasks())
            self.menu_pos = self.tasks


    def tasks(self):
        if self.mes.text == 'Нзд':
            bot.send_message(self.mes.chat.id, 'Выберите работу:\n' + self.show_tasks())
        else:
            self.task_way[1] = int(self.mes.text)
            if self.task_folder[0] == '':
                self.task_folder[0] = listdir('tasks')[self.task_way[0] - 1]
            self.task_folder[1] = listdir(f'tasks/{self.task_folder[0]}')[self.task_way[1] - 1]
            if self.subject == '':
                self.menu_pos = self.task
                self.task()
            else:
                self.menu_pos = self.res_show
                try:
                    self.res_show()
                except IndexError:
                    bot.send_message(self.mes.chat.id, 'Работу пока никто не выполнил')


    def task(self):
        ln = len(listdir(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/ans'))

        if self.mes.text == 'Нзд':
            n = ''
            for i in range(ln):
                n += '\n' + str(i + 1) + '.'
            bot.send_message(self.mes.chat.id, 'Выберите пункт, на который собираетесь дать ответ:\n' + n)
            self.menu_pos = self.point

        else:
            for filename in listdir(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/mat'):
                if filename.split('.')[-1] != 'txt':
                    with open(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/mat/{filename}', 'rb') as send_file:
                        bot.send_photo(self.mes.chat.id, send_file.read())
            for filename in listdir(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/mat'):
                if filename.split('.')[-1] == 'txt':
                    with open(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/mat/{filename}', 'r', encoding='utf-8') as send_file:
                        bot.send_message(self.mes.chat.id, send_file.read())

            if ln == 1:
                with open(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/res/1.txt', 'r', encoding='utf-8') as res_file:
                    for i in res_file.read()[:-1].split('\n'):
                        line = i.split('|')
                        if line[0] == self.reg_data[0]:
                            if line[1] == '1':
                                bot.send_message(self.mes.chat.id, 'Задание было выполнено верно')
                            else:
                                bot.send_message(self.mes.chat.id, 'Задание было выполнено неверно')
                            break
                    else:
                        self.menu_pos = self.ans
                        self.task_way[2] = '1'
                        bot.send_message(self.mes.chat.id, 'Введите ответ')

            else:
                n = ''
                for i in range(ln):
                    n += '\n' + str(i + 1) + '.'
                bot.send_message(self.mes.chat.id, 'Выберите пункт, на который собираетесь дать ответ:\n' + n)
                self.menu_pos = self.point


    def point(self):
        ln = len(listdir(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/ans'))
        if self.mes.text == 'Нзд':
            if ln > 1:
                n = ''
                for i in range(ln):
                    n += '\n' + str(i + 1) + '.'
                bot.send_message(self.mes.chat.id, 'Выберите пункт, на который собираетесь дать ответ:\n' + n)
            else:
                self.tasks()

        else:
            with open(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/res/{self.mes.text}.txt', 'r', encoding='utf-8') as res_file:
                for i in res_file.read()[:-1].split('\n'):
                    line = i.split('|')
                    if line[0] == self.reg_data[0]:
                        if line[1] == '1':
                            bot.send_message(self.mes.chat.id, 'Задание было выполнено верно')
                        else:
                            bot.send_message(self.mes.chat.id, 'Задание было выполнено неверно')
                        break
                else:
                    self.task_way[2] = int(self.mes.text)
                    bot.send_message(self.mes.chat.id, 'Введите ответ')
                self.menu_pos = self.ans


    def ans(self):
        with open(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/ans/{self.task_way[2]}.txt', 'r', encoding='utf-8') as ans_file:
            answer = ans_file.read().split('|')
            with open(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/res/{self.task_way[2]}.txt', 'a', encoding='utf-8') as res_file:
                if self.mes.text == answer[0]:
                    bot.send_message(self.mes.chat.id, 'Ответ верный')
                    res_file.write(self.reg_data[0] + '|' + '1' + '\n')
                else:
                    bot.send_message(self.mes.chat.id, 'Ответ неверный')
                    bot.send_message(self.mes.chat.id, answer[1])
                    res_file.write(self.reg_data[0] + '|' + '0' + '\n')

    # функции специально для учителей

    def t_in_menu(self):
        if self.mes.text == 'Нзд':
            bot.send_message(self.mes.chat.id, '''Выберите пункт:

1.Добавить работу
2.Удалить работу
3.Результаты учеников
4.Выход из аккаунта''')

            if self.nt_load_folder != '':
                rmtree(f"tasks/{self.subject}/{self.nt_load_folder}")
                self.nt_load_folder = ''

        elif self.mes.text == '1':
            bot.send_message(self.mes.chat.id, 'Введите название работы')
            self.menu_pos = self.nt_name

        elif self.mes.text == '2':
            bot.send_message(self.mes.chat.id, 'Выберите работу:\n' + self.show_tasks())
            self.menu_pos = self.task_del

        elif self.mes.text == '3':
            bot.send_message(self.mes.chat.id, 'Выберите работу:\n' + self.show_tasks())
            self.menu_pos = self.tasks

        elif self.mes.text == '4':
            self.menu_pos = self.main
            bot.send_message(self.mes.chat.id, '''Выберите пункт:

1.Вход
2.Регистрация учащегося''')


    def res_show(self):
        out = ''
        dr = listdir(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/res')
        ln = len(dr)
        pups = {}
        for point in dr:
            with open(f'tasks/{self.task_folder[0]}/{self.task_folder[1]}/res/{point}', 'r', encoding='utf-8') as file:
                data = file.read()[:-1]
                for i in data.split('\n'):
                    line = i.split('|')
                    if ln == 1:
                        out += line[0]
                        if line[1] == '1':
                            out += ' - верно\n'
                        else:
                            out += ' - неверно\n'
                    else:
                        for x in pups:
                            if x == line[0]:
                                pups[x] += int(line[1])
                                break
                        else:
                            pups[line[0]] = int(line[1])
        if ln > 1:
            for y in pups.items():
                out += f'{y[0]} - {y[1]} из {ln}\n'
        bot.send_message(self.mes.chat.id, out)


    def task_del(self):
        rmtree(f"tasks/{self.subject}/{listdir(f'tasks/{self.subject}')[int(self.mes.text) - 1]}")
        bot.send_message(self.mes.chat.id, 'Работа удалена')
        self.menu_pos = self.t_in_menu
        bot.send_message(self.mes.chat.id, '''Выберите пункт:

1.Добавить работу
2.Удалить работу
3.Результаты учеников
4.Выход из аккаунта''')


    def nt_name(self):
        for i in listdir(f'tasks/{self.subject}'):
            if i == self.mes.text:
                bot.send_message(self.mes.chat.id, 'Работа с таким именем уже есть')
                break
        else:
            self.nt_load_folder = self.mes.text
            Path(f'tasks/{self.subject}/{self.mes.text}/mat').mkdir(parents=True, exist_ok=True)
            self.menu_pos = self.nt_photo
            self.file_counter = 0
            bot.send_message(self.mes.chat.id, '''При наличии загрузите фотоматериал к работе
(по одной фотографии).
Для завершения введите "Далее"''')


    def nt_photo(self):
        if self.mes.text == 'Далее':
            self.menu_pos = self.nt_text
            self.file_counter = 0
            bot.send_message(self.mes.chat.id, '''При наличии загрузите текстовый материал к работе.
Для завершения введите "Далее"''')


    def nt_text(self):
        if self.mes.text == 'Далее':
            self.menu_pos = self.nt_ans
            self.file_counter = 0
            Path(f'tasks/{self.subject}/{self.nt_load_folder}/ans').mkdir(parents=True, exist_ok=True)
            Path(f'tasks/{self.subject}/{self.nt_load_folder}/res').mkdir(parents=True, exist_ok=True)
            bot.send_message(self.mes.chat.id, '''Загрузите ответы к каждому пункту работы
(отправляйте по очереди).
Для завершения введите "Далее"''')
        else:
            if self.text_check2(self.mes.text):
                self.file_counter += 1
                with open(f'tasks/{self.subject}/{self.nt_load_folder}/mat/text_{self.file_counter}.txt', 'w', encoding='utf-8') as file:
                    file.write(self.mes.text)


    def nt_ans(self):
        if self.mes.text == 'Далее':
            for i in range(self.file_counter):
                open(f'tasks/{self.subject}/{self.nt_load_folder}/res/{i+1}.txt', 'w', encoding='utf-8')
            self.menu_pos = self.nt_exp
            self.file_counter = len(listdir(f'tasks/{self.subject}/{self.nt_load_folder}/ans')) - 1
            bot.send_message(self.mes.chat.id, '''Загрузите пояснения ответы к каждому пункту работы.
При отсутствии такового введите "Далее"''')
            bot.send_message(self.mes.chat.id, 'Пункт 1:')
        else:
            if self.text_check2(self.mes.text):
                self.file_counter += 1
                with open(f'tasks/{self.subject}/{self.nt_load_folder}/ans/{self.file_counter}.txt', 'w', encoding='utf-8') as file:
                    file.write(self.mes.text + '|')


    def nt_exp(self):
        in_counter = self.file_counter
        if self.text_check2(self.mes.text):
            if self.mes.text != 'Далее':
                with open(f'tasks/{self.subject}/{self.nt_load_folder}/ans/{str(in_counter - self.file_counter + 1)}.txt', 'a', encoding='utf-8') as file:
                    file.write(self.mes.text)
            self.file_counter -= 1
            if self.file_counter >= 0:
                bot.send_message(self.mes.chat.id, f'Пункт {str(in_counter - self.file_counter + 1)}:')
            else:
                self.nt_load_folder = ''
                self.menu_pos = self.t_in_menu
                bot.send_message(self.mes.chat.id, 'Готово')
                bot.send_message(self.mes.chat.id, '''Выберите пункт:

1.Добавить работу
2.Удалить работу
3.Результаты учеников
4.Выход из аккаунта''')


    # главные методы

    def main(self):
        if self.mes.text == '/start' or self.mes.text == 'Нзд':
            bot.send_message(self.mes.chat.id, '''Выберите пункт:

1.Вход
2.Регистрация учащегося''')

        elif self.mes.text == '1':
            self.menu_pos = self.log
            bot.send_message(self.mes.chat.id, 'Введите свое имя и фамилию')
        elif self.mes.text == '2':
            self.menu_pos = self.reg
            bot.send_message(self.mes.chat.id, 'Введите свое имя и фамилию')


    def back(self):
        tags = {
            self.reg : self.main,
            self.reg_pass : self.main,
            self.log : self.main,
            self.log_pass : self.main,
            self.subs : self.in_menu,
            self.tasks : self.subs,
            self.task : self.tasks,
            self.point : self.tasks,
            self.ans : self.point,
            self.res_show : self.tasks,
            self.nt_name : self.t_in_menu,
            self.nt_photo : self.t_in_menu,
            self.nt_text : self.t_in_menu,
            self.nt_ans : self.t_in_menu,
            self.nt_exp : self.t_in_menu,
            self.task_del : self.t_in_menu
        }

        if self.menu_pos != self.main and self.menu_pos != self.in_menu and self.menu_pos != self.t_in_menu:
            if self.subject != '' and self.menu_pos == self.tasks:
                self.menu_pos = self.t_in_menu
            else:
                self.menu_pos = tags[self.menu_pos]
            self.menu_pos()


    def receiver(self, mes):
        self.mes = mes
        if self.mes.text == '/start':
            self.main()
        elif self.mes.text == 'Нзд':
            self.back()
        else:
            self.menu_pos()




bot = telebot.TeleBot('6913650332:AAHwmK8PD0vUZoTYxnSXuYsjmYPB4C_SbGI')
users = {}


@bot.message_handler(content_types=['text'])
def run(mes):
    if mes.text == '/start':
        users[mes.from_user.id] = User(mes.from_user.id)
        bot.send_message(mes.chat.id, 'Добро пожаловать в Задачник-7500')
        bot.send_message(mes.chat.id, '''Уточнительная информация:

• В любой момент введите "Нзд", чтобы  
  вернуться на предыдущую страницу

• В целях соблюдения достоверности
  регистрация учителей производится
  персонально

По вопросам обращаться сюда: @male_626
                        ''')

    try:
        users[mes.from_user.id].receiver(mes)
    except Exception as exp:
        print(exp)


@bot.message_handler(content_types=['photo'])
def get_photo(mes):
    obj = users[mes.from_user.id]
    if obj.menu_pos == obj.nt_photo:
        obj.file_counter += 1
        file_info = bot.get_file(mes.photo[-1].file_id)
        file = bot.download_file(file_info.file_path)
        save_path = f'tasks/{obj.subject}/{obj.nt_load_folder}/mat/photo_{obj.file_counter}.jpg'
        with open(save_path, 'wb') as new_file:
            new_file.write(file)


bot.polling()