from admin.view import AdminView
from user.account import UserView
import time


class MainView:
    def __init__(self):
        self.admin = AdminView
        self.user = UserView
        self.choice_user_type()

    def run_admin(self):
        self.admin(False).admin_view()

    def run_user(self):
        self.user(False).user_view()

    def choice_user_type(self):
        print("*************************************************")
        print("*                                               *")
        print("*                                               *")
        print("*                  Welcome                      *")
        print("*                                               *")
        print("*                                               *")
        print("*************************************************")
        time.sleep(0.5)

        print('=================================================')
        print('Please select your role：')
        print('1. admin')
        print('2. user')
        print('=================================================')
        user = input('>')
        if user not in ('1', '2'):
            return
        if user == '1':
            self.run_admin()
        else:
            self.run_user()

def start_app():
    MainView()

if __name__ == '__main__':
    start_app()