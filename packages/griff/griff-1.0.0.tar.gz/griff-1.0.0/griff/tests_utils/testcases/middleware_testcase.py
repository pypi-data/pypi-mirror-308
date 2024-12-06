from griff.tests_utils.testcases.abstract_testcase import AbstractTestCase


class MiddlewareTestCase(AbstractTestCase):
    @classmethod
    def init_class_context_data(cls):
        pass

    @classmethod
    def init_class_context_services(cls):
        pass

    def init_method_context_data(self):
        pass

    def init_method_context_services(self):
        pass
