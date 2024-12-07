import unittest
from test_viewandaction import TestAdminView 
from test_action import TestAction
from test_account import TestAccount  
from test_transaction import TestTransaction
  

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAdminView))
    suite.addTest(unittest.makeSuite(TestAction))
    suite.addTest(unittest.makeSuite(TestAccount))
    suite.addTest(unittest.makeSuite(TestTransaction))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
