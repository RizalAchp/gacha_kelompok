# from model import Mahasiswa, dataclass
from rich.color import ANSI_COLOR_NAMES
from typing import Literal, Optional, Set, Tuple, Type, TypeAlias, Union, get_args
from types import TracebackType, UnionType

Ganti = Literal[
    "update", "edit", "u"
]

Tambah = Literal[
    "add", "tambah", "a"
]

Urutkan = Literal[
    "sort", "urutkan", "s"
]

Randoming = Literal[
    "rand", "gacha", "g"
]

Hapus = Literal[
    "del", "hapus", "d"
]

CommandsOperator: TypeAlias = Literal[
    Ganti, Randoming, Hapus, Tambah, Urutkan
]


class CommandList:
    Command = get_args(CommandsOperator)
    Ganti = get_args(Ganti)
    Tambah = get_args(Tambah)
    Urutkan = get_args(Urutkan)
    Randoming = get_args(Randoming)
    Hapus = get_args(Hapus)


Mode: TypeAlias = Literal[
    "id", "nama_gol", "mahasiswa_id", "nama", "nim"
]
ModeUrut = Union[str, Mode]
Urut = get_args(Mode)

StylePrinted: TypeAlias = Literal[
    "b", "bold", "i", "italic", "u", "underline",
    "s", "strike", "r", "reverse", "blink", "o"
    "uu", "underline2", "frame", "encircle", "overline"
]
StylePrint = Union[object, StylePrinted]

TheColors: TypeAlias = Literal[
    "black", "red", "green", "yellow", "blue", "magenta", "cyan",
    "white", "bright_black", "bright_red", "bright_green",
    "bright_yellow", "bright_blue", "bright_magenta", "bright_cyan",
    "bright_white", "grey0", "gray0", "navy_blue", "dark_blue", "blue3",
    "blue1", "dark_green", "deep_sky_blue4", "dodger_blue3",
    "dodger_blue2", "green4", "spring_green4", "turquoise4",
    "deep_sky_blue3", "dodger_blue1", "green3", "spring_green3",
    "dark_cyan", "light_sea_green", "deep_sky_blue2", "deep_sky_blue1",
    "spring_green2", "cyan3", "dark_turquoise", "turquoise2", "green1",
    "spring_green1", "medium_spring_green", "cyan2", "cyan1", "dark_red",
    "deep_pink4", "purple4", "purple3", "blue_violet", "orange4", "grey37",
    "gray37", "medium_purple4", "slate_blue3", "royal_blue1",
    "chartreuse4", "dark_sea_green4", "pale_turquoise4", "steel_blue",
    "steel_blue3", "cornflower_blue", "chartreuse3", "cadet_blue",
    "sky_blue3", "steel_blue1", "pale_green3", "sea_green3", "aquamarine3",
    "medium_turquoise", "chartreuse2", "sea_green2", "sea_green1",
    "aquamarine1", "dark_slate_gray2", "dark_magenta", "dark_violet",
    "purple", "light_pink4", "plum4", "medium_purple3", "slate_blue1",
    "yellow4", "wheat4", "grey53", "gray53", "light_slate_grey",
    "light_slate_gray", "medium_purple", "light_slate_blue",
    "dark_olive_green3", "dark_sea_green", "light_sky_blue3", "sky_blue2",
    "dark_sea_green3", "dark_slate_gray3", "sky_blue1", "chartreuse1",
    "light_green", "pale_green1", "dark_slate_gray1", "red3",
    "medium_violet_red", "magenta3", "dark_orange3", "indian_red",
    "hot_pink3", "medium_orchid3", "medium_orchid", "medium_purple2",
    "dark_goldenrod", "light_salmon3", "rosy_brown", "grey63", "gray63",
    "medium_purple1", "gold3", "dark_khaki", "navajo_white3", "grey69",
    "gray69", "light_steel_blue3", "light_steel_blue", "yellow3",
    "dark_sea_green2", "light_cyan3", "light_sky_blue1", "green_yellow",
    "dark_olive_green2", "dark_sea_green1", "pale_turquoise1", "deep_pink3",
    "magenta2", "hot_pink2", "orchid", "medium_orchid1", "orange3",
    "light_pink3", "pink3", "plum3", "violet", "light_goldenrod3", "tan",
    "misty_rose3", "thistle3", "plum2", "khaki3", "light_goldenrod2",
    "light_yellow3", "grey84", "gray84", "light_steel_blue1", "yellow2",
    "dark_olive_green1", "honeydew2", "light_cyan1", "red1", "deep_pink2",
    "deep_pink1", "magenta1", "orange_red1", "indian_red1", "hot_pink",
    "dark_orange", "salmon1", "light_coral", "pale_violet_red1", "orchid2",
    "orchid1", "orange1", "sandy_brown", "light_salmon1", "light_pink1",
    "pink1", "plum1", "gold1", "navajo_white1", "misty_rose1", "thistle1",
    "yellow1", "light_goldenrod1", "khaki1", "wheat1", "cornsilk1", "grey100",
    "gray100", "grey3", "gray3", "grey7", "gray7", "grey11", "gray11",
    "grey15", "gray15", "grey19", "gray19", "grey23", "gray23", "grey27",
    "gray27", "grey30", "gray30", "grey35", "gray35", "grey39", "gray39",
    "grey42", "gray42", "grey46", "gray46", "grey50", "gray50", "grey54",
    "gray54", "grey58", "gray58", "grey62", "gray62", "grey66", "gray66",
    "grey70", "gray70", "grey74", "gray74", "grey78", "gray78", "grey82",
    "gray82", "grey85", "gray85", "grey89", "gray89", "grey93", "gray93",
]

MYCOLOR = list(ANSI_COLOR_NAMES)


def warna(byid: int = 0, byname: str | None = None):
    if byname:
        return MYCOLOR[MYCOLOR.index(byname)]
    return MYCOLOR[byid]


def get_styled(
        obj: str, _id: int = 0,
        byname: Optional[TheColors] = None,
        _s: Optional['StylePrint'] = "b"
):
    _c = warna(_id, byname)
    return f'[{_s} {_c}]{obj}[/{_s} {_c}]'


if __name__ == "__main__":
    pass
