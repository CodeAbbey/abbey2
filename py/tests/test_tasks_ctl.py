import unittest
from unittest.mock import patch
from werkzeug.exceptions import HTTPException

import ctl.tasks
from main import app


class TasksViewTestCase(unittest.TestCase):
    @patch('dao.tasks')
    def test_task_not_found(self, tasks_dao):
        with app.app_context():
            tasks_dao.load_one.return_value = None
            with self.assertRaises(HTTPException) as http_error:
                ctl.tasks.task_view('none-1')
                self.assertEqual(http_error.exception.code, 404)


if __name__ == '__main__':
    unittest.main()
