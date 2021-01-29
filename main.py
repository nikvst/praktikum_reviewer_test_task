# Ниже есть многочисленные нарушения pep8 и остальных стилистических соглашений.
# Далее я подробнее остановлюсь на каждом моменте, но на будущее рекомендую
# использовать автоматизированные инструменты для проверки стилей -
# линтеры (например, flake8 - https://github.com/PyCQA/flake8) или форматтеры
# (например, black - https://github.com/psf/black).
# Или всегда можно воспользоваться IDE, в которой есть встроенные инструменты
# для провекри стилей.
import datetime as dt
# Этот импорт лишний, т.к. модуль json нигде не вызывается.
# Чтобы не контролировать использование импортов и их сортировку
# рекомендую инструмент isort (https://github.com/PyCQA/isort)
# который автоматизирует эту работу.
import json

# здесь нехватает отступа
# https://www.python.org/dev/peps/pep-0008/#blank-lines
class Record:
    # Здесь у аргмента date значением по умолчанию указана пустая строка, хотя
    # ниже нам нигде это не требуется. Лучше будет указать None
    # Если хочется явно показать, что это строка, то можно воспользоваться
    # аннотациями типов и написать `date: Optional[str] = None`
    # (Optional нужно предварительно импортировать из модуля typing)
    def __init__(self, amount, comment, date=''):
        # вокруг операции присваивания нужны пробелы
        # https://www.python.org/dev/peps/pep-0008/#other-recommendations
        self.amount=amount
        # со строкой ниже есть несколько проблем
        # 1. она длиньше 79 символов
        # 2. если в `date` будет неправильная строка, то этот код упадет с
        #    ошибкой ValueError. Возможно стоит обработать эту ошибку
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, '%d.%m.%Y').date()
        # снова не хватает пробелов вокруг =
        self.comment=comment
# 1. здесь нужны два отступа
# 2. Если у класса Calculator не будет собственных экземпляров и предполагается
#    что от него будут только наследоваться другие классы, то этот класс
#    является абстрактным. Можно явно это показать, унаследовав его от класса
#    ABC из модуля abc (у меня нет под рукой нормальных статей по этой теме,
#    могу только приложить ссылку на оригинальную документацию
#    https://docs.python.org/3/library/abc.html)
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        # нет пробелов вокруг =
        self.records=[]
    # нет отступа
    def add_record(self, record):
        self.records.append(record)
    # нет отступа
    def get_today_stats(self):
        # нет пробелов вокруг =
        today_stats=0
        # 1. с большой буквы мы обычно называем классы -
        #    https://www.python.org/dev/peps/pep-0008/#class-names,
        #    здесь же нужно писать record с маленькой буквы -
        #    https://www.python.org/dev/peps/pep-0008/#method-names-and-instance-variables
        # 2. Если ты знаком с конструкцией list comprehension, то такие
        #    конструкции очень удобно оформлять с помощью них
        #    https://ru.wikipedia.org/wiki/Списковое_включение#Python
        #    например:
        #    today = dt.date.today()
        #    today_stats = sum([record.amount for self.records if record.date == today])
        #    или можно отбросить квадратные скобки из этого генератор
        for Record in self.records:
            # получение сегодняшней даты лучше вынести за пределы цикла, чтобы
            # не делать одну и ту же работу на каждой иттераци
            if Record.date == dt.datetime.now().date():
                # нет пробелов вокруг +
                today_stats = today_stats+Record.amount
        return today_stats
    # нет отступа
    def get_week_stats(self):
        week_stats=0
        today = dt.datetime.now().date()
        for record in self.records:
            # ниже слишком длинная строка и вокруг операторов < и >= нехватает
            # пробелов (в после "-" их слишком много).
            # python позволяет весьма изящно записывать такие выражения:
            # 0 <= (today - record.date).days < 7
            if (today -  record.date).days <7 and (today -  record.date).days >=0:
                # нет пробела после +=
                week_stats +=record.amount
        return week_stats
