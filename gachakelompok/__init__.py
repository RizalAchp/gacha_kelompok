from gachakelompok.gachacli import *
import argparse
# error messages


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
            default=None
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
