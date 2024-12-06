from admin.store import Store
from user.transaction import transaction


class UserView(Store):
    def __init__(self, run=True):
        super(UserView, self).__init__()
        self.transaction = transaction(self.users)
        if run:
            self.user_view()

    def menu(self):
        print("*************************************************")
        print("*    Balance（1）                                *")
        print("*    Withdraw（2）                               *")
        print("*    Deposit（3）                                *")
        print("*    Transfer（4）                               *")
        print("*    Quit（q）                                   *")
        print("*************************************************")

    def user_view(self):
        while True:
            self.menu()
            option = input("Please enter the process number：")
            if option == '1':
                self.transaction.balance()
            elif option == '2':
                self.transaction.withdraw()
            elif option == '3':
                self.transaction.deposit()
            elif option == '4':
                self.transaction.transfer()
            elif option == 'q':
                self.quit()
                break
            else:
                print('Invalid option. Please enter again...')
   
    def quit(self):
        print('Quiting...')
        self.save_all_data()



if __name__ == '__main__':
    UserView()

    