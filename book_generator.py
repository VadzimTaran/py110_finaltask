from random import randint, uniform, random
from faker import Faker
from os import path, stat
import re
import json

CONFPYFILE = "conf.py"
BOOKSTXTFILE = "books.txt"
AUTHORSTXTFILE = "authors.txt"


# декоратор для проверки выходных файлов
def decor_check_output_file(func):
    def wrapper(file_name, number):
        # проверяем количество
        try:
            if not isinstance(number, int) or number <= 0:
                raise ValueError
        except ValueError:
            print(f"Количество [{number}] недопустимо")
            return
        # проверяем, есть ли файл
        file_found = False
        try:
            book_titles = []
            with open(file_name, "rt") as book_txt_file:
                file_found = True
                for title_line in book_txt_file:
                    if not title_line:
                        continue
                    book_titles.append(title_line)
        except FileNotFoundError:
            print(f"Файл [{file_name}] не найден - генерируем")
        if file_found:
            if not book_titles:
                print("Список пуст - генерируем")
            elif len(book_titles) < number:
                print(f"Список меньше [{number}] - генерируем")
            else:
                return
        func(file_name=file_name, number=number)

    return wrapper


# декоратор для проверки входных файлов
def decor_check_input_file(func):
    def wrapper(file_name):
        # проверяем, есть ли файл
        if not path.isfile(file_name):
            print(f"Файл [{file_name}] не найден")
            return
        if stat(file_name) == 0:
            print(f"Файл [{file_name}] пустой")
            return
        result = func(file_name=file_name)
        return result

    return wrapper


# проверка имени автора
def check_author_name(author_name_line, pattern):
    match_ = None
    author_name = author_name_line.strip()
    if isinstance(pattern, str):
        match_ = re.fullmatch(pattern, author_name)
    else:
        match_ = pattern.fullmatch(author_name)
    return match_ is not None


# декоратор для проверки входных файлов
def decor_check_input_authors_file(func):
    def wrapper(file_name, number):
        # проверяем количество
        try:
            if number is None:
                number = randint(1, 3)
            if not isinstance(number, int) or 3 < number < 1:
                raise ValueError
        except ValueError:
            print(f"Количество [{number}] недопустимо")
            return
        # проверяем, есть ли файл
        if not path.isfile(file_name):
            print(f"Файл [{file_name}] не найден")
            return
        if stat(file_name) == 0:
            print(f"Файл [{file_name}] пустой")
            return
        # проверяем содержимое файла
        # Файл со списком имен и фамилий авторов должен быть проверен на корректность с помощью 
        # регулярных выражений. Каждая строка должна состоять из двух слов, начинающихся с заглавных 
        # букв, остальные буквы должны быть строчными. 
        author_pattern = re.compile(r"^[A-Z][a-z]+?\s+?[A-Z][a-z]+?\W*?$")
        with open(file_name, "rt") as author_file:
            for author_line in author_file:
                author = author_line.strip()
                # Если строка с фамилией и именем автора не
                # удовлетворяет указанным условиям, то должно возникать исключение ValueError с указанием
                # номера и значением строки, которая не прошла проверку.
                if not check_author_name(author, author_pattern):
                    print(f"Имя [{author}] не соответствует условию")
                    raise ValueError
        result = func(file_name=file_name, number=number)
        return result

    return wrapper


# “model” содержится в конфигурационном файле conf.py, его значение считывается оттуда
@decor_check_input_file
def get_model(file_name=CONFPYFILE):
    with open(file_name, "rt") as config_file:
        for model_line in config_file:
            return model_line.strip()


# генерирует conf.py
@decor_check_output_file
def init_conf_py(file_name, number):
    model_prefix = "model_"
    with open(file_name, "w") as conf_file:
        for idx in range(number):
            model = model_prefix + str(idx)
            conf_file.write(model + "\n")


# “pk” является автоинкрементом, то есть счётчиком, который увеличивается на единицу при
#   генерации нового объекта.
#   По умолчанию значение поля “pk” = 1.
#   Также должна быть реализована возможность устанавливать начальное значение через аргумент
#   командной строки “pk”.get
def get_pk(start=1):
    curr_pk = start
    while True:
        yield curr_pk
        curr_pk += 1


