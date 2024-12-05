import argparse
import logging
import random
import time
from collections import defaultdict
from os import getenv
from typing import TextIO, Tuple

from ..api import ApiClient, ApiError, BadRequest
from ..main import BaseOperation
from ..main import Namespace as BaseNamespace
from ..telemetry_client import TelemetryError
from ..telemetry_client import get_client as get_telemetry_client
from ..types import ApiListResponse, VacancyItem
from ..utils import fix_datetime, print_err, truncate_string

logger = logging.getLogger(__package__)


class Namespace(BaseNamespace):
    resume_id: str | None
    message_list: TextIO
    force_message: bool
    apply_interval: Tuple[float, float]
    page_interval: Tuple[float, float]


class Operation(BaseOperation):
    """Откликнуться на все подходящие вакансии"""

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--resume-id", help="Идентефикатор резюме")
        parser.add_argument(
            "--message-list",
            help="Путь до файла, где хранятся сообщения для отклика на вакансии. Каждое сообщение — с новой строки. В сообщения можно использовать плейсхолдеры типа %%(name)s",
            type=argparse.FileType(),
        )
        parser.add_argument(
            "--force-message",
            help="Всегда отправлять сообщение при отклике",
            default=False,
            action=argparse.BooleanOptionalAction,
        )
        parser.add_argument(
            "--apply-interval",
            help="Интервал между отправкой откликов в секундах (X, X-Y)",
            default="1-5",
            type=self._parse_interval,
        )
        parser.add_argument(
            "--page-interval",
            help="Интервал между получением следующей страницы рекомендованных вакансий в секундах (X, X-Y)",
            default="1-3",
            type=self._parse_interval,
        )

    @staticmethod
    def _parse_interval(interval: str) -> Tuple[float, float]:
        """Парсит строку интервала и возвращает кортеж с минимальным и максимальным значениями."""
        if "-" in interval:
            min_interval, max_interval = map(float, interval.split("-"))
        else:
            min_interval = max_interval = float(interval)
        return min(min_interval, max_interval), max(min_interval, max_interval)

    def run(self, args: Namespace) -> None:
        assert args.config["token"]
        api = ApiClient(
            access_token=args.config["token"]["access_token"],
            user_agent=args.config["user_agent"],
        )
        resume_id = self._get_resume_id(args, api)
        application_messages = self._get_application_messages(args)

        apply_min_interval, apply_max_interval = args.apply_interval
        page_min_interval, page_max_interval = args.page_interval

        self._apply_similar(
            api,
            resume_id,
            args.force_message,
            application_messages,
            apply_min_interval,
            apply_max_interval,
            page_min_interval,
            page_max_interval,
        )

    def _get_resume_id(self, args: Namespace, api: ApiClient) -> str:
        if not (
            resume_id := args.resume_id or args.config["default_resume_id"]
        ):
            resumes: ApiListResponse = api.get("/resumes/mine")
            resume_id = resumes["items"][0]["id"]
        return resume_id

    def _get_application_messages(self, args: Namespace) -> list[str]:
        if args.message_list:
            application_messages = list(
                filter(None, map(str.strip, args.message_list))
            )
        else:
            application_messages = [
                "Меня заинтересовала ваша вакансия %(name)s",
                "Прошу рассмотреть мою жалкую кандидатуру на вакансию %(name)s",
                "Ваша вакансия %(name)s соответствует моим навыкам и опыту",
                "Хочу присоединиться к вашей успешной команде лидеров рынка в качестве %(name)s",
                "Мое резюме содержит все баззворды, указанные в вашей вакансии %(name)s",
            ]
        return application_messages

    def _apply_similar(
        self,
        api: ApiClient,
        resume_id: str,
        force_message: bool,
        application_messages: list[str],
        apply_min_interval: float,
        apply_max_interval: float,
        page_min_interval: float,
        page_max_interval: float,
    ) -> None:
        telemetry_client = get_telemetry_client()
        telemetry_data = defaultdict(dict)

        vacancies = self._get_vacancies(
            api, resume_id, page_min_interval, page_max_interval, per_page=100
        )

        self._collect_vacancy_telemetry(telemetry_data, vacancies)

        for vacancy in vacancies:
            try:
                if getenv("TEST_TELEMETRY"):
                    break

                if vacancy.get("has_test"):
                    print("🚫 Пропускаем тест", vacancy["alternate_url"])
                    continue

                relations = vacancy.get("relations", [])

                if relations:
                    print(
                        "🚫 Пропускаем ответ на заявку",
                        vacancy["alternate_url"],
                    )
                    continue

                try:
                    employer_id = vacancy["employer"]["id"]
                except IndexError:
                    logger.warning(
                        f"Вакансия без работодателя: {vacancy['alternate_url']}"
                    )
                else:
                    employer = api.get(f"/employers/{employer_id}")

                    telemetry_data["employers"][employer_id] = {
                        "name": employer.get("name"),
                        "type": employer.get("type"),
                        "description": employer.get("description"),
                        "site_url": employer.get("site_url"),
                        "area": employer.get("area", {}).get("name"),  # город
                    }

                # Задержка перед отправкой отклика
                interval = random.uniform(
                    apply_min_interval, apply_max_interval
                )
                time.sleep(interval)

                params = {
                    "resume_id": resume_id,
                    "vacancy_id": vacancy["id"],
                    "message": (
                        random.choice(application_messages) % vacancy
                        if force_message or vacancy["response_letter_required"]
                        else ""
                    ),
                }

                res = api.post("/negotiations", params)
                assert res == {}
                print(
                    "📨 Отправили отклик",
                    vacancy["alternate_url"],
                    "(",
                    truncate_string(vacancy["name"]),
                    ")",
                )
            except ApiError as ex:
                print_err("❗ Ошибка:", ex)
                if isinstance(ex, BadRequest) and ex.limit_exceeded:
                    break

        print("📝 Отклики на вакансии разосланы!")

        self._send_telemetry(telemetry_client, telemetry_data)

    def _get_vacancies(
        self,
        api: ApiClient,
        resume_id: str,
        page_min_interval: float,
        page_max_interval: float,
        per_page: int,
    ) -> list[VacancyItem]:
        rv = []
        for page in range(20):
            res: ApiListResponse = api.get(
                f"/resumes/{resume_id}/similar_vacancies",
                page=page,
                per_page=per_page,
                order_by="relevance",
            )
            rv.extend(res["items"])

            if getenv("TEST_TELEMETRY"):
                break

            if page >= res["pages"] - 1:
                break

            # Задержка перед получением следующей страницы
            if page > 0:
                interval = random.uniform(page_min_interval, page_max_interval)
                time.sleep(interval)

        return rv

    def _collect_vacancy_telemetry(
        self, telemetry_data: defaultdict, vacancies: list[VacancyItem]
    ) -> None:
        for vacancy in vacancies:
            vacancy_id = vacancy["id"]
            telemetry_data["vacancies"][vacancy_id] = {
                "name": vacancy.get("name"),
                "type": vacancy.get("type", {}).get("id"),  # open/closed
                "area": vacancy.get("area", {}).get("name"),  # город
                "salary": vacancy.get("salary"),  # from, to, currency, gross
                "direct_url": vacancy.get(
                    "alternate_url"
                ),  # ссылка на вакансию
                "created_at": fix_datetime(
                    vacancy.get("created_at")
                ),  # будем вычислять говно-вакансии, которые по полгода висят
                "published_at": fix_datetime(vacancy.get("published_at")),
                "contacts": vacancy.get(
                    "contacts"
                ),  # пиздорванки там телеграм для связи указывают
                # HH с точки зрения перфикциониста — кусок говна, где кривые
                # форматы даты, у вакансий может не быть работодателя...
                "employer_id": int(vacancy["employer"]["id"])
                if "employer" in vacancy and "id" in vacancy["employer"]
                else None,
                # Остальное неинтересно
            }

    def _send_telemetry(
        self, telemetry_client, telemetry_data: defaultdict
    ) -> None:
        try:
            res = telemetry_client.send_telemetry(
                "/collect", dict(telemetry_data)
            )
            logger.debug(res)
        except TelemetryError as ex:
            logger.error(ex)
