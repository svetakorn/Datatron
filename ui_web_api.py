#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Поднимает сервис с API.
Поддерживает голос, текст и возвращает список документов по минфину
"""

from os import path, makedirs, listdir
import re
import random
import logging
from uuid import uuid4
import json

import pandas as pd
from flask import Flask, request, make_response
from flask_restful import reqparse, abort, Api, Resource

from messenger_manager import MessengerManager
from kb.kb_support_library import read_minfin_data
import logs_helper  # pylint: disable=unused-import
from logs_helper import time_with_message
from config import SETTINGS, TEST_PATH_RESULTS

from models.responses.text_response_model import TextResponseModel

from utils.resource_helper import ResourceHelper


# pylint: disable=no-self-use
# pylint: disable=missing-docstring


def get_minfin_data():
    """
    Возвращает данные по минфину в виде, готовому для вывода.
    В данный момент, кеширует их в памяти при запуске.
    Предполагается, что данных не очень много.
    """
    if get_minfin_data.data is None:
        get_minfin_data.data = _read_minfin_data()

        # Можно сразу привести к байтам, чтобы не делать это каждый раз
        get_minfin_data.data = json.dumps(
            get_minfin_data.data,
            ensure_ascii=False,
            indent=4
        ).encode("utf-8")
    return get_minfin_data.data

get_minfin_data.data = None


@time_with_message("_read_minfin_data", "debug", 10)
def _read_minfin_data():
    """
    Читает xlsx данные, соединяет в один документ и возвращает словарь с соотв. полями.
    Возвращает массив из словарей с вопросами
    Почти повторяет _read_data из kb/minfin_docs_generation.py
    """

    # чтение данные по минфину
    _, dfs = read_minfin_data()

    # Объединение все датафреймов в один
    data = pd.concat(dfs)
    logging.info("Прочитано {} записей минфина".format(data.shape[0]))
    return tuple(
        {
            "id": item[0],
            "question": item[1]
        } for item in zip(
            data["id"].tolist(),
            data["question"].tolist()
        )
    )


def get_good_queries(count=0):
    """
    Возвращает успешные вопросы по кубам и минфину в перемешанном виде.
    Если count == 0, то возвращает все успешные запросы
    """

    if not get_good_queries.queries:
        good_cube_query_re = re.compile(r"\d*\.\s+\+\s+(.+)")
        good_mifin_query_re = re.compile(r'Запрос\s*"(.+)"\s*отрабатывает корректно')
        get_good_queries.queries = []

        test_paths = listdir(TEST_PATH_RESULTS)
        try:
            latest_cube_path = max(filter(lambda x: x.startswith("cube"), test_paths))
        except ValueError:
            logging.error("Нет тестов по кубам!")
        get_good_queries.queries += good_cube_query_re.findall(open(
            path.join(TEST_PATH_RESULTS, latest_cube_path),
            encoding="utf-8"
        ).read())

        try:
            latest_mifin_path = max(filter(lambda x: x.startswith("minfin"), test_paths))
        except ValueError:
            logging.error("Нет тестов по минфину!")
        get_good_queries.queries += good_mifin_query_re.findall(open(
            path.join(TEST_PATH_RESULTS, latest_mifin_path),
            encoding="utf-8"
        ).read())

        # А теперь поставим везде заглавной первую букву
        for ind, val in enumerate(get_good_queries.queries):
            get_good_queries.queries[ind] = val[0].upper() + val[1:]

    if count == 0 or count > len(get_good_queries.queries):
        count = len(get_good_queries.queries)
    return random.sample(get_good_queries.queries, count)

get_good_queries.queries = None


def is_valid_api_key(api_key):
    """
    Проверяет на правльность ключи доступа к API. На данный момент, один ключ
    может всё, без ограничений
    """
    return api_key in SETTINGS.API_KEYS  # pylint: disable=no-member


class VoiceQuery(Resource):
    """Обрабатывает отправку файлов голосом"""

    @time_with_message("VoiceQuery API Get", "info", 7)
    def post(self):
        args = parser.parse_args()

        if not is_valid_api_key(args["apikey"]):
            abort(403, message="API key {} is NOT valid".format(args["apikey"]))

        if 'file' not in request.files:
            abort(400, message='You need "file" parameter"')

        # Получение файла
        voice_file = request.files['file']

        # Определение его формата
        file_extension = voice_file.filename.rsplit('.', 1)[-1]

        # Определение дериктории для сохранения файла
        save_path = 'tmp'
        if not path.exists(save_path):
            makedirs(save_path)

        # Генерация случайного имени файла
        new_file_name = uuid4().hex[:10]

        # Сохранения полученного файла под новым именем в папку для хранения временных файлов
        file_path = path.join(save_path, '{}.{}'.format(new_file_name, file_extension))

        logging.debug("Создали новый временный файл {}".format(file_path))
        voice_file.save(file_path)

        request_id = uuid4().hex

        return MessengerManager.make_voice_request(
            "API v1",
            args["apikey"],
            "",
            request_id,
            filename=file_path
        ).toJSON_API()


class TextQuery(Resource):
    """Обрабатывает простой текстовой зарос"""

    @time_with_message("TextQuery API Get", "info", 4)
    def get(self):
        data = self.get_data()

        return data.toJSON_API()

    def get_data(self):
        args = parser.parse_args()
        logging.info(args)

        if not is_valid_api_key(args["apikey"]):
            abort(403, message="API key {} is NOT valid".format(args["apikey"]))

        request_text = args['query']
        request_id = uuid4().hex

        if len(args['query']) < 4:
            abort(400, message='You need "query" parameter"')

        return MessengerManager.make_request(
            request_text,
            "API v1",
            args["apikey"],
            "",
            request_id
        )


class MinfinList(Resource):
    """Возвращает весь список минфин вопросов. Актуально, пока их мало"""

    @time_with_message("MinfinList API Get", "info", 1)
    def get(self):
        return get_minfin_data()


# API v2
class VoiceQueryV2(Resource):
    """Обрабатывает отправку файлов голосом"""

    @time_with_message("VoiceQuery API Get", "info", 7)
    def post(self):
        args = parser.parse_args()

        if not is_valid_api_key(args["apikey"]):
            abort(403, message="API key {} is NOT valid".format(args["apikey"]))

        if 'file' not in request.files:
            abort(400, message='You need "file" parameter"')

        # Получение файла
        voice_file = request.files['file']

        # Определение его формата
        file_extension = voice_file.filename.rsplit('.', 1)[-1]

        # Определение дериктории для сохранения файла
        save_path = 'tmp'
        if not path.exists(save_path):
            makedirs(save_path)

        # Генерация случайного имени файла
        new_file_name = uuid4().hex[:10]

        # Сохранения полученного файла под новым именем в папку для хранения временных файлов
        file_path = path.join(save_path, '{}.{}'.format(new_file_name, file_extension))

        logging.debug("Создали новый временный файл {}".format(file_path))
        voice_file.save(file_path)

        request_id = uuid4().hex

        return MessengerManager.make_voice_request(
            "API v1",
            args["apikey"],
            "",
            request_id,
            filename=file_path
        ).toJSON_API()


class TextQueryV2(Resource):
    """Обрабатывает простой текстовой зарос"""

    @time_with_message("TextQuery API Get", "info", 4)
    def get(self):
        answer = self.get_data()

        return answer.toJSON_API()

    def get_data(self):
        text_query = TextQuery()
        answer = text_query.get_data()
        result = TextResponseModel.form_answer(answer)
        return result


class MinfinListV2(Resource):
    """Возвращает весь список минфин вопросов. Актуально, пока их мало"""

    @time_with_message("MinfinList API Get", "info", 1)
    def get(self):
        return get_minfin_data()


class GoodQueries(Resource):
    """
    Возвращает список хороших вопросов, которые можно задавать.
    """

    @time_with_message("GoodQueries API Get", "info", 0.5)
    def get(self):
        args = parser.parse_args()
        count = 0
        if not args["count"] is None:
            count = args["count"]
        return get_good_queries(count=count)


app = Flask(__name__)  # pylint: disable=invalid-name
api = Api(app)  # pylint: disable=invalid-name
API_VERSION = getattr(SETTINGS.WEB_SERVER, 'VERSION', 'na')

parser = reqparse.RequestParser()  # pylint: disable=invalid-name
parser.add_argument('apikey', type=str, required=True, help="You need API key")
parser.add_argument('query', type=str)
parser.add_argument('count', type=int)


@api.representation('application/json')
def output_json(data, code, headers=None):
    """
    Переопределим кодирование, чтобы не кодировать уже закодированное
    И отправлять юникод
    """
    if isinstance(data, bytes):
        resp = make_response(data, code)
    else:
        resp = make_response(json.dumps(data).encode("utf-8"), code)
    resp.headers.extend(headers or {})
    return resp


api.add_resource(VoiceQuery, '/{}/voice'.format(API_VERSION))
api.add_resource(TextQuery, '/{}/text'.format(API_VERSION))
api.add_resource(MinfinList, '/{}/minfin_docs'.format(API_VERSION))

# Реализуем API v2
api.add_resource(VoiceQueryV2, '/v2/voice')
api.add_resource(TextQueryV2, '/v2/text')
api.add_resource(MinfinListV2, '/v2/minfin_docs')
api.add_resource(GoodQueries, '/v2/good_queries')


@app.route('/')
def main():
    """Чтобы что-то выводило при GET запросе - простая проверка рабочего состояния серевера"""
    return '<center><h1>Welcome to Datatron Home API page</h1></center>'


@app.route('/v1/resources/image')
def get_image():
    """
    Получение картинки. Пока они все отдаются как jpeg. Это не вечно
    ToDo: фиксить один тип
    """
    img_name = request.args.get('path')

    return ResourceHelper.get_image(img_name)


@app.route('/v1/resources/document')
def get_document():
    """
    Получение документа. Пока они все отдаются как pdf. Это не вечно
    ToDo: фиксить один тип
    """
    doc_name = request.args.get('path')

    return ResourceHelper.get_document(doc_name)


@app.route('/v2/resources/image/<image_id>')
def get_image_v2(image_id):
    return ResourceHelper.get_image(image_id)


@app.route('/v2/resources/document/<document_id>')
def get_document_v2(document_id):
    return ResourceHelper.get_document(document_id)
