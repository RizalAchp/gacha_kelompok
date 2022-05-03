import re
import rich
import time
from rich.progress import Progress
from rich.table import Table
from rich import box, pretty

from gachakelompok.data.the_data import (
    DataListCsv, RandomData, Mahasiswa,
    CommandsOperator, TheColors, StylePrinted, CommandList,
    KelompokRandom, warna, get_styled, Urut
)

console = rich.get_console()
PRINT = console.print
INPUT = console.input


def progress_wrapper(fun):
    def wrapper():
        with Progress(transient=True) as progress:
            task = progress.add_task("main menu...", total=100)
            while not progress.finished:
                progress.update(task, advance=5.0)
                time.sleep(0.05)
        return fun()
    return wrapper


class TableShow(Table):
    def __init__(self, title):
        super().__init__(
            title=title,
            show_header=True,
            show_lines=True,
            header_style="bold blue",
            box=box.ROUNDED,
        )
        self.add_column("Mhs-ID", min_width=5, justify="center")
        self.add_column("Nama", min_width=15, justify="center")
        self.add_column("NIM", min_width=10, justify="center")
        self.add_column("Golongan", min_width=5, justify="center")

    def draw(self, mhsw: list[Mahasiswa]):
        for _mh in mhsw:
            self.add_row(
                get_styled(_mh.mahasiswa_id, byname='magenta'),
                get_styled(_mh.nama, byname="blue", _s="u"),
                get_styled(_mh.nim, byname='cyan', _s="frame b"),
                get_styled(_mh.nama_gol, byname='blue_violet')
            )
        return self


class TableKelompok(Table):
    def __init__(self):
        super().__init__(
            title="Tabel Kelompok Random",
            show_header=True,
            show_lines=True,
            header_style="bold blue",
            box=box.ROUNDED,
        )
        self.add_column("Mhs-ID", min_width=5, justify="center")
        self.add_column("Golongan", min_width=5, justify="center")
        self.add_column("Nama", min_width=15, justify="center")
        self.add_column("NIM", min_width=10, justify="center")
        self.add_column("Kelompok", min_width=8, justify="center")

    def draw(self, kels: KelompokRandom):
        for idx, kelompok in enumerate(kels.data, start=1):
            for kel in kelompok:
                self.add_row(
                    get_styled(kel.mahasiswa_id, _id=idx),
                    get_styled(kel.nama_gol, _id=idx),
                    get_styled(kel.nama, _id=idx, _s='bold u'),
                    get_styled(kel.nim, _id=idx, _s='bold u'),
                    get_styled(f'Kel {idx}', _id=idx)
                )
        return self


def show_table_kelompok(kels: KelompokRandom, name):
    console.clear()
    table = TableKelompok().draw(kels)
    PRINT(table)
    if any(kels.data):
        PRINT("Tidak ada data yang tersedia..")
        PRINT(
            f"tambahkan terlebih dahulu data sebelum melakukan {name}")
        return ask_back()
    return None


def show_table(_d: DataListCsv, name):
    console.clear()
    _table = TableShow("List Mahasiswa").draw(_d.data)
    PRINT(_table)
    if _d.check():
        PRINT("Tidak ada data yang tersedia..")
        PRINT(
            f"tambahkan terlebih dahulu data sebelum melakukan {name}")
        return ask_back()
    return None


def yes(strs: str):
    return re.search("^y.*|^Y.*", strs)


def ask_back():
    PRINT("back Main Menu or exit?")
    back = INPUT("(y/Y/yes) or any key for exit \n -> ")
    if yes(back):
        return main_cli()
    raise SystemExit(0)


def ask_save(ins, name, file):
    save = INPUT(f"simpan data {name}? (y/N) \n -> ")
    if yes(save):
        ins.submit_data()
        PRINT(
            f"{name} data telah tersimpan di :\n\t`{file}`")

    return ask_back()


