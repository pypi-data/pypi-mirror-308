import threading


class ThreadMixin:
    _lock: threading.Lock = threading.Lock()

    @staticmethod
    def current_thread_id():
        return threading.current_thread().ident

    @staticmethod
    def list_active_thread_ids():
        return [t.ident for t in threading.enumerate()]  # pragma: no cover
