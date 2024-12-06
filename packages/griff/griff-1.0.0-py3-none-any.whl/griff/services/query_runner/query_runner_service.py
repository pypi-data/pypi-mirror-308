import datetime
from pathlib import Path
from typing import List

import aiosql
from injector import inject
from loguru import logger

from griff.services.abstract_service import AbstractService
from griff.services.database.db_service import DbService
from griff.services.date.date_service import DateService
from griff.services.query_runner.query_runner_settings import QueryRunnerSettings


class QueryRunnerService(AbstractService):
    @inject
    def __init__(
        self,
        db_service: DbService,
        date_service: DateService,
        settings: QueryRunnerSettings,
    ):
        self._db_service = db_service
        self._date_service = date_service
        self._sql_queries = None
        self._settings = settings

    async def run_query(self, query_name, **query_params):
        query = self.check_query_exists(query_name)
        async with self._db_service.get_connection() as conn:
            try:
                sql = query.sql.replace("\n", " ")
                logger.debug(f"'{query_name}':SQL: {sql}\nparams : {query_params}")
                results = await query(conn=conn, **query_params)
                return self.format_results(results)
            except Exception as exec_exception:
                raise RuntimeError(str(exec_exception))

    async def run_many_query(self, query_name, queries_params: List[dict]):
        query = self.check_query_exists(query_name)
        async with self._db_service.get_connection() as conn:
            try:
                results = await query(conn, queries_params)
                return self.format_results(results)
            # todo: fix couverture des tests manquantes à la prochaine modification
            except Exception as exec_exception:  # pragma: no cover
                raise RuntimeError(str(exec_exception))

    def set_sql_queries(self, relative_sql_path: str) -> None:
        sql_path = Path(self._settings.project_dir).joinpath(relative_sql_path)
        self._sql_queries = aiosql.from_path(
            sql_path=str(sql_path), driver_adapter=self._db_service.get_driver()
        )

    def check_query_exists(self, query_name: str):
        try:
            return getattr(self._sql_queries, query_name)
        except AttributeError as e:
            raise RuntimeError(f"query '{query_name}' not found: {e}")

    # todo: fix couverture des tests manquantes à la prochaine modification
    def get_queries(self):  # pragma: no cover
        return self._sql_queries

    # todo: fix couverture des tests manquantes à la prochaine modification
    def result_to_tuple(self, results) -> tuple:  # pragma: no cover
        newresults = []
        for value in results:
            if isinstance(value, datetime.datetime):
                value = str(value.strftime("%Y-%m-%d %H:%M:%S"))
            newresults.append(value)
        return tuple(newresults)

    def result_to_dict(self, results) -> dict:
        res_as_dict = dict(results)
        newresults = {}
        for key, value in res_as_dict.items():
            if isinstance(value, datetime.datetime):
                value = str(value.strftime("%Y-%m-%d %H:%M:%S"))
            newresults[key] = value
        return newresults

    def result_to_dict_list(self, results) -> list:
        new_list = list()
        for res in results:
            new_list.append(self.result_to_dict(res))
        return new_list

    def format_results(self, results):
        if results is None:
            return None

        result_type = type(results)

        # todo: fix couverture des tests manquantes à la prochaine modification
        if result_type is list and len(results) == 0:  # pragma: no cover
            return None

        if result_type in [str, int, float, bool]:
            return results

        if result_type is self._db_service.get_provider().get_result_type():
            return self.result_to_dict(results)

        if result_type is list and type(
            results[0] is self._db_service.get_provider().get_result_type()
        ):
            return self.result_to_dict_list(results)

        # todo: fix couverture des tests manquantes à la prochaine modification
        return self.result_to_tuple(results)  # pragma: no cover
