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


class Experiment(BasicRec):
    RECORD_LEN = BasicRec.MAX_NAME_LEN + 1 \
        + BasicRec.TIMESTAMP_LEN + 1 \
        + (BasicRec.MAX_READING_LEN * BasicRec.MAX_READINGS_NUM) \
        + (BasicRec.MAX_READINGS_NUM - 1)

    @staticmethod
    def size():
        return self.__class__.RECORD_LEN

    @staticmethod
    def pack(record):
        assert isinstance(record, Experiment)
        readings = "\0".join(str(r) for r in record._readings)
        result = f"{record._name}\0{record._timestamp}\0{readings}"
        if len(result) < Experiment.RECORD_LEN:
            result += "\0" * (Experiment.RECORD_LEN - len(result))
        return result

    @staticmethod
    def unpack(raw):
        assert isinstance(raw, str)
        parts = raw.split("\0")
        name = parts[0]
        timestamp = int(parts[1])
        readings = [int(r) for r in parts[2:] if len(r)]
        return Experiment(name, timestamp, readings)

    @staticmethod
    def pack_multi(records):
        return ''.join([Experiment.pack(r) for r in records])

    @staticmethod
    def unpack_multi(raw):
        size = Experiment.size()
        split = [raw[i:i + size] for i in range(0, len(raw), size)]
        return [Experiment.unpack(s) for s in split]
    
    
    
    
