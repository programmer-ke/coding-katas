from pathlib import Path
from unittest.mock import patch
import pytest
import pyfakefs

from backup import backup, hash_all, HASH_LEN

FILES = {"a.txt": "aaa", "b.txt": "bbb", "sub_dir/c.txt": "ccc"}

@pytest.fixture
def our_fs(fs):
    for name, contents in FILES.items():
        fs.create_file(name, contents=contents)

def test_hashing(our_fs):
    result = hash_all(".")
    expected = {"a.txt", "b.txt", "sub_dir/c.txt"}
    assert {r[0] for r in result} == expected
    assert all(len(r[1]) == HASH_LEN for r in result)

def test_change(our_fs):
    original = hash_all(".")
    original = [entry for entry in original if entry[0] == "a.txt"][0]
    with open("a.txt", "w") as writer:
        writer.write("this is new content for a.txt")
    changed = hash_all(".")
    changed = [entry for entry in changed if entry[0] == "a.txt"][0]
    print(original, changed)
    assert original != changed

def test_nested_example(our_fs):
    timestamp = 1234
    with patch("backup.current_time", return_value=timestamp):
        manifest = backup(".", "/backup")
    assert Path("/backup", f"{timestamp}.csv").exists()
    for filename, hash_code in manifest:
        assert Path("/backup", f"{hash_code}.bck").exists()


