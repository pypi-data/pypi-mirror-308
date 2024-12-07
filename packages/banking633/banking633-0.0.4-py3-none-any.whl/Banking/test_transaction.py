import unittest
from unittest.mock import patch
from user.transaction import transaction
from admin.card import Card
from admin.card import User
import time

test_card = Card('123456', '1234', 100)
test_user = User('Test User', '1234567890', '555-5555', test_card)
test_users = {'123456': test_user}

class TestTransaction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_card = Card('123456', '1234', 100)
        cls.test_user = User('Test User', '1234567890', '555-5555', cls.test_card)
        cls.test_users = {'123456': cls.test_user}
        print("Set up class resources...")

    @classmethod
    def tearDownClass(cls):
        print("Cleaning up class resources...")

    def setUp(self):
        self.allUser = TestTransaction.test_users.copy()
        self.transaction = transaction(self.allUser)

    def tearDown(self):
        TestTransaction.test_user.card.cardMoney = 100
        TestTransaction.test_user.card.cardLock = False
        self.allUser = None

    def testDeposit(self):
        with patch('builtins.input', side_effect=['123456', '1234', '-50']):
            self.transaction.deposit()
            self.assertEqual(TestTransaction.test_user.card.cardMoney, 100)
            self.assertIsNotNone(TestTransaction.test_user)
            self.assertIsNotNone(TestTransaction.test_user.card)
            self.assertFalse(TestTransaction.test_user.card.cardLock)
    
    def testWithdraw(self):
        with patch('builtins.input', side_effect=['123456', '1234', '50']):
            self.transaction.withdraw()
            self.assertEqual(TestTransaction.test_user.card.cardMoney, 50)
            self.assertIsNotNone(TestTransaction.test_user)
            self.assertIsNotNone(TestTransaction.test_user.card)
            self.assertFalse(TestTransaction.test_user.card.cardLock)

    def testTransfer(self):
        recipient_card = Card('654321', '4321', 200)
        recipient_user = User('Recipient User', '0987654321', '555-5556', recipient_card)
        self.allUser['654321'] = recipient_user
        
        with patch('builtins.input', side_effect=['123456', '1234', '50', '654321']):
            self.transaction.transfer()
            self.assertEqual(TestTransaction.test_user.card.cardMoney, 50)
            self.assertEqual(recipient_user.card.cardMoney, 250)
            self.assertIsNotNone(recipient_user)
            self.assertIsNotNone(recipient_user.card)
            self.assertFalse(recipient_user.card.cardLock)

    def testBalance_cardlocked(self):
        TestTransaction.test_user.card.cardLock = True
        with patch('builtins.input', side_effect=['123456']):
            balance = self.transaction.balance()
            self.assertTrue(TestTransaction.test_user.card.cardLock)
            self.assertIsNotNone(TestTransaction.test_user.card.cardId)
            self.assertIsNotNone(TestTransaction.test_user.card)

    def testBalance_incorpasswrd(self):
        with patch('builtins.input', side_effect=['123456', 'wrong_password', 'wrong_password', 'wrong_password']):
            balance = self.transaction.balance()
            self.assertIsNotNone(TestTransaction.test_user.card.cardId)
            self.assertIsNotNone(TestTransaction.test_user.card)

    @patch('builtins.input', side_effect=['123456', '1234', '50', 'nonexistent'])
    def testTransfer_nonextAcct(self, mock_inputs):
        self.transaction.transfer()
        self.assertEqual(TestTransaction.test_user.card.cardMoney, 100)

    @patch('builtins.input', side_effect=['123456', '1234', '50', '654321'])
    def testTransfer_locked(self, mock_inputs):
        recipient_card = Card('654321', '4321', 200)
        recipient_user = User('Recipient User', '0987654321', '555-5556', recipient_card)
        recipient_user.card.cardLock = True
        TestTransaction.test_users['654321'] = recipient_user
        self.transaction.transfer()
        self.assertEqual(TestTransaction.test_user.card.cardMoney, 100)
        
    @patch('builtins.input', side_effect=['123456', '1234', '200'])
    def testWithdraw_excbal(self, mock_inputs):
        self.transaction.withdraw()
        self.assertEqual(TestTransaction.test_user.card.cardMoney, 100)

    @patch('builtins.input', side_effect=['123456', '1234', '-50'])
    def testWithdraw_neg(self, mock_inputs):
        self.transaction.withdraw()
        self.assertEqual(TestTransaction.test_user.card.cardMoney, 100)   

if __name__ == '__main__':
    unittest.main()