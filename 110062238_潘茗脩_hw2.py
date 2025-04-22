import sys
import os

# Load initial money and records from 'records.txt'; if file is missing or corrupted, prompt user
def initialize():
    records = []
    try:
        with open("records.txt", "r") as f:
            # the records form should be like this:
            # 1000 (initial money)
            # breakfast -50 (record)
            # ...
            lines = f.readlines()
            try:
                amount = int(lines[0].strip())
                for line in lines[1:]:
                    parts = line.strip().split()
                    if len(parts) != 2:
                        raise ValueError("Record format error")
                    desc, amt = parts
                    amt = int(amt)
                    records.append((desc, str(amt)))
                print("Welcome back!")
            except (ValueError, IndexError):
                # If the first line is not a valid integer or if records are malformed, reset the records
                sys.stderr.write("Invalid format in records.txt. Deleting the contents.\n")
                records = []
                try:
                    amount = int(input("How much money do you have? "))
                except ValueError:
                    print("Invalid value for money. Set to 0 by default.")
                    amount = 0


    except FileNotFoundError:
        try:
            amount = int(input("How much money do you have? "))
            
        except ValueError:
            print("Invalid value for money. Set to 0 by default.")
            amount = 0
    return amount, records

# Prompt user to add records in the format 'desc amt' and append them to the list
def add(records):
    new_records = input("Add some expense or income records with description and amount: \ndesc1 amt1, desc2 amt2, desc3 amt3, ...\n")
    try:
        new_records = new_records.split(",")
        # used pared to store the records and check if the records are valid
        parsed = []
        for item in new_records:
            parts = item.strip().split()
            if len(parts) != 2:
                raise ValueError("The format of a record should be like this: breakfast -50.")
            desc, amt = parts
            # Check if the amount is valid, it should be int
            amt = int(amt)
            parsed.append((desc, str(amt)))
        records += parsed
    except ValueError as ve:
        sys.stderr.write(f"{ve}\nFail to add a record.\n")
    except Exception as e:
        sys.stderr.write(f"Unexpected error: {e}\n")
    return records

# Display all records and the current remaining money
def view(initial_money, records):
    print("Here's your expense and income records:")
    print("Index | Description | Amount")
    print("=" * 30)
    # print the index with 1-based index
    for i, record in enumerate(records):
        print(f"{i + 1:<5} | {record[0]:<11} | {record[1]:<6}")
    print("=" * 30)
    print(f"Now you have {initial_money + sum(int(r[1]) for r in records)} money left.")

# Ask user for index to delete a specific record from the list
def delete(records):
    try:
        # since the index is 1-based, we need to subtract 1 from the input
        index = int(input("Enter the index of the record you want to delete: ")) - 1
        if index < 0 or index >= len(records):
            raise IndexError("Index out of range")
        deleted_record = records.pop(index)
        print(f"Deleted record: {deleted_record}")
    except (ValueError, IndexError) as e:
        sys.stderr.write(f"Invalid index: {e}\n")
    return records

# Save current state (initial money and all records) to 'records.txt'
def save(initial_money, records):
    try:
        with open("records.txt", "w") as f:
            f.write(f"{initial_money}\n")
            f.writelines([f"{desc} {amt}\n" for desc, amt in records])
    except Exception as e:
        sys.stderr.write(f"Failed to save records: {e}\n")

# Main loop: receive and execute commands from user input
if __name__ == "__main__":
    initial_money, records = initialize()

    while True:
        command = input('\nWhat do you want to do (add / view / delete / exit)? ')
        if command == 'add':
            records = add(records)
        elif command == 'view':
            view(initial_money, records)
        elif command == 'delete':
            records = delete(records)
        elif command == 'exit':
            save(initial_money, records)
            print("Goodbye!")
            break
        else:
            sys.stderr.write('Invalid command. Try again.\n')