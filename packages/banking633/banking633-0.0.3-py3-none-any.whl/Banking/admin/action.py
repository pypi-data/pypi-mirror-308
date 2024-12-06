import time
import random
from .card import Card, User

class action(object):
    
    def __init__(self, allUser):
        self.allUser = allUser
        
   
    def createUser(self):
        try:
            name = input("Please enter your name:")
            idCard = input("Please enter your id: ")
            phone = input("Please enter your phone number")
            prestoreMoney = int(input("Please enter your prestore money:"))

            if prestoreMoney <= 0:
                raise ValueError("Prestore money must be greater than 0")

            firstPasswd = input("Please enter password:")
            secondPasswd = input("Please enter password again:")

            if firstPasswd != secondPasswd:
                raise ValueError("Passwords do not match")

            print("Password set, please remember it: %s" % secondPasswd)

            cardId = self.randomCardId()
            card = Card(cardId, secondPasswd, prestoreMoney)
            user = User(name, idCard, phone, card)

            # Save
            self.allUser[cardId] = user
            print("Create User Successfully! Please remember the card number...(%s)" % cardId)

        except ValueError as e:
            print("Error: {}".format(e))
            return -1


        
    
    def randomCardId(self):
        while True:
            str = ""
            for i in range(12):
                ch = chr(random.randrange(ord('0'), ord('9') + 1))
                str += ch
            if not self.allUser.get(str):
                return str
            
        
    def killUser(self):
        try:
            cardNum = input("Please enter card number:")

            if not cardNum.isnumeric():
                raise ValueError("Card number must be numeric")

            user = self.allUser.get(cardNum)
            if not user:
                raise ValueError("User does not exist")

            # Check password
            if not self.checkPasswd(user.card.cardPasswd):
                raise ValueError("Incorrect password")

            del self.allUser[cardNum]
            time.sleep(1)
            print("Remove the user successfully!")

        except ValueError as e:
            print("Error: {}".format(e))
            return -1
        

    def checkPasswd(self, realPasswd):
        try:
            tempPasswd = input("Please enter password: ")
            if tempPasswd == realPasswd:
                return True
            else:
                raise ValueError("Incorrect Password")
        except ValueError as e:
            
            print("Error: {}".format(e))
            return False
        except Exception as e:
            print("An unexpected error occurred: {}".format(e))
            return False
