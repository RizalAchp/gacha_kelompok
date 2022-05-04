from gachakelompok.gachacli import *
import os
import argparse
import shutil
# error messages
INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .csv file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."
shortit = os.path.relpath


class Parser(argparse.ArgumentParser):
    def __init__(self, description: str = "Aplikasi Gacha Golongan C TKK 2020") -> None:
        super().__init__(
            os.path.basename(__file__),
            '%(prog)s [-h, --help, arguments]',
            description,
            'ENJOY~!',
            add_help=True,
            exit_on_error=True
        )
        self.arguments()

    def arguments(self):
        self.add_argument(
            'start', action='store', nargs='?', type=str,
            help="Menjalankan Program Gacha secara Interaktif Mode",
            default='start'
        )
        self.add_argument(
            "-r", "--read", type=str, nargs=1,
            metavar="file", default=None,
            help="Membuka dan Membaca isi file csv.")
        self.add_argument(
            "-s", "--show", type=str, nargs=1,
            metavar="path", default=None,
            help="Menampilkan semua file csv pada directori. Type '.' untuk current directori.")
        self.add_argument(
            "-d", "--delete", type=str, nargs=1,
            metavar="file", default=None,
            help="Menghapus spesifik csv file.")
        self.add_argument(
            "-c", "--copy", type=str, nargs=2,
            metavar=('file1', 'file2'),
            help="Copy file csv file1 dan file2 Warning: file1 akan di overwrite.")
        self.add_argument(
            "--rename", type=str, nargs=2,
            metavar=('old_name', 'new_name'),
            help="Mengganti Nama dari file yang di berikan.")


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
