import unittest
from admin.action import action 
from admin.card import Card, User
import time
import random
from unittest.mock import patch


class TestAction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Set up class")
        
    def setUp(self):
        print("Setting up for a test case")
        self.allUser = {}
        
    def tearDown(self):
        print("Tearing down after a test case")
        self.allUser = None
        
    @classmethod    
    def tearDownClass(cls):
        print("Tearing down the test class")

    def test_randomCardId(self):
        my_action = action(self.allUser)
        card_id = my_action.randomCardId()
        duplicate_card_id = my_action.randomCardId()
        
        self.assertEqual(len(card_id), 12)
        self.assertNotIn(card_id, my_action.allUser)
        self.assertTrue(card_id.isdigit())
        self.assertNotEqual(card_id, duplicate_card_id)

            
    def test_killUser(self):
        card_id = '123456789012'  
        user_data = {'name': 'Test User', 'idCard': '987654321', 'phone': '9876543210', 'card': Card(card_id, '5678', 500)}
        self.allUser[card_id] = User(**user_data)
        
        non_existent_card_id = '1111111111'

        with patch('builtins.input', side_effect=[card_id, '5678']):
            my_action = action(self.allUser)
            my_action.killUser()

            self.assertNotIn(card_id, self.allUser)
            self.assertEqual(len(self.allUser), 0)
            self.assertNotIn(non_existent_card_id, self.allUser)
            
            
        with patch('builtins.input', side_effect=[non_existent_card_id, '5678']):
            my_action = action(self.allUser)
            result = my_action.killUser()
            self.assertEqual(result, -1)

if __name__ == '__main__':
    unittest.main()