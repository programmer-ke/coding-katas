import pytest


class DataBase:
    def __init__(self, record_cls):
        self._record_cls = record_cls
        
    def add(self, record):
        raise NotImplementedError('add')

    def get(self, key):
        raise NotImplementedError('get')


class JustDict(Database):
    def __init__(self, record_cls):
        super().__init__(record_cls)
        self._data = {}

    def add(self, record):
        key = self._record_cls.key(record)
        self._data[key] =  record

    def get(self, key):
        return self._data.get(key, None)


class BasicRec:
    MAX_NAME_LEN = 6     # length of name in chars
    TIMESTAMP_LEN = 8    # length of timestamp in chars
    MAX_READING = 10     # maximum reading value
    MAX_READING_LEN = 2  # length of reading in chars
    MAX_READINGS_NUM = 2 # maximum number of readings

    @staticmethod
    def key(record):
        assert isinstance(record, BasicRec)
        return record._name

    def __init__(self, name, timestamp, readings):
        assert 0 < len(name) <= self.MAX_NAME_LEN
        assert 0 <= len(readings) <= self.MAX_READINGS_NUM
        assert all((0 <= r <= self.MAX_READING) for r in readings)
        self._name = name
        self._timestamp = timestamp
        self._readings = readings


@pytest.fixture
def db():
    return JustDict(BasicRec.key)

@pytest.fixture
def ex01():
    return BasicRec("ex01", 12345, [1, 2])


@pytest.fixture
def ex02():
    return BasicRec("ex02", 67890, [3, 4])
        
def test_construct(db):
    assert db

def test_get_nothing_from_empty_db(db):
    assert db.get("something") is None

def test_add_then_get(db, ex01):
    db.add(ex01)
    assert db.get("ex01") == ex01

def test_add_two_then_get_both(db, ex01, ex02):
    db.add(ex01)
    db.add(ex02)
    assert db.get("ex01") == ex01
    assert db.get("ex02") == ex02

def test_add_then_overwrite(db, ex01):
    db.add(ex01)
    ex01._timestamp = 67890
    db.add(ex01)
    assert db.get("ex01") == ex01
