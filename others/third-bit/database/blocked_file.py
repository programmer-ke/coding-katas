from pathlib import Path
from blocked import Blocked


class BlockedFile(Blocked):

    def __init__(self, record_cls, db_dir):
        super().__init__(record_cls)
        self._db_dir = Path(db_dir)
        self._build_index()


    def add(self, record):
        super().add(record)
        self._save(record)


    def get(self, key):
        if key not in self._index:
            return None
        self._load(key)
        return super().get(key)

    def _save(self, record):
        key = self._record_cls.key(record)
        seq_id = self._next_seq_id()
        self._index[key] = seq_id
        block_id = self._get_block_id(seq_id)

        block = self._get_block(block_id)
        packed = self._record_cls.pack_multi(block.values())

        filename = self._get_filename(block_id)
        with open(filename, 'wt') as f:
            f.write(''.join(packed))

    def _load(self, key):
        seq_id = self._index[key]
        block_id = self._get_block_id(seq_id)
        filename = self._get_filename(block_id)
        self._load_block(block_id, filename)

    def _load_block(self, block_id, filename):
        with open(filename, "r") as reader:
            raw = reader.read()

        records = self._record_cls.unpack_multi(raw)
        base = self.size() * block_id
        block = self._get_block(block_id)
        for i, r in enumerate(records):
            block[base + i] = r

    

