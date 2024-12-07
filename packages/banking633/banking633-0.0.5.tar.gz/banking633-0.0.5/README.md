# Introduction: 
[![Build Status](https://app.travis-ci.com/zhangz128/DATA533-project-step3-group20.svg?token=ZE7d4eqsfoF5iC5KRgDj&branch=main)](https://app.travis-ci.com/zhangz128/DATA533-project-step3-group20)

The `banking633` system is divided into 2 subpackage `Admin` with modules `view`, `action`, `card` and `User` with modules `account`, `transaction`. 
`main` is the main menu, `data.json` is for storing all action data though `store`.

# Running the Application
Execution: The application can be started by running main `import banking633` and `import banking633.main` directly, then select role depending on the desired mode (admin or user). 
We general "account: 1, password: 1" for admin, user should have account created at the first time.

## MainView Class
Purpose: Serves as the entry point for the application, allowing users to choose between admin and user modes.
Methods:
run_admin: Executes the admin view.
run_user: Executes the user view.
choice_user_type: Displays welcome message and lets users choose their role (admin or user).

# Admin
## Store Class
Purpose: Handles data storage and retrieval.
Attributes: data_file_path (path to the data file), users (dictionary of users).
Methods:
save_all_data: Saves all user data to a file.
read_users_from_file: Reads users from a file and converts them to User objects.

## action Class
Purpose: Handles user actions such as creating or removing users.
Methods:
createUser: Registers a new user after validating inputs.
randomCardId: Generates a unique card ID.
killUser: Deletes a user based on card number after validation.
checkPasswd: Validates a password.

## Card Class
Purpose: Represents a bank card.
Attributes: cardId, cardPasswd, cardMoney, cardLock.
Method: to_dict: Converts card attributes to a dictionary.

## User Class
-Purpose: Represents a user.
Attributes: name, idCard, phone, card.
Method: to_dict: Converts user attributes to a dictionary.


## AdminView Class (Inherits from Store)
Purpose: Provides the admin interface for managing users.
Methods:
quit: Saves data and exits.
login: Handles admin login.
admin_view: Displays admin options and handles user interactions.


# User
## UserView Class (Inherits from Store)
Purpose: Provides the user interface for banking transactions.
Methods:
menu: Displays the user menu.
user_view: Handles user interactions based on menu choices.
quit: Saves data and exits.

## transaction Class
Purpose: Handles banking transactions like balance check, withdrawal, deposit, and transfer.
Methods:
balance: Displays the user's current balance.
withdraw: Processes a withdrawal after validation.
deposit: Processes a deposit.
transfer: Handles fund transfers between accounts.
checkPasswd: Validates the password with a maximum of three attempts.


## Coverage Reports
![report](/Coverage_Reports.png)

NOTE: the lack of coverage for admin/view is UI code and for user/transaction is print statement

pypi: https://pypi.org/project/banking633/0.0.2/
