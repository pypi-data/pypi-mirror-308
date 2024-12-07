import unittest
from admin.action import action 
from admin.card import Card, User
import time
import random
from unittest.mock import patch, Mock
from itertools import cycle

from admin.view import AdminView
from admin.store import Store


class TestAdminView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Set up class")
    
    @classmethod    
    def tearDownClass(cls):
        print("Tearing down the test class")
        
    def setUp(self):
        print("Setting up for a test case")
        self.allUser = {}
        self.action_instance = action(self.allUser)
        
        self.admin_view_instance = AdminView(run=False)
        
    def tearDown(self):
        print("Tearing down after a test case")
        self.allUser = None
        

    def test_createUser(self):
        with patch('builtins.input', side_effect=['John Doe', '123456789', '1234567890', '1000', '1234', '1234']):
            my_action = action(self.allUser)
            my_action.createUser()
            card_id = list(self.allUser.keys())[0]
            user = self.allUser[card_id]

            self.assertEqual(user.name, 'John Doe')
            self.assertEqual(user.idCard, '123456789')
            self.assertEqual(user.phone, '1234567890')
            self.assertEqual(user.card.cardMoney, 1000)
            self.assertEqual(user.card.cardPasswd, '1234')
            
    def test_checkPasswd(self):       
        real_password = '12345'

        with patch('builtins.input', return_value=real_password):
            result = self.action_instance.checkPasswd(real_password)
            self.assertTrue(result)

        # Test with incorrect password
        with patch('builtins.input', return_value='111111'):
            result = self.action_instance.checkPasswd(real_password)
            self.assertFalse(result)

        # Test with empty input
        with patch('builtins.input', return_value=''):
            result = self.action_instance.checkPasswd(real_password)
            self.assertFalse(result)

        # Test with multiple incorrect inputs followed by correct input
        with patch('builtins.input', side_effect=['wrong1', 'wrong2', 'wrong3', real_password]):
            result = self.action_instance.checkPasswd(real_password)
            self.assertFalse(result)
            
    def test_login_credentials(self):
        with patch('builtins.input', side_effect=['1', '1']):
            result = self.admin_view_instance.login()            
            self.assertTrue(result)           
            self.assertNotIn('1', self.admin_view_instance.users)
    
            
        with patch('builtins.input', side_effect=['1', '2']):
            result = self.admin_view_instance.login()            
            self.assertFalse(result)
            
        with patch('builtins.input', side_effect=['3', '2']):
            result = self.admin_view_instance.login()            
            self.assertFalse(result)
            
            
   
        

if __name__ == '__main__':
    unittest.main()