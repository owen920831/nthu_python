import sys

class Record:
    """Represent a record with category, description, and amount."""
    def __init__(self, category, description, amount):
        self._category = category
        self._description = description
        self._amount = amount

    @property
    def category(self):
        return self._category

    @property
    def description(self):
        return self._description

    @property
    def amount(self):
        return self._amount

    def __str__(self):
        return f"{self._category} {self._description} {self._amount}"

class Categories:
    """Maintain nested category list and operations."""
    def __init__(self):
        """Initialize default categories."""
        self._categories = [
            'expense',
                ['food', \
                    ['meal', 'snack', 'drink'], \
                'transportation', \
                    ['bus', 'railway']\
                ], \
            'income', \
                ['salary', 'bonus']
        ]

    def view(self, categories=None, indent=0):
        """Recursively print all categories hierarchically."""
        if categories is None:
            categories = self._categories
        if not isinstance(categories, list):
            print("  " * indent + f"- {categories}")
        else:
            for item in categories:
                if isinstance(item, list):
                    self.view(item, indent + 1)
                else:
                    print("  " * indent + f"- {item}")

    def is_category_valid(self, category, categories=None):
        """Recursively check if a category exists."""
        if categories is None:
            categories = self._categories
        if isinstance(categories, list):
            for item in categories:
                if self.is_category_valid(category, item):
                    return True
            return False
        else:
            return categories == category

    def find_subcategories(self, category):
        """Return a flat list of the specified category and all its subcategories."""
        def find_subcategories_gen(category, cats, found=False):
            if isinstance(cats, list):
                for idx, child in enumerate(cats):
                    yield from find_subcategories_gen(category, child, found or child == category)
                    if child == category and idx + 1 < len(cats) and isinstance(cats[idx + 1], list):
                        yield from find_subcategories_gen(category, cats[idx + 1], True)
            else:
                if cats == category or found:
                    yield cats

        return list(find_subcategories_gen(category, self._categories))

class Records:
    """Maintain a list of Record instances and the initial money."""
    def __init__(self):
        """
        Initialize records from 'records.txt' if valid, otherwise prompt for initial money.
        """
        self._records = []
        try:
            with open("records.txt", "r") as f:
                lines = f.readlines()
            self._initial_money = int(lines[0].strip())
            for line in lines[1:]:
                parts = line.strip().split()
                if len(parts) != 3:
                    continue
                cat, desc, amt = parts[0], parts[1], int(parts[2])
                self._records.append(Record(cat, desc, amt))
            print("Welcome back!")
        except Exception:
            try:
                self._initial_money = int(input("How much money do you have? "))
            except ValueError:
                print("Invalid value for money. Set to 0 by default.")
                self._initial_money = 0

    def add(self, input_str, categories):
        """Add records from a comma-separated input string 'cat desc amt, ...'."""
        entries = input_str.split(",")
        for item in entries:
            parts = item.strip().split()
            if len(parts) != 3:
                print("The format of a record should be: category description amount.")
                return
            cat, desc, amt_str = parts
            try:
                amt = int(amt_str)
            except ValueError:
                print("Invalid amount.")
                return
            if not categories.is_category_valid(cat):
                print("The specified category is not in the category list.")
                print('You can check the category list by command "view categories".')
                return
            self._records.append(Record(cat, desc, amt))

    def view(self):
        """Display all records and the current balance."""
        print("Here's your expense and income records:")
        print(f"{'Index':<6}{'Category':<15}{'Description':<20}{'Amount':<10}")
        print("=" * 55)
        for i, rec in enumerate(self._records, start=1):
            print(f"{i:<6}{rec.category:<15}{rec.description:<20}{rec.amount:<10}")
        print("=" * 55)
        total = self._initial_money + sum(r.amount for r in self._records)
        print(f"Now you have {total} dollars.")

    def delete(self, index_str):
        """Delete a record by its 1-based index."""
        try:
            idx = int(index_str) - 1
            if idx < 0 or idx >= len(self._records):
                raise IndexError
            rec = self._records.pop(idx)
            print(f"Deleted record: {rec.category} {rec.description} {rec.amount}")
        except Exception:
            print("Invalid index.")

    def find(self, category_list):
        """Display records whose category is in category_list and report their total."""
        filtered = [r for r in self._records if r.category in category_list]
        print("Here's your records under specified categories:")
        print(f"{'Category':<15}{'Description':<20}{'Amount':<10}")
        print("=" * 45)
        for rec in filtered:
            print(f"{rec.category:<15}{rec.description:<20}{rec.amount:<10}")
        print("=" * 45)
        total = sum(r.amount for r in filtered)
        print(f"The total amount above is {total}.")

    def save(self):
        """Save initial money and all records to 'records.txt'."""
        try:
            with open("records.txt", "w") as f:
                f.write(f"{self._initial_money}\n")
                for rec in self._records:
                    f.write(f"{rec.category} {rec.description} {rec.amount}\n")
        except Exception as e:
            print(f"Failed to save records: {e}")

def main():
    categories = Categories()
    records = Records()

    while True:
        cmd = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
        if cmd == 'add':
            inp = input("Add some expense or income records with category, description, and amount (separate by commas):\n")
            records.add(inp, categories)
        elif cmd == 'view':
            records.view()
        elif cmd == 'delete':
            idx = input("Enter the index of the record you want to delete: ")
            records.delete(idx)
        elif cmd == 'view categories':
            categories.view()
        elif cmd == 'find':
            cat = input("Which category do you want to find? ")
            subs = categories.find_subcategories(cat)
            if not subs:
                print("Category not found.")
            else:
                print(f'Here are records under category "{cat}":')
                records.find(subs)
        elif cmd == 'exit':
            records.save()
            print("Goodbye!")
            break
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()