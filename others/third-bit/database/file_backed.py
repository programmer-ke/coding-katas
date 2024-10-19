from pathlib import Path
from interface_original import JustDict


class FileBacked(JustDict):

    def __init__(self, record_cls, filename):
        super().__init__(record_cls)
        self._filename = Path(filename)
        if not self._filename.exists():
            self._filename.touch()
        self._load()

    def add(self, record):
        key = self._record_cls.key(record)
        self._data[key] = record
        self._save()

    def _save(self):
        packed = self._record_cls.pack_multi(self._data.values())
        with open(self._filename, 'wt') as f:
            f.write(packed)

    def _load(self):
        assert self._filename.exists()
        with open(self._filename, 'rt') as f:
            packed = f.read()
        records = self._record_cls.unpack_multi(packed)
        self._data = {self._record_cls.key(record): record for record in records}
