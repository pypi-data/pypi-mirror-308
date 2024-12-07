from .store import Store
from .card import User, Card
from .action import action

import time 

#inheritance class
class AdminView(Store):

    def __init__(self, run=True):
        super(AdminView, self).__init__()
        self.action = action(self.users)
        if run:
            self.admin_view()

    def quit(self):
        print('Bye~')
        self.save_all_data()



    def login(self):
        _user = input('admin username: ')
        _password = input('admin password: ')

        if _user == '1' and _password == '1':
            print('Login successful!')
            # Check if the user is already in the dictionary
            
            return True
        else:
            print('Incorrect username or password!')
            self.users = None
            return False

              
    
    def admin_view(self):

        if not self.login():
            print('Password is wrong，Bye~')
            return

        while True:
            print("*************************************************")
            print("*             Create User（1）                   *")
            print("*          Deactivate User（0）                  *")
            print("*                 Exit（q）                      *")
            print("*************************************************")
            option = input("Please enter your option:")
            if option == "1":  
                self.action.createUser()
            elif option == "0":
                self.action.killUser()
            elif option == "q":
                self.quit()
                break
            else:
                raise ValueError("Invalid option provided")
                


if __name__ == '__main__':
    AdminView()

    
    