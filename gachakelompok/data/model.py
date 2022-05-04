from math import ceil


class Mahasiswa():
    def __init__(
        self,
        gid: int | str | None = None,
        nama_gol: str | None = None,
        mid: int | str | None = None,
        nama: str | None = None,
        nim: str | None = None,
        kelamin: str | None = None
    ):
        self.gid = str(gid) if gid is not None else "empty"
        self.nama_gol = nama_gol.upper() if nama_gol is not None else "C"
        self.mid = str(mid) if mid is not None else "empty"
        self.nama = nama.capitalize() if nama is not None else "empty"
        self.nim = nim.upper() if nim is not None else "empty"
        self.kelamin = kelamin.upper() if kelamin is not None else "L"


class KelompokRandom():
    def __init__(
        self,
        jml_mhs: int,
        data: list[Mahasiswa],
        wanita: bool,
        jml_klmp: int | None = None
    ) -> None:
        jumlah_klmk = jml_klmp if jml_klmp else ceil(len(data)/jml_mhs)
        self.data = self.ensure_woman(
            data, jml_mhs, jumlah_klmk
        ) if wanita else self.process(data, jml_mhs, jumlah_klmk)

    @staticmethod
    def process(data, jml, kmlpk) -> list[list[Mahasiswa]]:
        __data = [[]]
        idx = 0
        for i in range(kmlpk):
            for _ in range(jml):
                __data[i].append(data[idx])
                idx += 1

        return __data

    @staticmethod
    def ensure_woman(data, jml, kmlpk) -> list[list[Mahasiswa]]:
        __data = [[]]
        woman = [
            data.pop(data.index(w))
            for w in data
            if w.kelamin == "P"
        ]
        idx = 0
        for _i in range(kmlpk):
            for _k in range(jml - int(len(woman)/kmlpk)):
                __data[_i].append(data[idx])
                idx += 1
        _w = 0
        for _n in __data:
            if _w == len(woman):
                break
            while len(_n) < jml:
                _n.append(woman[_w])
                _w += 1

        return __data


def get_list_object(obj: object):
    return [
        _v for _, _v in vars(obj).items() if str(hex(id(_v))) not in str(_v)
    ]


if __name__ == "__main__":
    print(get_list_object(Mahasiswa(1, 'C', 2, 'rizal', 'e32201406', 'l')))
