# 💾 Pymoney — A Simple Expense Tracker in Python

**Pymoney** is a command-line based personal finance tracker. It allows users to record incomes and expenses, classify them by category, and search or manage them through an intuitive CLI interface.

---

## 📆 Features

* 📅 Add multiple records at once: `category description amount`
* 📊 View all records and see running balance
* 🗑️ Delete records by index
* 🗂️ Display nested categories with indentation
* 🔎 Find records by category (supports subcategory matching)
* 📄 Persistent storage in `records.txt`
* ✨ Recursion + `yield` / `yield from` to traverse nested lists

---

## 🪧 Project Structure

```
.
├── 110062238_潘茗脩_hw3.py      # Main interactive program
├── test/
│   └── test_hw3.py              # Unit tests with pytest
├── records.txt                  # Persistent saved data (created at runtime)
└── README.md                    # This file
```

---

## 🚀 Getting Started

### Run the program

```bash
python3 110062238_潘茜辝_hw3.py
```

### Install dependencies for testing

```bash
pip install pytest
```

### Run tests

```bash
pytest
```

---

## 📁 File Format: `records.txt`

```
1000
meal breakfast -50
food bread -80
salary job 2000
```

* Line 1: Initial balance
* Remaining: Individual records (category, description, amount)

---

## 🫠 Concepts Demonstrated

* □ Object-Oriented Design

  * `Record` class for data
  * `Categories` for recursive category tree
  * `Records` for list management and file I/O

* □ Generator functions using `yield`, `yield from`

* □ Recursive traversal of nested lists

* □ CLI input/output and validation

* □ Data persistence with local files

* □ Unit testing with `pytest`

---

## 📖 Sample Interaction

```txt
> What do you want to do (add / view / delete / find / exit)? add
Add some expense or income records:
meal breakfast -50, salary job 2000

> view
Index Category        Description          Amount
1     meal            breakfast            -50
2     salary          job                  2000
Now you have 1950 dollars.

> find
Which category? income
Category        Description          Amount
salary          job                  2000
The total amount above is 2000.
```

---

## 📙 License

MIT License © 2025 owen920831
