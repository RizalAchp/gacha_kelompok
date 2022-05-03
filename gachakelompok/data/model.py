from math import ceil


class Mahasiswa():
    def __init__(
        self,
        id: int | None = None,
        nama_gol: str | None = None,
        mahasiswa_id: int | None = None,
        nama: str | None = None,
        nim: str | None = None,
        kelamin: str | None = None
    ):
        self.id = str(id+1) if id is not None else "empty"
        self.nama_gol = nama_gol.upper() if nama_gol is not None else "C"
        self.mahasiswa_id = str(
            mahasiswa_id+1) if mahasiswa_id is not None else "empty"
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
            for k in range(jml):
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
        for i in range(kmlpk):
            for k in range(jml - int(len(woman)/kmlpk)):
                __data[i].append(data[idx])
                idx += 1
        w = 0
        for n in __data:
            if w == len(woman):
                break
            while len(n) < jml:
                n.append(woman[w])
                w += 1

        return __data


def list_obj(obj: object):
    return [
        val for k, val in vars(obj).items()
        if not str(hex(id(val))) in str(val)
    ]


if __name__ == "__main__":
    print(list_obj(Mahasiswa('1', 'C', '2', 'rizal', 'e32201406', 'l')))
