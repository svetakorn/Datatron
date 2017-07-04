#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import uuid
import datetime
from os import getcwd, listdir

import requests

from data_retrieving import DataRetrieving


def post_request_to_server(request):
    return requests.post('http://api.datatron.ru/test', {"Request": request})


def cube_testing(local=True):
    """Метод для тестирования работы системы по кубам.
    Тесты находятся в папке tests и имеют следующую структуру названия
    cube_<local/server>_<имя куба>

    :param local: если True, то тестируется локальная система, если False, то стоящая на сервере
    :return: None
    """
    test_path = r'{}\{}'.format(getcwd(), 'tests')
    file_name = 'cube_{}_{}_OK_{}_Fail_{}.txt'

    test_files_paths = []
    testing_results = []
    true_answers = 0

    for file in listdir(test_path):
        if file.startswith("cubes_test"):
            test_files_paths.append(r'{}\{}'.format(test_path, file))

    for tf in test_files_paths:
        with open(r'{}'.format(tf), 'r', encoding='utf-8') as file_in:
            doc_name_output_str = 'Файл: {}'.format(tf.split('\\')[-1])
            testing_results.append(doc_name_output_str)
            print(doc_name_output_str)

            for idx, line in enumerate(file_in):
                line = ' '.join(line.split())

                if line.startswith('*'):
                    continue

                req, answer = line.split(':')
                if local:
                    system_answer = json.loads(DataRetrieving.get_data(
                        req, uuid.uuid4(),
                        formatted=False
                    ).toJSON())
                else:
                    system_answer = json.loads(post_request_to_server(req).text)

                response = system_answer['cube_documents']['response']
                if response:
                    try:
                        assert int(answer) == response
                        ars = '{}. + Запрос "{}" отрабатывает корректно'.format(idx, req)
                        testing_results.append(ars)
                        true_answers += 1
                        print(ars)
                    except AssertionError:
                        ars = (
                            '{}. - Запрос "{}" отрабатывает некорректно' +
                            '(должны получать: {}, получаем: {})'
                        )
                        ars = ars.format(idx, req, int(answer), response)
                        testing_results.append(ars)
                        print(ars)
                else:
                    ars = '{}. - Запрос "{}" вызвал ошибку: {}'
                    ars = ars.format(idx, req, system_answer['message'])
                    testing_results.append(ars)
                    print(ars)

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    false_answers = len(testing_results) - true_answers - len(test_files_paths)

    if local:
        file_name = file_name.format('local', current_datetime, true_answers, false_answers)
    else:
        file_name = file_name.format('server', current_datetime, true_answers, false_answers)

    with open(r'{}\{}'.format(test_path, file_name), 'w', encoding='utf-8') as file_out:
        file_out.write('\n'.join(testing_results))

    print('Лог прогона записан в файл {}'.format(file_name))


def minfin_testing(local=True):
    """Метод для тестирования работы системы по вопросам Минфина.
    Тесты находятся в папке tests и имеют следующую структуру названия:
    minfin_test_<auto/manual>_<local/server>_for_<номер партии>_questions
    mifin_test_auto - создаются автоматически на основе документов из папки data/minfin
    mifin_test_manual - прописываются вручную

    :param local: если True, то тестируется локальная система, если False, то стоящая на сервере
    :return: None
    """
    test_files_paths = []
    test_path = r'{}\{}'.format(getcwd(), 'tests')
    file_name = 'minfin_{}_{}_OK_{}_Fail_{}.txt'
    testing_results = []
    true_answers = 0

    for file in listdir(test_path):
        if file.startswith("minfin_test"):
            test_files_paths.append(r'{}\{}'.format(test_path, file))

    for tf in test_files_paths:
        with open(tf, 'r', encoding='utf-8') as file:
            doc_name_output_str = 'Файл: {}'.format(tf.split('\\')[-1])
            testing_results.append(doc_name_output_str)
            print(doc_name_output_str)

            for line in file:
                req, question_id = line.split(':')
                if local:
                    system_answer = json.loads(DataRetrieving.get_data(req, uuid.uuid4()).toJSON())
                else:
                    system_answer = json.loads(post_request_to_server(req).text)

                response = system_answer['minfin_documents']['number']
                question_id = ''.join(question_id.split())
                if response:
                    try:
                        assert question_id == str(response)
                        ars = '{q_id}  + Запрос "{req}" отрабатывает корректно'
                        ars = ars.format(q_id=question_id, req=req)
                        testing_results.append(ars)
                        true_answers += 1
                    except AssertionError:
                        ars = (
                            '{q_id} - Запрос "{req}" отрабатывает некорректно ' +
                            '(должны получать:{q_id}, получаем:{fl})'
                        )
                        ars = ars.format(q_id=question_id, req=req, fl=response)
                        testing_results.append(ars)
                else:
                    # TODO: подправить MSG
                    ars = '{q_id}  - Запрос "{req}" вызвал ошибку: {msg}'.format(
                        q_id=question_id,
                        req=req,
                        msg='Не определена'
                    )
                    testing_results.append(ars)
                print(ars)

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    false_answers = len(testing_results) - true_answers - len(test_files_paths)
    if local:
        file_name = file_name.format('local', current_datetime, true_answers, false_answers)
    else:
        file_name = file_name.format('server', current_datetime, true_answers, false_answers)

    with open(r'{}\{}'.format(test_path, file_name), 'w', encoding='utf-8') as file:
        file.write('\n'.join(testing_results))

    print('Лог прогона записан в файл {}'.format(file_name))


if __name__ == "__main__":
    cube_testing()
    minfin_testing()
