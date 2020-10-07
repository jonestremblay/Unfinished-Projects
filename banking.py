import math
import random
import sqlite3

# Connect to database and create a cursor instance.
conn = sqlite3.connect("card.s3db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS card (
        id INTEGER ,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
         )""")
conn.commit()


def remove_symbols_from_string(fetch) -> str:
    """
    Convert the fetch into a string, then removes symbols   [ ] ( ) ,    from the string.
    """
    string = str(fetch)
    for z in ("[", ""), ("]", ""), ("(", ""), (")", ""), (",", ""):
        string = string.replace(*z)
    return string


def gen_acc_number() -> str:
    acc_num = ""
    while len(acc_num) < 9:
        acc_num += str(random.randint(0, 9))
    return acc_num


def gen_pin_code() -> str:
    pin_code = ""
    while len(pin_code) < 4:
        pin_code += str(random.randint(0, 9))
    return pin_code


def gen_check_digit() -> str:
    """
    Luhn's algorithm: all numbers % 10 == 0
    so sum of all numbers of the card number - without check digit - (sum)
    (sum + x) % 10 == 0
    """
    count_list = list(iin_bin) + list(acc_number)
    int_count_list = [int(i) for i in count_list]
    new_list = []

    for a in range(0, len(int_count_list), 2):
        new_list.append(int_count_list[a] * 2)
    for b in range(1, len(int_count_list), 2):
        new_list.append(int_count_list[b])
    c = 0
    for i in new_list:
        if i > 9:
            c += 9
    int_sum = sum(new_list) - c
    poss_check_digits = []
    for x in range(10):
        if (int_sum + x) % 10 == 0:
            # poss_check_digits.append(x)
            check_digit = str(x)
    # check_digit = str(random.choice(poss_check_digits))
    return check_digit


class CardNumber:

    def __init__(self, _bin, _acc_number, _pin_code):
        self.bin = _bin
        self.acc_number = _acc_number
        self.pin_code = _pin_code
        self.card_number_no_check_digit = self.bin + self.acc_number
        self.balance = 0


iin_bin = "400000"
acc_number = ""
check_sum = ""
card_number = ""
card_pin = ""
choice = -1
while choice != 0:
    choice = input("1. Create an account\n"
                   "2. Log into account\n"
                   "3. View all accounts\n"
                   "0. Exit\n")
    if choice == "1":
        acc_number = gen_acc_number()
        check_sum = gen_check_digit()
        card_number = iin_bin + acc_number + check_sum
        card_pin = gen_pin_code()
        print("\nYour card has been created\n"
              "Your card number:\n" +
              card_number + "\n"
                            "Your card PIN:\n" +
              card_pin + "\n")
        card = (iin_bin, acc_number + check_sum, card_pin, "0")
        c.execute("INSERT INTO card (id, number, pin, balance) VALUES (?, ?, ?, ?)", card)
        conn.commit()
        print("New card added to the card\'s database.")
        print("BIN: " + card[0] + " Acc_#: " + card[1] + "\n"
              "PIN: " + card[2] + "   Balance: " + card[3] + "\n")
        continue
    elif choice == "2":
        # Log into acc
        log_in = False
        user = (input("Enter you card number:\n"),)
        pin = (input("Enter your PIN:\n"),)
        u = (user[0][6:],)
        p = pin[0]
        c.execute("SELECT number FROM card WHERE number == ? ", u[0])
        user_fetch = c.fetchone()
        user_data = remove_symbols_from_string(user_fetch)
        c.execute("SELECT pin FROM card WHERE number == ? ", u[0])
        pin_fetch = c.fetchone()
        pin_data = remove_symbols_from_string(pin_fetch)
        # print(user)
        # print(pin)
        # print(u)
        # print(p)
        # print(user[0][6:])
        # print(pin[0])
        # print(user_fetch)
        # print(user_data)
        # print(pin_fetch)
        # print(pin_data)
        # user[6:]: slice the BIN (400000) from the input, to compare only acc_number, not card number.
        if user[0][6:] == user_data and p == pin_data:     # THE PROBLEM IS HERE MY FRIEND. IT'S COMPARING EMPTY VARIABLES.
            print("\nYou have successfully logged in!")
            log_in = True
            while log_in:
                menu = input("\n1. Balance\n"
                             "2. Add income\n"
                             "3. Do transfer\n"
                             "4. Close account\n"
                             "5. Log out\n"
                             "0. Exit\n")
                if menu == "1":
                    # Balance
                    acc = (acc_number,)
                    # c.execute("SELECT balance FROM card WHERE number=? ", acc)
                    # balance = c.fetchone()
                    k = c.execute("SELECT balance FROM card WHERE number == ? ", acc)
                    for i in k:
                        print("\nBalance: ", i)
                    continue
                elif menu == "2":
                    # Add income
                    income = (input("Enter income:\n"),)
                    c.execute("UPDATE card SET balance=?", income)
                    conn.commit()
                    print("Income was added!")
                    continue
                elif menu == "3":

                    # Do transfers
                    pass
                elif menu == "4":
                    # Close account
                    pass
                elif menu == "5":
                    # Log out
                    print("\nYou have successfully logged out!\n")
                    log_in = False
                elif menu == "0":
                    print("\nBye!")
                    conn.close()
                    exit()
                else:
                    print("Incorrect parameter.")
                    continue
        else:
            print("\nWrong card number or PIN!\n")
            continue
    elif choice == "3":
        c.execute("SELECT * FROM card")
        data = c.fetchall()
        for i in data: print(i)

        print("TEST ----------------------")
        user = (input("Enter you card number:\n"),)
        pin = (input("Enter your PIN:\n"),)
        u = (user[0][6:],)
        p = pin[0]
        c.execute("SELECT number FROM card WHERE number == ? ", u[0])
        user_fetch = c.fetchone()
        user_data = remove_symbols_from_string(user_fetch)
        c.execute("SELECT pin FROM card WHERE number == ? ", u[0])
        pin_fetch = c.fetchone()
        pin_data = remove_symbols_from_string(pin_fetch)
        print(user)
        print(pin)
        print(u)
        print(p)
        print(u[0])
        print(user[0][6:])
        print(pin[0])
        print(user_fetch)
        print(user_data)
        print(pin_fetch)
        print(pin_data)
    elif choice == "0":
        # Exit
        print("Bye!")
        conn.commit()
        conn.close()
        exit()
    else:
        print("Incorrect parameter.")
        conn.close()
        exit()

for


defv 
