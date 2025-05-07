import importlib.util
import sys
from pathlib import Path
import os
import pytest

# Dynamically load the module under test
spec = importlib.util.spec_from_file_location(
    "pymoney",
    str(Path(__file__).parent.parent / "110062238_潘茗脩_hw3.py")
)
pymoney = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pymoney)

Record = pymoney.Record
Categories = pymoney.Categories
Records = pymoney.Records


def test_record_properties():
    r = Record('meal', 'breakfast', -50)
    assert r.category == 'meal'
    assert r.description == 'breakfast'
    assert r.amount == -50
    assert str(r) == 'meal breakfast -50'


def test_categories_validation_and_find():
    cats = Categories()
    # Valid categories
    assert cats.is_category_valid('meal')
    assert cats.is_category_valid('bus')
    assert cats.is_category_valid('salary')
    # Invalid category
    assert not cats.is_category_valid('clothing')
    # Find subcategories
    food_subs = cats.find_subcategories('food')
    assert set(food_subs) == set(['food', 'meal', 'snack', 'drink'])
    trans_subs = cats.find_subcategories('transportation')
    assert set(trans_subs) == set(['transportation', 'bus', 'railway'])
    # Nonexistent
    assert cats.find_subcategories('unknown') == []


def test_records_init_and_save(tmp_path, monkeypatch):
    # Prepare a temporary records.txt
    content = "1000\nmeal breakfast -50\nfood bread -80\n"
    tmp_file = tmp_path / "records.txt"
    tmp_file.write_text(content)
    # Change cwd to tmp_path
    monkeypatch.chdir(tmp_path)

    cats = Categories()
    recs = Records(cats)
    # Initialization
    assert recs._initial_money == 1000
    assert len(recs._records) == 2
    assert any(r.category == 'meal' and r.description == 'breakfast' and r.amount == -50 for r in recs._records)
    # Test save after modifications
    recs.add('bus commute -20')
    recs.save()
    saved_lines = tmp_file.read_text().splitlines()
    assert saved_lines[0] == '1000'
    assert 'bus commute -20' in saved_lines[-1]


def test_add_invalid_category(capsys):
    cats = Categories()
    recs = Records(cats)
    recs.add('clothing pants -100')
    captured = capsys.readouterr()
    assert 'not in the category list' in captured.out


def test_delete_and_find(capsys):
    cats = Categories()
    recs = Records(cats)
    # Seed some records manually
    recs._records = [
        Record('meal', 'a', -10),
        Record('food', 'b', -5),
        Record('bus', 'c', -2)
    ]
    # Test delete valid
    recs.delete('2')  # should delete 'food b -5'
    assert len(recs._records) == 2
    assert all(r.category != 'food' for r in recs._records)
    # Test delete invalid
    recs.delete('10')
    out = capsys.readouterr().out
    assert 'Invalid index' in out

    # Test find filters correctly
    recs._records = [
        Record('meal', 'x', -10),
        Record('bus', 'y', -5),
        Record('meal', 'z', -3)
    ]
    # Only meal
    recs.find(['meal'])
    captured = capsys.readouterr().out
    assert 'meal' in captured
    assert 'bus' not in captured


def test_view_outputs(capsys):
    cats = Categories()
    recs = Records(cats)
    recs._records = [Record('meal', 'test', -15)]
    recs._initial_money = 100
    recs.view()
    captured = capsys.readouterr().out
    assert "Here\"s your expense and income records:" in captured
    assert 'meal' in captured
    assert 'test' in captured
    assert '85' in captured  # 100 - 15 = 85

if __name__ == '__main__':
    pytest.main()
