from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

class OLParser:
    def __init__(self, n=1):
        """Метод подготавливает браузер и открывает в нём сцену из objection.lol.
        По умолчанию использует Chrome"""

        if(n == 1):
            self.driver = webdriver.Chrome()
        if(n == 2):
            self.driver = webdriver.Firefox()
        if(n == 3):
            self.driver = webdriver.Edge()
        if(n == 4):
            self.driver = webdriver.Ie()
        if(n == 5):
            self.driver = webdriver.Safari()

        self.driver.get("https://objection.lol/edit/scene/4817606")
        self.driver.maximize_window()
    
    def autorization(self, input='console'):
        """Метод авторизует вас на сайте objection.lol"""


        if(input == 'file'):
            filename = input('Введите название файла с данными. Внимение: требуется указание формата файла!\n')

            f = open(filename, 'r')

            login, passwd = f.read().split()
        if(input == 'console'):
            login, passwd = input('Введите через пробел логин и пароль аккаунта\n').split()

        #Получает все доступные кнопки на сайте
        actionbar = self.driver.find_elements(by=By.CLASS_NAME, value='v-btn')
        actionbar[5].click()

        #Обновление списка доступных кнопок
        #(некоторые из них находятся во фреймах, которые необходимо открыть перед захватом)
        actionbar = self.driver.find_elements(by=By.CLASS_NAME, value='v-btn')

        #Получает все поля для ввода, чтобы найти поля для ввода логина и пароля
        #(эти поля меняют свой id с каждым перезапуском браузера)
        textfields = self.driver.find_elements(by=By.TAG_NAME, value="input")

        #Ввод данных аккаунта в поля логина и пароля соответственно
        textfields[len(textfields) - 2].send_keys(login)
        textfields[len(textfields) - 1].send_keys(passwd)

        actionbar[len(actionbar) - 2].click()

    def get_lines(self, page=1, func='print'):
        """Метод получает все имеющиеся реплики в сцене на данной странице
        и проводит с ними некоторые операции. По умолчанию выводит в консоль
        все реплики в сцене со страницы 1."""

        #Получает все кнопки, переключающие страницы сцены
        pagination = self.driver.find_elements(by=By.CLASS_NAME, value='v-pagination__item')
        pagination[page - 1].click()

        #Получает все поля для ввода реплик
        textlines = self.driver.find_elements(by=By.TAG_NAME, value='textarea')

        if(func == 'print'):
            #Выводит в консоль все реплики на странице
            for i in textlines:
                print(i.get_attribute('value'))
        if(func == 'return'):
            for i in range(len(textlines)):
                textlines[i] = textlines[i].get_attribute('value')
            return textlines
        

        
    def get_character(self, page=1, func='print'):
        """Метод получает все окна реплик в сцене на данной странице и,
        открывая каждое по очереди, получает имена их персонажей из базы
        данных, а затем проводит с ними некоторые операции. По умолчанию
        выводит в консоль все имена персонажей со страницы 1."""

        char_list = []

        #Получает все кнопки, переключающие страницы сцены
        pagination = self.driver.find_elements(by=By.CLASS_NAME, value='v-pagination__item')
        pagination[page - 1].click()

        #Получает все окна реплик на данной странице
        charwindow = self.driver.find_elements(by=By.CLASS_NAME, value='col-sm-3')
        h = 350 #координаты Y для прокрутки окна вниз

        for i in charwindow:
            i.click()

            #Получает все поля ввода и из одного из них вытягивает имя персонажа в базе из этой реплики
            selectfields = self.driver.find_elements(by=By.TAG_NAME, value='input')
            
            if(func == 'print'):
                print(selectfields[7 + len(charwindow)].get_attribute('value'))
            if(func == 'return'):
                char_list.append(selectfields[7 + len(charwindow)].get_attribute('value'))
            
            #Прокрутка страницы вниз на одно поле реплики
            self.driver.execute_script('window.scrollTo(0, ' + str(h) + ')')

            h += 195

        if(func == 'return'):
            return char_list
        
    def get_pose_name(self, page=1, func='print'):
        """Метод получает все окна реплик в сцене на данной странице и,
        открывая каждое по очереди, получает названия поз их персонажей,
        а затем проводит с ними некоторые операции. По умолчанию выводит
        в консоль все названия поз персонажей со страницы 1."""

        pose_list = []

        #Получает все кнопки, переключающие страницы сцены
        pagination = self.driver.find_elements(by=By.CLASS_NAME, value='v-pagination__item')
        pagination[page - 1].click()

        #Получает все окна реплик на данной странице
        charwindow = self.driver.find_elements(by=By.CLASS_NAME, value='col-sm-3')
        h = 350 #координаты Y для прокрутки окна вниз

        for i in charwindow:
            i.click()

            #Получает все поля выбора и из одного из них вытягивает позу персонажа в этой реплике
            selectfields = self.driver.find_elements(by=By.CLASS_NAME, value='v-input__slot')

            if(func == 'print'):
                print(selectfields[5 + len(charwindow)].accessible_name)
            if(func == 'return'):
                pose_list.append(selectfields[5 + len(charwindow)].accessible_name)
            
            #Прокрутка страницы вниз на одно поле реплики
            self.driver.execute_script('window.scrollTo(0, ' + str(h) + ')')

            h += 195

        if(func == 'return'):
            return pose_list
        
    def get_speech_bubble(self, page=1, func='print'):
        """Метод получает все окна реплик в сцене на данной странице и,
        открывая каждое по очереди, получает названия выкриков их персонажей,
        а затем проводит с ними некоторые операции. По умолчанию выводит в консоль
        все названия выкриков персонажей со страницы 1."""

        sb_list = []

        #Получает все кнопки, переключающие страницы сцены
        pagination = self.driver.find_elements(by=By.CLASS_NAME, value='v-pagination__item')
        pagination[page - 1].click()

        #Получает все окна реплик на данной странице
        charwindow = self.driver.find_elements(by=By.CLASS_NAME, value='col-sm-3')
        h = 350

        for i in charwindow:
            i.click()

            bubblename = None

            #Получает все поля для ввода, а потом ищет среди них поле с выкриком персонажа
            textfields = self.driver.find_elements(by=By.CLASS_NAME, value="v-input__slot")

            for j in textfields:
                if(j.accessible_name.find('Speech Bubble') != -1 or j.accessible_name.find('Gavel') != -1):
                    bubblename = j.accessible_name

                    if(bubblename.find('Speech Bubble') != -1):
                        bubblename = bubblename.removeprefix('Speech Bubble ')
                    else:
                        bubblename = bubblename.removeprefix('Gavel ')
                    
                    break

            if(func == 'print'):
                print(bubblename)
            if(func == 'return'):
                sb_list.append(bubblename)

            #Прокрутка страницы вниз на одно поле реплики
            self.driver.execute_script('window.scrollTo(0, ' + str(h) + ')')

            h += 195
        
        if(func == 'return'):
            return sb_list
        
    def get_char_name(self, page=1, func='print'):
        """Метод получает все окна реплик в сцене на данной странице и,
        открывая каждое по очереди, получает пользовательские имена их
        персонажей, а затем проводит с ними некоторые операции. По умолчанию
        выводит в консоль все пользовательские имена персонажей со страницы 1."""

        cn_list = []
        
        #Получает все кнопки, переключающие страницы сцены
        pagination = self.driver.find_elements(by=By.CLASS_NAME, value='v-pagination__item')
        pagination[page - 1].click()

        #Получает все окна реплик на данной странице
        charwindow = self.driver.find_elements(by=By.CLASS_NAME, value='col-sm-3')
        h = 350

        for i in charwindow:
            i.click()

            #Получает все поля для ввода, а потом ищет среди них поле с пользовательским
            #именем персонажа
            textfields = self.driver.find_elements(by=By.TAG_NAME, value="input")

            if(func == 'print'):
                for j in textfields:
                    if(j.accessible_name == 'Custom Name'):
                        print(j.get_attribute('value'))
            
            if(func == 'return'):
                for j in textfields:
                    if(j.accessible_name == 'Custom Name'):
                        cn_list.append(j.get_attribute('value'))

            #Прокрутка страницы вниз на одно поле реплики
            self.driver.execute_script('window.scrollTo(0, ' + str(h) + ')')

            h += 195

        if(func == 'return'):
            return cn_list
        

    
    def overwrite_line(self, page=1, n = 1, new='foo'):
        """Метод получает на вход номер реплики на странице и строку,
        на которую необходимо заменить старую реплику. По умолчанию заменяет
        первую реплику на 'foo'"""

        #Получает все кнопки, переключающие страницы сцены
        pagination = self.driver.find_elements(by=By.CLASS_NAME, value='v-pagination__item')
        pagination[page - 1].click()

        #Получает все поля для ввода реплик
        textlines = self.driver.find_elements(by=By.TAG_NAME, value='textarea')

        #Очищает поле для ввода реплики и вводит туда же новую
        textlines[n - 1].clear()
        textlines[n - 1].send_keys(new)

    def save_scene(self):
        """Метод собирает всю основную информацию о сцене и сохраняет её в excel-файл"""

        cn, pn, sb, char, line = [], [], [], [], []

        pagination = self.driver.find_elements(by=By.CLASS_NAME, value='v-pagination__item')

        for i in range(1, len(pagination) + 1):
            char.extend(self.get_character(page=i, func='return'))
            pn.extend(self.get_pose_name(page=i, func='return'))
            sb.extend(self.get_speech_bubble(page=i, func='return'))
            cn.extend(self.get_char_name(page=i, func='return'))
            line.extend(self.get_lines(page=i, func='return'))

        char = pd.Series(char, name='Character_Name')
        pn = pd.Series(pn, name='Pose_Name')
        sb = pd.Series(sb, name='Speech_Bubble')
        cn = pd.Series(cn, name='Custom_Name')
        line = pd.Series(line, name='Line')

        df = pd.concat([char, pn, sb, cn, line], axis=1)
        df.index.name = 'Line_Number'

        df.to_excel('scene_info.xlsx')


    def actions(self, n):
        """Метод получает на вход число, согласно которому запускается
        та или иная функция. Предварительно функция возвращает страницу в
        исходное положение. По умолчанию запускает функцию 'get_lines'"""

        #Возвращение страницы в исходное положение
        self.driver.execute_script('window.scrollTo(0, 0)')

        if(n == 0):
            self.driver.close()
            exit(0)
        if(n == 1):
            self.autorization()
        if(n == 2):
            self.get_lines()
        if(n == 3):
            self.get_char_name()
        if(n == 4):
            self.get_pose_name()
        if(n == 5):
            self.get_speech_bubble()
        if(n == 6):
            self.get_character()
        if(n == 7):
            self.save_scene()


site = OLParser()

while True:
    n = int(input())

    site.actions(n)