# нет двух отступов
class CaloriesCalculator(Calculator):
    # Комментарий ниже должен быть оформлен как docstring
    def get_calories_remained(self): # Получает остаток калорий на сегодня
        # Нет пробелов вокруг операторов "=" и "-"
        # Ничего не говорящее название переменной.
        x=self.limit-self.get_today_stats()
        if x > 0:
            # слишком длинная строка.
            # такие строки можно переносить с ипользованием скобок, например:
            # return (
            #     f'Сегодня можно съесть что-нибудь ещё, но с общей '
            #     'калорийностью не более {x} кКал'
            # )
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'
        # Этот else следует убрать, т.к. он ни на что не влияет
        else:
            return 'Хватит есть!'
# нет двух отступов
class CashCalculator(Calculator):
    # проблемы общие для следующих двух строк:
    # 1. Деньги нельзя хранить в float! Попробуй запустить интерпретатор и
    #    выполнить `1.2 - 1.0`. Результат будет совсем не тем, который ты
    #    ожидаешь.
    #    Чтобы избежать ошибок округления, следует использовать Decimal
    #    (или воспользоваться типом данных Money из библиотеки
    #    https://github.com/py-moneyed/py-moneyed)
    # 2. не хватает отступов вокруг =
    # 3. комментарии должны минимум на два пробела отступать от кода,
    #    а между комментарием и "#" должен быть пробел
    #    https://www.python.org/dev/peps/pep-0008/#inline-comments
    USD_RATE=float(60) #Курс доллар США.
    EURO_RATE=float(70) #Курс Евро.
    # 1. нет отступа
    # 2. слишком длинная строка
    # 3. аргументы не должны называться в загланых сивмолах
    # 4. могут быть ошибки с таким присваиванием значений по умолчанию, лучше
    #    в аргументах указать `USD_RATE=None, EURO_RATE=None` и подставлять
    #    значения по умолчанию уже в теле метода
    def get_today_cash_remained(self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # нет оступов вокруг =
        currency_type=currency
        cash_remained = self.limit - self.get_today_stats()
        # 1. нет оступов вокруг ==
        # 2. Этот блок удобнее оформить в виде словаря:
        #    что-то вроде этого:
        #    currency = {
        #        'usd': {
        #            'verbose_name': 'USD',
        #            'rate': usd_rate or self.USD_RATE,
        #         },
        #        'eur': {
        #            'verbose_name': 'Euro',
        #            'rate': euro_rate or self.EURO_RATE,
        #         },
        #        'rub': {
        #            'verbose_name': 'руб',
        #            'rate': Decimal(1),
        #         },
        #    }
        if currency=='usd':
            cash_remained /= USD_RATE
            # нет оступа после =
            currency_type ='USD'
        # нет оступов вокруг ==
        elif currency_type=='eur':
            cash_remained /= EURO_RATE
            # нет оступа после =
            currency_type ='Euro'
        # нет оступов вокруг ==
        elif currency_type=='rub':
            # Здесь происходит сравнение, но оно ни на то не влияет.
            # Эту строку можно в принципе удалить
            cash_remained == 1.00
            # нет оступа после =
            currency_type ='руб'
        if cash_remained > 0:
            # 1. В f-sting не должно быть никаких вычислений
            # 2. Если правильно использовать Decimal, то round скорее всего и
            #    не понадобится
            # 3. строка слишком длинная
            return f'На сегодня осталось {round(cash_remained, 2)} {currency_type}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # последний elif можно убрать, если cash_remained не меньше 0, 
        # то к этому моменту уже бы сработало одно из условий выше  
        elif cash_remained < 0:
            # длинная строка
            return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(-cash_remained, currency_type)

    # Кажется тут ошибка и метод ниже нужно полностью удалить:
    # 1. Зачем переопределять метод, если мы ничего не меняем?
    # 2. Этот метод хоть и вызывает super().get_week_stats(), но ничего не
    #    возвращает. Здесь результатом всегда будет None
    def get_week_stats(self):
        super().get_week_stats()
