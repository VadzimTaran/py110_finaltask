from book_generator import generate_n_book_data, to_json_file, to_csv_file
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Для скрипта должны быть реализованы следующие аргументы:
    # count - количество случайных элементов, которое необходимо сгенерировать
    parser.add_argument("count", type=int)

    # authors - количество авторов для каждого элементов. Если не указано, то количество авторов
    #   для каждого объекта варьируется от 1 до 3
    parser.add_argument("authors", type=int)

    # sale - генерировать скидку или нет
    parser.add_argument("sale", type=bool)

    # output_format (json или csv), если не указано, то выводит сгенерированные книги в консоль
    #   в виде списка словарей.
    parser.add_argument("-o", "--output_format", type=str, help="json или csv")
    #   Если указано json или csv, то перенаправляет вывод в json или csv файл соответственно.
    #   Для json вывода должны запрашиваться 2 аргумента название файла и размер отступов (по умолчанию 0).
    parser.add_argument("-f", "--file_name", type=str, help="file name")
    parser.add_argument("-i", "--indent", type=int, default=0, help="размер отступов")
    #   Для csv название файла, разделитель строк (по умолчанию “\n”) и 
    #   разделитель элементов в строке (по умолчанию “,”)
    parser.add_argument("-d", "--delimiter", default=",", type=str, help="delimiter")
    parser.add_argument("-n", "--string_delimiter", default="\n", type=str, help="string delimiter")

    args = parser.parse_args()
    # получаем данные о книгах
    book_data = generate_n_book_data(args.count, args.authors, args.sale)
    # записываем в файл
    if args.output_format == "json":
        if not args.file_name:
            print(f"Не задано имя json файла")
            exit(1)
        elif not args.indent:
            print(f"Не задан отступ в json файле")
            exit(1)
        else:
            to_json_file(book_data, args.file_name, indent=args.indent)
    elif args.output_format == "csv":
        if not args.file_name:
            print(f"Не задано имя csv файла")
            exit(1)
        elif not args.delimiter or not args.string_delimiter:
            print(f"Не заданы разделители в csv файле")
            exit(1)
        else:
            to_csv_file(book_data, args.file_name, delimiter=args.indent, string_delimiter=args.string_delimiter)
    # или выводим на экран
    else:
        print(book_data)
