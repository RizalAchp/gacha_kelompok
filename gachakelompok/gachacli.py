from .proses import (
    PRINT, INPUT, console, progress_wrapper, re, RandomData, DataListCsv,
    yes, show_table, show_table_kelompok, Mahasiswa, Urut, print_display_awal,
    UB, CommandList, MyCSV, pretty, Optional, os,
    read, delete, copy, rename, show
)


@progress_wrapper
def main_cli():
    cmd = print_display_awal()
    return operator_command(cmd)


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


def ask_back():
    PRINT("back Main Menu or exit?")
    back = INPUT("(y/Y/yes) or any key for exit \n ➜ ")
    if yes(back):
        return main_cli()
    raise SystemExit(0)


def ask_save(ins: DataListCsv | RandomData, name, file):
    save = INPUT(f"simpan data {name}? (y/N) \n ➜ ")
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
        wmn = INPUT("pastikan setiap kelompok ada cwe nya? :v (y/N) \n ➜  ")
        if yes(wmn):
            rand = RandomData(data.data, jml, True)
        else:
            rand = RandomData(data.data, jml)

        while True:
            rand.random_data()
            show_table_kelompok(rand.data, "`Random Data`")
            PRINT("yakin dengan random data?", style="bold yellow")
            ykn = INPUT(
                "lanjut random? (y/n) atau ketik apa aja untuk stop \n ➜  "
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

        mh = None
        if not gol:
            mh = Mahasiswa(None, None, data.jumlah_mhs, nam, nim, kel)
        else:
            mh = Mahasiswa(ID[gol], gol, data.jumlah_mhs, nam, nim, kel)

        data.tambah(mh)
        PRINT("mahasiswa tertambah.. ingin menambah lagi?",
              style="bold yellow")
        ykn = INPUT(
            "lanjut tambah? (y/n) atau ketik apa aja untuk stop \n ➜  "
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
        PRINT(f"masukkan data baru untuk mahasiswa {data.data[idx-1].nama}")
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
            "lanjut edit? (y/N) atau ketik apa aja untuk stop \n ➜  "
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
        PRINT(f"[b black on cyan] {i} ➜  ", end="\t")
        PRINT(
            f"[b black on cyan]  {u}  [/b black on cyan]",
            sep="|", end="\t\t")
        PRINT(
            f"➜  [bright_cyan]{d}[/bright_cyan]\n"
        )

    idx = int(INPUT(
        "pilih salah satu dari mode diatas(angka saja: 1,2,3...): "))
    resv = INPUT("reserve sort?(y/N) \n ➜  ")
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
        if not show_table(data, "`Menghapus Data`"):
            return ask_back()
        idx = INPUT(
            "Masukkan [green]Mhs-ID[/green] dari [green]Tabel Mahasiswa[green]"
            " diatas yang ingin Dihapus, or any key to cancel\n ➜  "
        )
        if not idx:
            break
        mhdel = data.data[int(idx)-1]
        askdel = INPUT(
            "yakin menghapus mahasiswa:"
            f" [red on white]`{mhdel.nama}`[/red on white]"
            " dari list?(y/N) \n ➜  "
        )
        if yes(askdel):
            data.hapus_mhs(mhdel)
        ykn = INPUT(
            "lanjut menghapus data lain? (y/N)"
            " atau ketik apa aja untuk stop \n ➜  "
        )
        if yes(ykn):
            continue
        break

    return ask_save(data,
                    "data mahasiswa baru setelah dihapus",
                    data.file_list)


if __name__ == "__main__":
    pass
