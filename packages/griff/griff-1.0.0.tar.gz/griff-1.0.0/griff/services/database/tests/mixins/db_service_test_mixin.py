import threading

import pytest

from griff.tests_utils.mixins.async_test_mixin import AsyncTestMixin
from griff.tests_utils.mixins.db_test_mixin import DbTestMixin


class DbServiceTestMixin(AsyncTestMixin, DbTestMixin):
    async def async_setup(self):
        return await super().async_setup()

    async def test_start_transaction_with_success_return_none(self):
        await self._db_service.start_transaction()
        local_thread_id = threading.current_thread().ident
        assert local_thread_id in self._db_service._connection.keys()
        conn = self._db_service._connection[local_thread_id]
        assert conn is not None
        assert str(type(conn)) == "<class 'aiosqlite.core.Connection'>"
        assert conn.isolation_level == ""
        await self._db_service.release_connection()
        await self.async_teardown()

    @pytest.mark.skip
    async def test_start_and_rollback_transaction_handle_connection_with_success(self):
        await self._db_service.start_transaction()
        await self._db_service.rollback_transaction()
        local_thread_id = threading.current_thread().ident
        assert local_thread_id not in self._db_service._connection.keys()
        await self.async_teardown()

    @pytest.mark.skip
    async def test_start_and_commit_transaction_handle_connection_with_success(self):
        await self._db_service.start_transaction()
        await self._db_service.commit_transaction()
        local_thread_id = threading.current_thread().ident
        assert local_thread_id not in self._db_service._connection.keys()
        await self.async_teardown()

    @pytest.mark.skip
    async def test_try_to_run_query_with_sucess(self):
        await self.assert_test_table_is_empty()
        await self._db_service.start_transaction()
        # insert test data on work connection
        await self._test_queries.insert_test_data(
            await self._db_service.get_managed_connection()
        )
        # table should be filled on work connection
        await self.assert_datatable_is_filled()
        # table should be empty on test connection
        await self.assert_test_table_is_empty_using_connection(self._test_connection)
        await self._db_service.rollback_transaction(auto_close_connection=False)
        # and now table should be empty on work connection
        await self.assert_test_table_is_empty_using_connection(
            await self._db_service.get_managed_connection()
        )
        await self._db_service.release_connection()
        await self.async_teardown()

    @pytest.mark.skip
    async def test_final_cleanup(self):
        await self._db_service.start_transaction()
        await self._db_service.cleanup()
        assert len(self._db_service._connection) == 0
        await self.async_teardown()
