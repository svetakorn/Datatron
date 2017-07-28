#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Поднимает сервис с API.
Поддерживает голос, текст и возвращает список документов по минфину
"""

from os import path, makedirs
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
from config import SETTINGS


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
        ).toJSON_API()


class MinfinList(Resource):
    """Возвращает весь список минфин вопросов. Актуально, пока их мало"""

    @time_with_message("MinfinList API Get", "info", 1)
    def get(self):
        return get_minfin_data()


app = Flask(__name__)  # pylint: disable=invalid-name
api = Api(app)  # pylint: disable=invalid-name
API_VERSION = getattr(SETTINGS.WEB_SERVER, 'VERSION', 'na')

parser = reqparse.RequestParser()  # pylint: disable=invalid-name
parser.add_argument('apikey', type=str, required=True, help="You need API key")
parser.add_argument('query', type=str)


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


@app.route('/')
def main():
    """Чтобы что-то выводило при GET запросе - простая проверка рабочего состояния серевера"""
    return '<center><h1>Welcome to Datatron Home API page</h1></center>'
