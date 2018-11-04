import unittest
from unittest.mock import patch

import dao.tasks
from main import app


class TaskLoadTestCase(unittest.TestCase):
    @patch('dao.utils.mysql')
    def test_task_not_found(self, mysql_connector):
        with app.app_context():
            mysql_connector.connect().cursor().fetchone.return_value = None
            Res = dao.tasks.load_one('some-non-existent-id')
            self.assertEqual(Res, None)


if __name__ == '__main__':
    unittest.main()
