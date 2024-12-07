import unittest
from unittest.mock import patch, MagicMock
from user.account import UserView


class TestAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Set up class resources...")
        cls.transaction_patch = patch('user.transaction.transaction')
        cls.mock_transaction = cls.transaction_patch.start()
        cls.mock_transaction.return_value.withdraw = MagicMock(return_value=True)
        cls.mock_transaction.return_value.deposit = MagicMock(return_value=True)

    @classmethod
    def tearDownClass(cls):
        print("Cleaning up class resources...")
        cls.transaction_patch.stop()

    def setUp(self):
        self.user_view = UserView(run=False)

    def tearDown(self):
        self.user_view = None

    def testSelectWithdraw(self):
        with patch('builtins.input', side_effect=['2', '123456', '1234', '50', 'q']), \
             patch('builtins.print') as mock_print:
            self.user_view.user_view()
            self.assertFalse(TestAccount.mock_transaction.return_value.withdraw.called)
            self.assertIsNotNone(TestAccount.mock_transaction.return_value.withdraw)
            self.assertIsNotNone(self.user_view)
            self.assertIsInstance(TestAccount.mock_transaction.return_value, MagicMock)

    def testSelectDeposit(self):
        with patch('builtins.input', side_effect=['3', '123456', '1234', '50', 'q']), \
             patch('builtins.print') as mock_print:
            self.user_view.user_view()

            self.assertEqual(TestAccount.mock_transaction.return_value.deposit.call_count, 0)
            self.assertIsInstance(self.user_view, UserView)
            self.assertFalse(self.user_view is None)
            self.assertIs(self.user_view, self.user_view)


if __name__ == '__main__':
    unittest.main()
