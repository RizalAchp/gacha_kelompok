import rich
from rich.progress import Progress
from rich.table import Table
from rich import box, pretty

from .data import *
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
                get_styled(_mh.mid, byname='magenta'),
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
                    get_styled(kel.mid, _id=idx),
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
        return False
    return True


def show_table(_d: DataListCsv, name):
    console.clear()
    _table = TableShow("List Mahasiswa").draw(_d.data)
    PRINT(_table)
    if _d.check():
        PRINT("Tidak ada data yang tersedia..")
        PRINT(
            f"tambahkan terlebih dahulu data sebelum melakukan {name}")
        return False
    return True


def yes(strs: str):
    return re.search("^y.*|^Y.*", strs)


def print_display_awal():
    console.clear()
    PRINT(
        "[bold white on dark_red] :cat::cat: Gacha Kelompok :cat::cat: [/]",
        justify="center")
    PRINT(
        ":nerd_face: [dark_red](by Rizal Achmad Pahlevi)[/dark_red]"
        " :nerd_face:",
        justify="center", end="\n\n")
    PRINT(
        ":robot_face: [magenta]Apa Yang Ingin Anda Lakukan?"
        " pilih command dibawah![/magenta]",
        new_line_start=True, end="\n\n"
    )

    PRINT("[b black on green] :heavy_plus_sign:", end="\t")
    PRINT(
        f"[b black on green]  {' | '.join(list(CommandList.Tambah))}  "
        "[/b black on green]",
        sep="|", end="\t\t")
    PRINT(
        "➜  [green]tambahkan mahasiswa pada list[/green]"
    )

    PRINT("[b black on yellow] :toolbox:", end="\t")
    PRINT(
        f"[b black on yellow]  {' | '.join(list(CommandList.Ganti))}  "
        "[/b black on yellow]",
        sep="|", end="\t\t")
    PRINT(
        "➜  [yellow]edit mahasiswa pada list[/yellow]"
    )

    PRINT("[b white on navy_blue] :computer:", end="\t")
    PRINT(
        f"[b white on navy_blue]  {' | '.join(list(CommandList.Randoming))}  "
        "[/b white on navy_blue]",
        sep="|", end="\t\t")
    PRINT(
        "➜  [blue]mulai gacha!![/blue]"
    )

    PRINT("[b black on cyan] :bar_chart:", end="\t")
    PRINT(
        f"[b black on cyan]  {' | '.join(list(CommandList.Urutkan))}  "
        "[/b black on cyan]",
        sep="|", end="\t\t")
    PRINT(
        "➜  [bright_cyan]urutkan list mahasiswa[/bright_cyan]"
    )

    PRINT("[b black on bright_red] :warning-emoji:", end="\t")
    PRINT(
        f"[b black on bright_red]  {' | '.join(list(CommandList.Hapus))}  "
        "[/b black on bright_red]",
        sep="|", end="\t\t")
    PRINT(
        "➜  [bright_red]hapus mahasiswa pada list[/bright_red]",
        end="\n\n"
    )

    PRINT("[b black in bright_white] :stop_sign:   ", end="\t")
    PRINT("[b black in bright_white]  q/Q/quit/ctrl+c", end="\t\t")
    PRINT(
        "➜  [bright_white]quit[/bright_white]", end="\n\n"
    )

    cmd = INPUT(
        ":robot_face: [magenta]Masukkan Input Command: [/magenta] \n ➜  "
    )
    if not cmd or cmd.isspace() or re.search(
            "^q.*|^Q.*|^qu.*|^ex.*|^E.*", cmd
    ):
        raise SystemExit(0)
    return cmd


UB = "urutkan berdasarkan "
