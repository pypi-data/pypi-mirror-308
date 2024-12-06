from griff.tests_utils.testcases.abstract_testcase import AbstractTestCase


# noinspection PyMethodMayBeStatic
class ModelTestCase(AbstractTestCase):
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

    def assert_comparing_failed(self, model, model_greater, model_same):
        assert (model == model_greater) is False, "== failed"
        assert (model != model_same) is False, "!= failed"
        assert (model > model_greater) is False, "> failed"
        assert (model_greater < model) is False, "< failed"
        assert (model >= model_greater) is False, ">=  failed"
        assert (model_greater <= model) is False, "<=  failed"

    def assert_comparing_succeed(self, model, model_greater, model_same):
        assert model == model_same, "== failed"
        assert model != model_greater, "!= failed"
        assert model_greater > model, "> failed"
        assert model < model_greater, "< failed"
        assert model_greater >= model, ">=  failed"
        assert model_same >= model, ">=  failed"
        assert model <= model_greater, "<=  failed"
        assert model <= model_same, "<=  failed"

    def assert_copy(self, model):
        copy = model.copy()
        assert copy is not model
        assert copy == model
