import shelve
import random
import os
from Config import Config


class Account:
    def __init__(self, identifier, username, password, other_info):
        self.identifier = identifier
        self.username = username
        self.password = password
        self.other_information = other_info


def create_account_identifier(account_type):
    # Creates a brand new unique account identifier
    new_identifier = ""
    if account_type in ["Member", 0]:
        new_identifier += "M"
    elif account_type in ["Staff", 1]:
        new_identifier += "S"
    elif account_type in ["Admin", 2]:
        new_identifier += "A"
    else:
        print("Unknown Account Type.")
        return False

    new_identifier += str(random.randint(0, 9))

    account_shelf = open_db()
    account_number = str(len(account_shelf["Account"].keys()) + 1)
    account_shelf.close()

    for _ in range(5 - len(account_number)):
        account_number = "0" + account_number
    new_identifier += account_number

    last_letter = 0
    for letter in new_identifier[1:]:
        last_letter += ord(letter)
    last_letter = last_letter % 25

    new_identifier += chr(last_letter + 65)
    return new_identifier


def new_account(username, password, account_type, other_information=[]):
    # Creates a new account
    identifier = create_account_identifier(account_type)
    if identifier is False:
        print("Account Creation Failed")
        return

    account_shelf = open_db()
    account_dic = account_shelf["Account"]
    account_dic[identifier] = [username, password, account_type, other_information]
    account_shelf["Account"] = account_dic
    account_shelf.close()

    return identifier


def new_account_by_class(username, password, account_type, other_information=[]):
    identifier = create_account_identifier(account_type)
    if identifier is False:
        print("Account Creation Failed")
        return
    account_shelf = open_db()
    account_dic = account_shelf["Account"]
    account_dic[identifier] = Account(identifier, username, password, other_information)
    account_shelf["Account"] = account_dic
    account_shelf.close()
    return identifier


def open_db():
    # Opens up the database. Creates a fresh file if not found.
    # Remember to close the database once you are done.
    all_storage = shelve.open(Config.STORAGE_PATH, "c")
    if "Account" not in all_storage:
        all_storage["Account"] = {}
    return all_storage


def account_info(identifier):
    # Returns an account's information
    # If not found, returns False
    account_shelf = open_db()
    if identifier in account_shelf["Account"]:
        info = account_shelf["Account"][identifier]
    else:
        info = False
    account_shelf.close()
    return info


def account_info_by_class(identifier):
    account_shelf = open_db()
    if identifier in account_shelf["Account"]:
        user_info = account_shelf["Account"][identifier]
        info = [user_info.username, user_info.password, user_info.other_information]
    else:
        info = False
    account_shelf.close()

    return info



def quick_identifier_check(identifier):
    # Random code I wrote just to make sure my code works.
    # Can be used to validate account identifiers quickly
    if len(identifier) != 8:
        return False
    last_letter = 0
    for letter in identifier[1:-1]:
        last_letter += int(ord(letter))
    last_letter = chr(last_letter % 25 + 65)
    if last_letter == identifier[-1]:
        return True
    else:
        return False


def wipe_test():
    # Erases the ENTIRE STORAGE.
    # Use with caution.
    with shelve.open(Config.STORAGE_PATH, flag='n'):
        pass


def main():
    # For testing purposes only.
    # Do not run this file for any other purpose other than testing.

    wipe_test()
    print(dict(open_db()))


if __name__ == "__main__":
    main()
