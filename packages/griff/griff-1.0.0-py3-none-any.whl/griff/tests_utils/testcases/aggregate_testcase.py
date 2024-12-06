from griff.services.uuid.fake_uuid_service import FakeUuidService
from griff.tests_utils.testcases.abstract_testcase import AbstractTestCase


class AggregateTestCase(AbstractTestCase):
    uuid_service: FakeUuidService = None

    @classmethod
    def init_class_context_data(cls):
        pass

    @classmethod
    def init_class_context_services(cls):
        cls.uuid_service = FakeUuidService(100)

    def init_method_context_data(self):
        pass

    def init_method_context_services(self):
        self.uuid_service.reset()