def random_data():
    console.clear()
    rand: RandomData | None = None
    data = DataListCsv()
    PRINT(
        "Masukkan Jumlah anggota Setiap Kelompok yang akan di Random",
        style="bold cyan"
    )
    jml = int(INPUT("Jumlah Anggota: "))
    if isinstance(jml, int):
        wmn = INPUT("pastikan setiap kelompok ada cwe nya? :v (y/N) \n -> ")
        if yes(wmn):
            rand = RandomData(data.data, jml, True)
        else:
            rand = RandomData(data.data, jml)

        while True:
            rand.random_data()
            show_table_kelompok(rand.data, "`Random Data`")
            PRINT("yakin dengan random data?", style="bold yellow")
            ykn = INPUT(
                "lanjut random? (y/n) atau ketik apa aja untuk stop \n -> "
            )
            if yes(ykn):
                continue
            break

        return ask_save(rand, "random", rand.file_out)

    PRINT(
        "jumlah error! ketikkan jumlah berupa angka! contoh: `4`",
        style="bold red"
    )
    return random_data()


def tambah_data():
    console.clear()
    data = DataListCsv()
    PRINT("Proses Menambahkan Data Pada List Mahasiswa",
          new_line_start=True)
    ID = dict(zip(["A", "B", "C", "D"], [1, 2, 3, 4]))
    while True:
        gol = INPUT("golongan(ex: a/b/c/d..)    : ").upper()
        nam = INPUT("nama(nama mahasiswa)       : ")
        nim = INPUT("nim(ex: e322..)            : ")
        kel = INPUT("kelamin(ex: L / W)         : ")

        data.tambah(Mahasiswa(ID[gol], gol, data.jumlah_mhs, nam, nim, kel))
        PRINT("mahasiswa tertambah.. ingin menambah lagi?",
              style="bold yellow")
        ykn = INPUT(
            "lanjut tambah? (y/n) atau ketik apa aja untuk stop \n -> "
        )
        if yes(ykn):
            continue
        break

    show_table(data, "`Tambah Data`")
    return ask_save(data, "mahasiswa", data.file_list)


def ganti_data():
    console.clear()
    data = DataListCsv()
    show_table(data, "`Update Data`")
    PRINT("Proses Ganti Data Pada List Mahasiswa",
          new_line_start=True)
    while True:
        PRINT("masukan index dari data mahasiswa yang ingin diubah")
        idx = int(INPUT("index(ex: 0/1/2/3...!!HARUSANGKA!!) : "))
        PRINT(f"masukkan data baru untuk mahasiswa {data.data[idx].nama}")
        data.data[idx].nama_gol = INPUT(
            "golongan(ex: a/b/c/d..)    : ").upper()
        data.data[idx].nama = INPUT(
            "nama(nama mahasiswa)       : ").capitalize()
        data.data[idx].nim = INPUT(
            "nim(ex: e322..)            : ").upper()
        data.data[idx].kelamin = INPUT(
            "kelamin(ex: L / W)         : ").upper()

        PRINT("mahasiswa berhasil di tambah.. ingin mengubah lagi?",
              style="bold yellow")
        ykn = INPUT(
            "lanjut edit? (y/N) atau ketik apa aja untuk stop \n -> "
        )
        if yes(ykn):
            continue
        break
    return ask_save(data, "update mahasiswa", data.file_list)


def urutkan_data():
    console.clear()
    data = DataListCsv()
    show_table(data, "`Mengurutkan Data`")
    PRINT("Proses Mengurutkan Data Pada List Mahasiswa", end="\n\n",
          new_line_start=True)
    desc = [f"{UB}id", f"{UB}nama golongan",
            f"{UB}id mahasiswa", f"{UB}nama", f"{UB}nim"]
    PRINT("Urutkan Data Sesuai Dengan?")
    for i, (u, d) in enumerate(zip(Urut, desc)):
        PRINT(f"[b black on cyan] {i} -> ", end="\t")
        PRINT(
            f"[b black on cyan]  {u}  [/b black on cyan]",
            sep="|", end="\t\t")
        PRINT(
            f"-> [bright_cyan]{d}[/bright_cyan]\n"
        )

    idx = int(INPUT(
        "pilih salah satu dari mode diatas(angka saja: 1,2,3...): "))
    resv = INPUT("reserve sort?(y/N) \n -> ")
    if yes(resv):
        data.urutkan(Urut[idx], True)
    data.urutkan(Urut[idx])

    return ask_save(data, "urutan baru mahasiswa", data.file_list)


