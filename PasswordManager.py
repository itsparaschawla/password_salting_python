import random
import csv

class PasswordManager:
    def __init__(self):
        self.original_passwords = {}
        self.salted_passwords = {}

    def salt_password(self, password):
        length = len(password)
        mid = length // 2
        salt = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=5))
        salted_password = password[:mid] + salt + password[mid:]
        return salted_password

    def write_passwords_to_file(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password", "salted_password"])
            for variable, password in self.original_passwords.items():
                salted_password = self.salted_passwords.get(variable, "")
                writer.writerow([variable, password, salted_password])

    def read_passwords_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    variable = row["username"]
                    original_password = row["password"]
                    salted_password = row["salted_password"]
                    self.original_passwords[variable] = original_password
                    if salted_password:
                        self.salted_passwords[variable] = salted_password
        except FileNotFoundError:
            print("File not found. No salted passwords loaded.")

    def delete_password(self, variable_name, filename):
        if variable_name in self.original_passwords:
            del self.original_passwords[variable_name]
        else:
            print("No such user exists")
        if variable_name in self.salted_passwords:
            del self.salted_passwords[variable_name]
            print(f"Password for {variable_name} deleted.")
        else:
            print("No such user exists in salted passwords dataset")
        self.write_passwords_to_file(filename)

    def menu(self):
        while True:
            print("\nOptions:")
            print("1. Save a password \n2. Salt a password \n3. Show all passwords & Retrieve previously stored Data")
            print("4. Delete a password \n5. Exit\n")

            choice = input("Enter your choice (1/2/3/4/5): ")

            if choice == '1':
                print("\n")
                variable_name = input("Enter a Username: ")
                password = input("Enter a password: ")
                self.original_passwords[variable_name] = password
                do_salting = input("Do you want to add salt to this password? (yes/no): ")

                if do_salting.lower() == 'yes':
                    salted_password = self.salt_password(password)
                    self.salted_passwords[variable_name] = salted_password

                self.write_passwords_to_file('salted_passwords.csv')
                print("Password saved.")
                print()

            elif choice == '2':
                print("\n")
                variable_name = input("Enter the Username: ")
                if variable_name in self.original_passwords:
                    password = self.original_passwords[variable_name]
                    salted_password = self.salt_password(password)
                    self.salted_passwords[variable_name] = salted_password
                    self.write_passwords_to_file('salted_passwords.csv')
                    print("Password salted and updated.")
                    print()
                else:
                    print("Username not found.")
                    print()

            elif choice == '3':
                print("\n")
                self.read_passwords_from_file('salted_passwords.csv')
                print("Stored Passwords:")
                for variable, original_password in self.original_passwords.items():
                    print(f"Username: {variable}")
                    print(f"Original Password: {original_password}")
                    if variable in self.salted_passwords:
                        salted_password = self.salted_passwords[variable]
                        print(f"Salted Password: {salted_password}")
                    else:
                        print("No salted password.")
                    print()
                print()

            elif choice == '4':
                print("\n")
                variable_name = input("Enter the Username to delete: ")
                self.delete_password(variable_name, 'salted_passwords.csv')
                print()

            elif choice == '5':
                break
            else:
                print("Invalid option. Please select 1, 2, 3, 4, or 5.")
                print()

# Usage example
password_manager = PasswordManager()
password_manager.menu()
