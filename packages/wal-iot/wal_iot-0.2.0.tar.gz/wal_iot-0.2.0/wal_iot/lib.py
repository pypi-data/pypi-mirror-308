from typing import BinaryIO, Optional
from logging import getLogger
import atexit
import pickle
import os

logger = getLogger(__name__)

class WriteAheadLog:
    """
    WriteAheadLog class is responsible for managing the write-ahead log file.

    The layout of a log record is as follows:
    | +Index (4 bytes) | Length (4 bytes) | Data (Length bytes) |
    
    Where
    - Index: A 4-byte signed integer that is used to identify the record. 
    - Length: A 4-byte unsigned integer that is used to indicate the length of the data.
    - Data: The actual data that is written to the log.

    A special record with only negative value of index is used to indicate the corresponding record has been committed.
    | -Index (4 bytes) |
    """

    def __init__(self, log_file: str):
        """
        Create a WriteAheadLog object.

        :param log_file: The path to the log file.
        """
        self.log_file = log_file
        self._log_fd: Optional[BinaryIO] = None
        atexit.register(self.close)

    def init(self):
        """
        Initialize the WriteAheadLog object.
        """
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'wb') as f:
                pass
        with open(self.log_file, 'rb') as f:
            self._staged_records, self._max_index = wal_load(f, validate=True)
        self.compress()
        self._log_fd = open(self.log_file, 'ab', buffering=0)
    
    def open(self):
        """
        Open the log file.
        """
        if self._log_fd and self._log_fd.closed:
            self._log_fd = open(self.log_file, 'ab', buffering=0)
    
    def close(self):
        """
        Close the log file.
        """
        if self._log_fd and not self._log_fd.closed:
            self._log_fd.flush()
            self._log_fd.close()
    
    def tell(self):
        """
        Return the current position of the log file.
        """
        return self._log_fd.tell()
    
    def compress(self):
        """
        Compress the log file by removing the committed records.
        """
        self.close()
        tmp_file = self.log_file + '.tmp'
        with open(tmp_file, 'wb') as f:
            wal_dump(f, self._staged_records)
        os.rename(tmp_file, self.log_file)
        self.open()
        
    def stage(self, data):
        """
        Stage the given data to the log.

        :param data: The data to be staged.
        :return: The index of the staged record.
        """
        b_data = pickle.dumps(data)
        i = self._max_index + 1
        self._staged_records[i] = b_data
        b_record = i.to_bytes(4, signed=True) + len(b_data).to_bytes(4, signed=False) + b_data
        self._log_fd.write(b_record)
        self._log_fd.flush()
        self._max_index = i
        return i
    
    def commit(self, i):
        """
        Commit the record with the given index.

        :param i: The index of the record to be committed.
        """
        if i not in self._staged_records:
            logger.warning(f'The record with index {i} does not exist.')
            return
        del self._staged_records[i]
        b_record = (-i).to_bytes(4, signed=True)
        self._log_fd.write(b_record)
        self._log_fd.flush()
    
    def iter_records(self):
        """
        Iterate over the staged records.
        """
        for i, data in self._staged_records.items():
            yield i, pickle.loads(data)
            

def wal_load(f: BinaryIO, validate=False):
    """
    Load data from the given file object and return the parsed data.
    """
    records = {}
    max_index = 0
    while True:
        b_i = f.read(4)
        if not b_i:
            break
        i = int.from_bytes(b_i, signed=True)
        if i > 0:
            b_l = f.read(4)
            l = int.from_bytes(b_l, signed=False)
            b_data = f.read(l)
            if validate:
                pickle.loads(b_data)
            records[i] = b_data
            max_index = i if i > max_index else max_index
        else:
            del records[-i] 
    return records, max_index


def wal_dump(f: BinaryIO, records: dict):
    """
    Dump the given records to the file object.
    """
    for i, data in records.items():
        f.write(i.to_bytes(4, signed=True))
        f.write(len(data).to_bytes(4, signed=False))
        f.write(data)
        f.flush()
