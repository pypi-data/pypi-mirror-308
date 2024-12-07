import time


class AccountError(Exception):
    """Custom exception for account-related errors."""
    pass

class transaction:
    def __init__(self, allUser):
        self.allUser = allUser

    def _validate_account(self, cardNum):
        user = self.allUser.get(cardNum)
        if not user:
            raise AccountError("This account does not exist.")
        if user.card.cardLock:
            raise AccountError("This account is locked down.")
        return user

    def _check_password(self, realPasswd):
        for i in range(3):
            tempPasswd = input("Please enter your password: ")
            if tempPasswd == realPasswd:
                return True
        raise AccountError("Wrong password. Your account is locked down...")

    def balance(self):
        try:
            cardNum = input("Please enter your account number: ")
            user = self._validate_account(cardNum)
            if not self._check_password(user.card.cardPasswd):
                user.card.cardLock = True
                return
            print("Account number：%s  Account balance：%d" % (user.card.cardId, user.card.cardMoney))
        except AccountError as e:
            print(e)

    def withdraw(self):
        try:
            cardNum = input("Please enter your account number: ")
            user = self._validate_account(cardNum)
            self._check_password(user.card.cardPasswd)
            
            money = int(input("Please enter withdraw amount："))
            if money > user.card.cardMoney or money < 0:
                raise AccountError("Invalid amount. Withdrawal failed.")

            user.card.cardMoney -= money
            print("Withdraw success. Account balance: %d" % user.card.cardMoney)
        except AccountError as e:
            print(e)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def deposit(self):
        try:
            cardNum = input("Please enter your account number: ")
            user = self._validate_account(cardNum)
            self._check_password(user.card.cardPasswd)
            
            money = int(input("Please enter deposit amount："))
            if money < 0:
                raise AccountError("Invalid amount. Deposit failed.")

            user.card.cardMoney += money
            print("Deposit success: %d. Account balance: %d" % (money, user.card.cardMoney))
        except AccountError as e:
            print(e)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def transfer(self):
        try:
            cardNum = input("Please enter your account number: ")
            user = self._validate_account(cardNum)
            self._check_password(user.card.cardPasswd)

            money = int(input("Please enter transfer amount："))
            if money > user.card.cardMoney or money < 0:
                raise AccountError("Invalid amount. Transfer failed.")

            newcardNum = input("Please enter the recipient account number：")
            newcard = self._validate_account(newcardNum)

            user.card.cardMoney -= money
            newcard.card.cardMoney += money
            time.sleep(1)
            print("Transfer success")
            time.sleep(1)
            print("Transfer amount: %d. Account balance: %d" % (money, user.card.cardMoney))
        except AccountError as e:
            print(e)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def checkPasswd(self, realPasswd):
        for i in range(3):
            tempPasswd = input("Please enter your password: ")
            if tempPasswd == realPasswd:
                return True
        return False