#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Управление классами ядра системы
"""

import logging

from core.solr import Solr
from core.cube_docs_processing import CubeAnswer
from core.support_library import group_documents
from core.support_library import send_request_to_server
from core.support_library import process_server_response
from core.support_library import process_cube_answer
from core.answer_object import CoreAnswer
from core.cube_docs_processing import CubeProcessor
from core.minfin_docs_processing import MinfinProcessor
from core.cube_classifier import CubeClassifier

from text_preprocessing import TextPreprocessing

from config import SETTINGS
from constants import ERROR_NO_DOCS_FOUND
from model_manager import MODEL_CONFIG
import logs_helper  # pylint: disable=unused-import


class DataRetrieving:
    """
    Модуль связывающие в себе результаты работы Apache Solr,
    и классов обработки его выдачи - CubeProcessor и MinfinProcessor
    """

    @staticmethod
    def get_data(user_request: str, request_id: str):
        """API метод к ядру системы"""

        core_answer = CoreAnswer()
        core_answer.user_request = user_request

        norm_user_request = DataRetrieving._preprocess_user_request(
            user_request,
            request_id
        )

        # получение результатов поиска от Apache Solr в JSON-строке
        solr_response = Solr.get_data(
            norm_user_request,
            request_id,
            SETTINGS.SOLR_MAIN_CORE
        )['response']

        # Если хотя бы 1 документ найден:
        if solr_response['numFound']:
            minfin_docs, cube_data = group_documents(
                solr_response['docs'],
                user_request,
                request_id
            )

            minfin_answers = MinfinProcessor.get_data(minfin_docs)

            clf = CubeClassifier.inst()
            best_prediction = tuple(clf.predict_proba(user_request))[0]

            cube_answers = CubeProcessor.get_data(cube_data, best_prediction)

            logging.info(
                "Query_ID: {}\tMessage: Найдено {} докумета(ов) по кубам и {} по Минфину".format(
                    request_id,
                    len(cube_answers),
                    len(minfin_answers)
                )
            )

            answers = DataRetrieving._sort_answers(minfin_answers, cube_answers)

            DataRetrieving._format_core_answer(answers, request_id, core_answer)
        else:
            # Обработка случая, когда документы не найдены
            core_answer.message = ERROR_NO_DOCS_FOUND
            logging.info(
                'Query_ID: {}\tMessage: Документа не найдены'.format(request_id)
            )

        return core_answer

    @staticmethod
    def _preprocess_user_request(user_request: str, request_id: str):
        """Предобработка запроса пользователя"""

        text_proc = TextPreprocessing(request_id)

        # нормализация запроса пользователя
        norm_user_request = text_proc.normalization(
            user_request,
            delete_question_words=False,
            parse_dates=True
        )

        if MODEL_CONFIG["delete_repeating_words_in_request"]:
            norm_user_request = DataRetrieving._set_user_request(
                norm_user_request, request_id
            )

        if MODEL_CONFIG["enable_repetition_for_short_request"]:
            norm_user_request = DataRetrieving._multiple_user_request(
                norm_user_request, request_id
            )

        return norm_user_request

    @staticmethod
    def _set_user_request(norm_user_request: str, request_id: str):
        """
        Удаление повторяющихся слов и увеличение длины запроса
        при необходимости
        """

        request_words = norm_user_request.split()
        unique_of_request_words = set(request_words)

        # удаление повторяющихся слов, чтобы пользователи не читерили
        if len(unique_of_request_words) != len(request_words):
            norm_user_request = ' '.join(unique_of_request_words)

            logging.info(
                "Query_ID: {}\tMessage: Удалено {} повторяющихся слов".format(
                    request_id,
                    len(request_words) - len(unique_of_request_words)
                )
            )

        return norm_user_request

    @staticmethod
    def _multiple_user_request(norm_user_request: str, request_id: str):
        """
        Дублирование коротких запросов
        """

        short_question_threshold = MODEL_CONFIG["short_request_threshold"]
        multiplier = MODEL_CONFIG["repetition_num_for_short_request"]
        request_len = len(norm_user_request.split())

        if request_len <= short_question_threshold:
            norm_user_request = ' '.join(
                [norm_user_request.strip()] * multiplier
            )

            logging.info(
                "Query_ID: {}\tMessage: Запрос из {} слов был "
                "удлинен в {} раза".format(
                    request_id,
                    request_len,
                    multiplier
                )
            )

        return norm_user_request

    @staticmethod
    def _sort_answers(minfin_answers: list, cube_answers: list):
        """Совокупное ранжирование ответов по кубам и минфину"""

        # Если по минфину найден только 1 ответ
        if not isinstance(minfin_answers, list):
            minfin_answers = [minfin_answers]

        # Если по куба найден только 1 ответ
        if not isinstance(cube_answers, list):
            cube_answers = [cube_answers]

        # Фильтрация выборки в порядке убывания по score
        all_answers = sorted(
            cube_answers + minfin_answers,
            key=lambda ans: ans.get_score(),
            reverse=True
        )

        return all_answers

    @staticmethod
    def _format_core_answer(answers: list, request_id: str, core_answer: CubeAnswer):
        """Формирование структуры финального ответа"""

        # Предельное количество "смотри также"
        THRESHOLD = 5

        if answers:
            DataRetrieving._process_main_answer(
                core_answer,
                answers,
                request_id
            )

            starting_from = 1
            if not core_answer.answer:
                starting_from = 0

            DataRetrieving._process_more_answers(
                core_answer,
                answers[starting_from:THRESHOLD + 1],
                request_id
            )

        return core_answer

    @staticmethod
    def _process_main_answer(
            core_answer: CoreAnswer,
            answers: list,
            request_id: str
    ):
        """Форматирование главного ответа"""

        # Выбор главного ответа
        core_answer.answer = answers[0]

        # Если главный ответ по кубам
        if isinstance(core_answer.answer, CubeAnswer):
            core_answer.status = True

            logging.info(
                "Query_ID: {}\tMessage: Главный ответ - "
                "ответ по кубу - {} - {}".format(
                    request_id,
                    core_answer.answer.get_score(),
                    core_answer.answer.mdx_query
                ))

            response = send_request_to_server(
                core_answer.answer.mdx_query,
                core_answer.answer.cube
            )

            # ответ с сервера
            value = process_server_response(core_answer.answer, response)

            # форматирование ответа при его наличии
            if value is not None:
                process_cube_answer(core_answer.answer, value)
        # Если главный ответ по минфину
        else:
            # фильтр по релевантности на минфин
            if answers[0].get_score() >= MODEL_CONFIG["relevant_minfin_main_answer_threshold"]:
                core_answer.status = True

                logging.info(
                    "Query_ID: {}\tMessage: Главный ответ - "
                    "ответ по Минфину - {} - {}".format(
                        request_id,
                        core_answer.answer.get_score(),
                        core_answer.answer.number
                    ))
            else:
                # Обнуление найденого ответа
                core_answer.answer = None

                logging.info(
                    "Query_ID: {}\tMessage: Главный ответ по Минфину "
                    "не прошел порог ({} vs {})".format(
                        request_id,
                        answers[0].get_score(),
                        MODEL_CONFIG["relevant_minfin_main_answer_threshold"]
                    ))

    @staticmethod
    def _process_more_answers(
            core_answer: CoreAnswer,
            more_answers: list,
            request_id: str
    ):
        """Обработка дополнительных ответов"""

        more_cube_answers = []
        more_minfin_answers = []

        more_answers_order = ''

        for ind, answer in enumerate(more_answers):
            answer.order = ind

        for answer in more_answers:
            if isinstance(answer, CubeAnswer):
                more_cube_answers.append(answer)
                more_answers_order += '0'
            else:
                more_minfin_answers.append(answer)
                more_answers_order += '1'

        if more_cube_answers:
            core_answer.more_cube_answers = more_cube_answers

        if more_minfin_answers:
            core_answer.more_minfin_answers = more_minfin_answers

        if more_answers_order:
            core_answer.more_answers_order = more_answers_order

        logging.info(
            "Query_ID: {}\tMessage: В смотри также {} "
            "ответ(а, ов) по кубам и {} по Минфину".format(
                request_id,
                len(more_cube_answers),
                len(more_minfin_answers)
            ))