# “title” - содержит в себе название книги.
#   Является обязательным полем и не может быть пустым.
#   Список возможных названий хранится в файле books.txt. Каждая книга указана на отдельной строке
@decor_check_input_file
def get_title(file_name):
    book_titles = []
    with open(file_name, "rt") as book_file:
        for title_line in book_file:
            if not title_line:
                continue
            book_titles.append(title_line)
    idx = randint(0, len(book_titles) - 1)
    curr_title = book_titles[idx].strip()
    while True:
        yield curr_title
        curr_title = book_titles[randint(0, len(book_titles))].strip()


# генерирует book.txt
@decor_check_output_file
# def init_book_txt(file_name=BOOKSTXTFILE, number=100):
def init_book_txt(file_name, number):
    # генерация
    fake = Faker()
    with open(file_name, "w") as book_file:
        for _ in range(number):
            title = fake.paragraph(nb_sentences=1)
            book_file.write(title + "\n")


# “year” является натуральным числом.
#   Генерируется случайным образом.
def get_year():
    start_year = 1600
    end_year = 2021
    curr_year = randint(start_year, end_year)
    while True:
        yield curr_year
        curr_year = randint(start_year, end_year)


# “pages” является натуральным числом.
#   Генерируется случайным образом.
def get_pages():
    return randint(0, 2000)


# “isbn13” международный стандартный книжный номер.
#   Генерируется случайным образом.
def get_isbn13():
    fake = Faker()
    curr_isbn13 = fake.isbn13()
    while True:
        yield curr_isbn13
        curr_isbn13 = fake.isbn13()


# “rating” - число с плавающей запятой в диапазоне от 0 до 5 обе границы включительно.
#   Генерируется случайным образом
def get_rating(start=0, end=5):
    curr_rating = round(uniform(start, end), 3)
    while True:
        yield curr_rating
        curr_rating = round(uniform(start, end), 3)


# “price” - число с плавающей запятой.
#   Генерируется случайным образом.
def get_price(start=1, end=100000):
    curr_price = round(uniform(start, end), 3)
    while True:
        yield curr_price
        curr_price = round(uniform(start, end), 3)


# “discount” - размер скидки в виде натурального числа от 1 до 100.
#   Генерируется случайным образом.
#   Если скидка отсутствует, то поле принимает значение None.
def get_discount(start=1, end=100):
    curr_discount = round(uniform(start, end), 3)
    while True:
        yield curr_discount
        curr_discount = round(uniform(start, end), 3)


# “author” - список авторов. Содержит от 1 до 3 авторов.
#   Имя и фамилия автора выбираются случайным образом из файла authors.txt, который содержит
#   в себе перечень имен и фамилий.
#   Название файла, должно быть указано в виде переменной с константным значением.
@decor_check_input_authors_file
def get_authors(file_name, number):
    authors = []
    with open(file_name, "rt") as authors_file:
        for author_line in authors_file:
            authors.append(author_line)
    curr_authors = []
    for i in range(0, number):
        idx = randint(0, len(authors) - 1)
        author = authors[idx].strip()
        curr_authors.append(author)
    return curr_authors


# генерирует book.txt
@decor_check_output_file
def init_authors_txt(file_name, number):
    # генерация
    fake = Faker()
    with open(file_name, "w") as author_file:
        while number:
            author = fake.name()
            if check_author_name(author, r"^[A-Z][a-z]+?\s+?[A-Z][a-z]+?\W*?$"):
                author_file.write(author + "\n")
                number -= 1
            else:
                continue


# инициализация файлов
def init_files():
    # генерируем book.txt
    init_book_txt(BOOKSTXTFILE, 100)
    # генерируем conf.py
    init_conf_py(CONFPYFILE, 1)
    # генерируем authors.txt
    init_authors_txt(AUTHORSTXTFILE, 100)


