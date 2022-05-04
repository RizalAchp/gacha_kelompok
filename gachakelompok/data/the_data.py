from .component import (
    CommandsOperator, TheColors,
    StylePrinted, CommandList,
    Optional, Type, TracebackType,
    ModeUrut, warna, get_styled, Urut
)
from .model import (
    Mahasiswa, KelompokRandom, get_list_object
)
from rich import box, pretty
from rich.table import Table
from rich.progress import Progress
import csv
import os
import random
import shutil
import re
import time
import rich

console = rich.get_console()
PRINT = console.print
INPUT = console.input


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

INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .csv file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."
shortit = os.path.relpath


def validate_file(file: str, file2: Optional[str] = None):
    '''
    validate file name and path.
    '''
    if not valid_path(file):
        raise SystemExit(INVALID_PATH_MSG % (file))
    elif not valid_filetype(file):
        raise SystemExit(INVALID_FILETYPE_MSG % (file))
    if file2:
        if not valid_filetype(file2):
            raise SystemExit(INVALID_FILETYPE_MSG % (file2))
        return os.path.abspath(file), os.path.abspath(file2)
    return os.path.abspath(file)


def valid_filetype(file_name: str):
    # validate file type
    return file_name.endswith('.csv')


def valid_path(path: str):
    # validate file path
    return os.path.exists(path)


class MyCSV():
    """CSV."""

    def __init__(self, _file) -> None:
        """__init__.

        :param _file:
        :rtype: None
        """
        if valid_path(_file):
            self.file = _file
        else:
            with open(_file, 'x') as f:
                f.close()
            self.file = _file

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        del self

    def write_random(self, _data: list[list[Mahasiswa]]):
        with open(self.file, "w") as f:
            _w = csv.writer(f, delimiter=',')
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
        with open(self.file, 'w') as f:
            _w = csv.DictWriter(f, HEADER, delimiter=',')
            _w.writeheader()
            for d in _data:
                _w.writerow(vars(d))

    def read(self):
        """__read__."""
        with open(self.file, 'r') as f:
            return [
                Mahasiswa(**data) for data in csv.DictReader(f)
            ]


class DataListCsv():
    """DataListCsv."""
    file_list = os.path.abspath("data.csv")

    def __init__(self) -> None:
        """__init__.

        :rtype: None
        """
        with MyCSV(self.file_list) as _csv:
            data = _csv.read()

            self.data = data

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
        return True if not self.data else False

    def submit_data(self) -> None:
        with MyCSV(self.file_list) as _csv:
            _csv.write(self.data)

    @property
    def jumlah_mhs(self) -> int:
        return int(len(self.data)+1) if len(self.data) else 1

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


def read(fl: str):
    file = validate_file(fl)
    with MyCSV(file) as f:
        console.print("mid\tnama\tnim")
        for m in f.read():
            console.print(f'[blue]{m.mid=}[/blue]', end="\t")
            console.print(f'[b blue]{m.nama=}[/b blue]', end="\t")
            console.print(f'[i blue]{m.nim=}[/i blue]')

    return 0


def show(dirs: str):
    if not valid_path(dirs):
        raise SystemExit("Error: No such directory found.")
    # get text files in directory
    files = [f for f in os.listdir(dirs) if valid_filetype(f)]
    console.print(f"\n[green]{len(files)} csv[/green] files found.\n")
    console.print('\n'.join(f' :book:  [u cyan]{f}[/u cyan]' for f in files))
    return 0


def delete(f: str):
    file = validate_file(f)
    if not isinstance(file, str):
        raise SystemExit(1)

    os.remove(file)
    console.print(f"[b green]Successfully deleted {shortit(file)}.[/b green]")
    return 0


def copy(file1: str, file2: str):
    f1, f2 = validate_file(file1, file2)
    # copy file1 to file2
    shutil.copyfile(src=f1, dst=f2)
    console.print(
        f"Successfully copied {shortit(f1)} to {shortit(f2)}."
    )
    return 0


def rename(old: str, new: str):
    # validate the file to be renamed
    fold = validate_file(old)
    fnew = os.path.abspath(new)
    # validate the type of new file name
    if not valid_filetype(fnew) or not isinstance(fold, str):
        raise SystemExit(INVALID_FILETYPE_MSG % (fnew))
    # renaming
    shutil.move(fold, fnew)
    print(f"Successfully renamed {shortit(fold)} to {shortit(fnew)}.")
    return 0


if __name__ == "__main__":
    data = DataListCsv()
