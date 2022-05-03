import csv
import os
import random
import re
import time
from .model import (
    Mahasiswa, KelompokRandom, get_list_object
)
from .component import (
    CommandsOperator, TheColors,
    StylePrinted, CommandList,
    Optional, Type, TracebackType,
    ModeUrut, warna, get_styled, Urut
)

HEADER = list(vars(Mahasiswa()))


def bygol(obj: Mahasiswa):
    return int(obj.gid)


def bymid(obj: Mahasiswa):
    return int(obj.mid)


def byname(obj: Mahasiswa):
    return obj.nama[:1]


def bynim(obj: Mahasiswa):
    return obj.nim[-4:]


callback_sort = {
    "gid": bygol,
    "nama_gol": bygol,
    "mid": bymid,
    "nama": byname,
    "nim": bynim
}


class MyCSV():
    """CSV."""

    def __init__(self, _file) -> None:
        """__init__.

        :param _file:
        :rtype: None
        """
        self.file = open(_file, 'w+')

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def write_random(self, _data: list[list[Mahasiswa]]):
        _w = csv.writer(self.file, delimiter=',')
        _w.writerow(HEADER)
        for i, _d in enumerate(_data, start=1):
            _w.writerow([])
            _w.writerow([f">> KELOMPOK {i} <<"])
            _w.writerows([get_list_object(d) for d in _d])

    def write(self, _data: list[Mahasiswa]):
        """__write__.

        :param _data:
        :type _data: list[Mahasiswa]
        """
        _w = csv.DictWriter(self.file, fieldnames=HEADER, delimiter=',')
        _w.writeheader()
        for d in _data:
            _w.writerow(vars(d))

    def read(self):
        """__read__."""
        return [
            Mahasiswa(**data) for data in csv.DictReader(
                self.file, fieldnames=HEADER, delimiter=','
            )
        ]

    def close(self):
        self.file.close()


class DataListCsv():
    """DataListCsv."""
    file_list = os.path.abspath("data.csv")

    def __init__(self) -> None:
        """__init__.

        :rtype: None
        """
        with MyCSV(self.file_list) as _csv:
            self.data = _csv.read()

    def tambah(self, mhs: Mahasiswa) -> None:
        """tambah.

        :param mhs:
        :type mhs: Mahasiswa
        """
        return self.data.append(mhs)

    def hapus_mhs(self, mhs: Mahasiswa) -> None:
        return self.data.remove(mhs)

    def hapus_idx(self, index: int) -> Mahasiswa:
        """hapus.

        :param index:
        :type index: int
        """
        return self.data.pop(index)

    def get_index(self, idx: int) -> Mahasiswa:
        return self.data.pop(idx)

    def ubah(self, index: int, mhs: Mahasiswa) -> None:
        """ubah.

        :param index:
        :type index: int
        :param mhs:
        :type mhs: Mahasiswa
        """
        return self.data.insert(index, mhs)

    def urutkan(self, sortby: ModeUrut, reverse: bool = False) -> None:
        """urutkan.

        :param sortby:
        :type sortby: ModeUrut `( g_id, nama_gol, m_id, nama, nim )`
        :param reverse: = literal[False] of literal[True]
        :type reverse: bool
        """
        self.data.sort(key=callback_sort[sortby], reverse=reverse)

    def check(self) -> bool:
        return False if self.data else True

    def submit_data(self) -> None:
        with MyCSV(self.file_list) as _csv:
            _csv.write(self.data)

    @property
    def jumlah_mhs(self) -> int:
        return len(self.data) if len(self.data) else 0

    @property
    def getdata(self) -> list[Mahasiswa]:
        """data."""
        return self.data


class RandomData():
    """RandomedData."""
    file_out = os.path.abspath("output.csv")

    def __init__(
        self, _data: list[Mahasiswa],
        jml_mhswa_per_klm: int,
        ensure_woman: bool = False
    ) -> None:

        super().__init__()
        """__init__.

        :rtype: None
        """
        self._data = _data
        self.ensure_woman = ensure_woman
        self.jml_mhswa_per_klm = jml_mhswa_per_klm

    def last_random_data(self):
        """get last random data pada file `output.csv`"""
        with MyCSV(self.file_out) as _csv:
            return _csv.read()

    def submit_data(self):
        with MyCSV(self.file_out) as _csv:
            _csv.write_random(self.data.data)

    def random_data(self):
        random.shuffle(self._data)

    @ property
    def data(self) -> KelompokRandom:
        """data."""
        return KelompokRandom(
            self.jml_mhswa_per_klm,
            self._data,
            self.ensure_woman
        )


if __name__ == "__main__":
    data = DataListCsv()