# генерирует данные об 1 книге
def generate_book_data(pk, authors, sale):
    book_data = dict()

    # {
    #     "model": "shop_final.book",
    #     "pk": 1,
    #     "fields": {
    #         "title": "test_book",
    #         "year": 2020,
    #         "pages": 123,
    #         "isbn13": "978-1-60487-647-5",
    #         "rating": 5,
    #         "price": 123456.0,
    #         "discount": 20,
    #         "author": [
    #             "test_author_1",
    #             "test_author_2"
    #         ]
    #     }
    # }

    # генерирует model
    book_data["model"] = get_model(CONFPYFILE)
    # pk
    book_data["pk"] = pk
    # генерирует fields
    fields_data = dict()
    # генерирует title
    fields_data["title"] = next(get_title(BOOKSTXTFILE))
    # генерирует year
    fields_data["year"] = next(get_year())
    # генерирует pages
    fields_data["pages"] = get_pages()
    # генерирует isbn13
    fields_data["isbn13"] = next(get_isbn13())
    # генерирует rating
    fields_data["rating"] = next(get_rating())
    # генерирует price
    fields_data["price"] = next(get_price())
    # генерирует discount
    fields_data["discount"] = next(get_discount()) if sale else None
    # генерирует author
    fields_data["author"] = get_authors(AUTHORSTXTFILE, authors)

    book_data["fields"] = fields_data

    return book_data


# генерирует данные об 'count' книгах
def generate_n_book_data(count, authors=None, sale=False):
    # инициализируем файлы данных
    init_files()
    # генерируем данные о книгах
    pk_gen = get_pk()
    return [generate_book_data(next(pk_gen), authors=authors, sale=sale) for i in range(count)]


# пишет данные в json файл
def to_json_file(obj, filename, indent=1):
    with open(filename, "w") as f:
        json.dump(obj, f, indent=indent)


# пишет данные в csv файл
def to_csv_file(obj, filename, delimiter=",", string_delimiter="\n"):
    with open(filename, "w") as f:
        header_str = delimiter.join(obj[0].keys())
        f.write(header_str + string_delimiter)
        for data in obj:
            data_str = delimiter.join(data.values())
            f.write(data_str + string_delimiter)


if __name__ == '__main__':
    # # генерируем book.txt
    # init_book_txt(BOOKSTXTFILE, 100)
    # # генерируем conf.py
    # init_conf_py(CONFPYFILE, 1)
    # генерируем authors.txt
    init_authors_txt(AUTHORSTXTFILE, 100)

    # # test get_model
    # print("model: ", get_model(CONFPYFILE))
    #
    test_num = 5
    # # test get_pk
    # pk_generator = get_pk(2)
    # for _ in range(test_num):
    #     print("pk: ", next(pk_generator))
    # # test get_title
    # title_generator = get_title(BOOKSTXTFILE)
    # for _ in range(test_num):
    #     print("title: ", next(title_generator))
    # # test get_pages
    # for _ in range(test_num):
    #     print("pages: ", get_pages())
    # # test get_isbn13
    # isbn13_generator = get_isbn13()
    # for _ in range(test_num):
    #     print("isbn13: ", next(isbn13_generator))
    # # test get_rating
    # rating_generator = get_rating()
    # for _ in range(test_num):
    #     print("rating: ", next(rating_generator))
    # # test get_price
    # price_generator = get_price()
    # for _ in range(test_num):
    #     print("price: ", next(price_generator))
    # # test get_price
    # discount_generator = get_discount()
    # for _ in range(test_num):
    #     print("discount: ", next(discount_generator))
    # test get_authors
    for _ in range(test_num):
        print("author: ", get_authors(AUTHORSTXTFILE, 3))
    # test init_files
    # init_files()
    # test generate_book_data
    # pk_generator = get_pk()
    # print([generate_book_data(next(pk_generator), 3, sale=True) for i in range(5)])
    # to_json_file([generate_book_data(next(pk_generator), sale=True) for i in range(5)], "test.json", indent=4)
    # to_csv_file([generate_book_data(next(pk_generator), sale=True) for i in range(5)], "test.csv", delimiter=",",
    #             string_delimiter="\n")
    # to_json_file(generate_n_book_data(test_num), "test.json", indent=4)
