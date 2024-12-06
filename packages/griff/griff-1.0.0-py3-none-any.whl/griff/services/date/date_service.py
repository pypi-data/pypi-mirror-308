import datetime
from typing import Any, Optional, Union

import arrow
from injector import singleton

from griff.services.abstract_service import AbstractService
from griff.services.date.date_models import WDatetime


@singleton
class DateService(AbstractService):
    def __init__(self, locale="fr-fr"):
        self._locale = locale

    def now(self) -> WDatetime:
        return WDatetime(arrow.utcnow())

    def to_mysql_date(self, d: Union[WDatetime, Any] = None) -> str:
        return self._get(d).to_mysql_date()

    def to_mysql_datetime(self, d: Union[WDatetime, Any] = None) -> str:
        return self._get(d).to_mysql_datetime()

    def to_date(self, d: Union[WDatetime, Any] = None) -> datetime.date:
        return self._get(d).to_date()

    def to_datetime(self, d: Union[WDatetime, Any] = None) -> datetime.datetime:
        return self._get(d).to_datetime()

    def _get(self, d: Optional[WDatetime] = None):
        if d and isinstance(d, WDatetime) is False:
            # todo: fix couverture des tests manquantes à la prochaine modification
            raise ValueError("Invalid Datetime instance")
        return self.now() if d is None else d

    # todo: fix couverture des tests manquantes à la prochaine modification
    def _format(self, d: WDatetime, date_format) -> str:
        return d._value.to(self._timezone).format(date_format, locale=self._locale)