def hapus_data():
    data = DataListCsv()
    console.clear()
    PRINT("Proses Menghapus Data Pada List Mahasiswa",
          new_line_start=True)
    while True:
        show_table(data, "`Menghapus Data`")
        idx = INPUT(
            "Masukkan [green]Mhs-ID[/green] dari [green]Tabel Mahasiswa[green] "
            "diatas yang ingin Dihapus\n -> "
        )
        mhdel = data.data[int(idx)-1]
        askdel = INPUT(
            "yakin menghapus mahasiswa:"
            f" [red on white]`{mhdel.nama}`[/red on white]"
            " dari list?(y/N) \n -> "
        )
        if yes(askdel):
            data.hapus_mhs(mhdel)
        ykn = INPUT(
            "lanjut menghapus data lain? (y/N)"
            " atau ketik apa aja untuk stop \n -> "
        )
        if yes(ykn):
            continue
        break

    return ask_save(data,
                    "data mahasiswa baru setelah dihapus",
                    data.file_list)


def operator_command(_d: str):
    if _d in CommandList.Command:
        if _d in CommandList.Tambah:
            return tambah_data()
        elif _d in CommandList.Ganti:
            return ganti_data()
        elif _d in CommandList.Randoming:
            return random_data()
        elif _d in CommandList.Urutkan:
            return urutkan_data()
        elif _d in CommandList.Hapus:
            return hapus_data()

    else:
        PRINT(":warning-emoji: [bold red blink] WARNING!![/]")
        PRINT(
            f"[red]command `{_d}` tidak terdefinisi!"
            " pastikan command terdapat pada list pilihan[/red]",
            end="\n\n"
        )
        return main_cli()


def print_display_awal():
    console.clear()
    console.screen(style="white on dark_slate_gray3")
    PRINT(
        "[bold white on dark_red] :cat::cat: Gacha Kelompok :cat::cat: [/]",
        justify="center")
    PRINT(
        ":nerd_face: [dark_red](by Rizal Achmad Pahlevi)[/dark_red] :nerd_face:",
        justify="center", end="\n\n")
    PRINT(
        ":robot_face: [magenta]Apa Yang Ingin Anda Lakukan? pilih command dibawah![/magenta]",
        new_line_start=True, end="\n\n"
    )

    PRINT("[b black on green] :heavy_plus_sign:", end="\t")
    PRINT(
        f"[b black on green]  {' | '.join(list(CommandList.Tambah))}  [/b black on green]",
        sep="|", end="\t\t")
    PRINT(
        "-> [green]tambahkan mahasiswa pada list[/green]"
    )

    PRINT("[b black on yellow] :toolbox:", end="\t")
    PRINT(
        f"[b black on yellow]  {' | '.join(list(CommandList.Ganti))}  [/b black on yellow]",
        sep="|", end="\t\t")
    PRINT(
        "-> [yellow]edit mahasiswa pada list[/yellow]"
    )

    PRINT("[b white on navy_blue] :computer:", end="\t")
    PRINT(
        f"[b white on navy_blue]  {' | '.join(list(CommandList.Randoming))}  [/b white on navy_blue]",
        sep="|", end="\t\t")
    PRINT(
        "-> [blue]mulai gacha!![/blue]"
    )

    PRINT("[b black on cyan] :bar_chart:", end="\t")
    PRINT(
        f"[b black on cyan]  {' | '.join(list(CommandList.Urutkan))}  [/b black on cyan]",
        sep="|", end="\t\t")
    PRINT(
        "-> [bright_cyan]urutkan list mahasiswa[/bright_cyan]"
    )

    PRINT("[b black on bright_red] :warning-emoji:", end="\t")
    PRINT(
        f"[b black on bright_red]  {' | '.join(list(CommandList.Hapus))}  [/b black on bright_red]",
        sep="|", end="\t\t")
    PRINT(
        "-> [bright_red]hapus mahasiswa pada list[/bright_red]",
        end="\n\n"
    )

    PRINT("[b black in bright_white] :stop_sign:   ", end="\t")
    PRINT("[b black in bright_white]  q/Q/quit/ctrl+c", end="\t\t")
    PRINT(
        "-> [bright_white]quit[/bright_white]", end="\n\n"
    )

    cmd = INPUT(
        ":robot_face: [magenta]Masukkan Input Command: [/magenta] \n -> "
    )
    if not cmd or cmd.isspace() or re.search(
            "^q.*|^Q.*|^qu.*|^ex.*|^E.*", cmd
    ):
        raise SystemExit(0)
    return cmd


@progress_wrapper
def main_cli():
    cmd = print_display_awal()
    return operator_command(cmd)


UB = "urutkan berdasarkan "
if __name__ == "__main__":
    pass
