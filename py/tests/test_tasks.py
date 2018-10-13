import unittest
from unittest.mock import patch
from werkzeug.exceptions import HTTPException

import ctl.tasks
from app import app


class TasksViewTestCase(unittest.TestCase):
    @patch('dao.utils.mysql')
    def test_connect_to_database(self, mysql_connector):
        with app.app_context():
            mysql_connector.connect().cursor().fetchone.return_value = None
            with self.assertRaises(HTTPException) as http_error:
                ctl.tasks.task_view('')
                self.assertEqual(http_error.exception.code, 404)


if __name__ == '__main__':
    unittest.main()
