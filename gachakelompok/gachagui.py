# -*- coding: utf-8 -*-
import glfw
import OpenGL.GL as gl
from gachakelompok.data.the_data import HEADER, DataListCsv

import imgui
from imgui.integrations.glfw import GlfwRenderer

main_window_flags = imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_COLLAPSE | imgui.HOVERED_CHILD_WINDOWS
main_child_flags = imgui.WINDOW_NO_DECORATION
main_table_flags = imgui.TABLE_REORDERABLE | imgui.TABLE_ROW_BACKGROUND | imgui.TABLE_BORDERS | imgui.TABLE_RESIZABLE
datalist = DataListCsv()

WIDHT_SB = 270

def main_window(f_widht, f_height):
    imgui.set_next_window_size(f_widht - WIDHT_SB, f_height)
    imgui.set_next_window_position(WIDHT_SB, 0)
    with imgui.begin("Main", flags=main_window_flags):
        imgui.text("Test")
        child_widht = f_widht - WIDHT_SB
        with imgui.begin_child("canvas", f_widht - WIDHT_SB, f_height - 180,
                               border=True, flags=main_child_flags):
            table_main()
            bottom_menu(child_widht, f_height)


def table_main():
    style = imgui.get_style()
    with imgui.begin_table("Tabel: List Mahasiswa", 6, flags=main_table_flags):
        for i in range(6):
            imgui.table_setup_column(HEADER[i])
        imgui.table_headers_row()
        for row in range(datalist.jumlah_mhs):
            imgui.table_next_row()
            for col in range(len(HEADER)):
                imgui.table_set_column_index(col)
                imgui.text_colored(
                    vars(datalist.data[col])[HEADER[row]], *style.colors[row]
                )


def sidemenu(f_widht, f_height):
    imgui.set_next_window_size(f_widht - 20, f_height)
    imgui.set_next_window_position(20, 20)
    imgui.begin(
        "Hello World",
        flags=imgui.WINDOW_NO_MOVE
        | imgui.WINDOW_NO_RESIZE
        | imgui.WINDOW_NO_SAVED_SETTINGS
        | imgui.WINDOW_NO_COLLAPSE,
    )
    imgui.button("button1")
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("This button is clickable.")
        imgui.text("This button has full window tooltip.")
        texture_id = imgui.get_io().fonts.texture_id
        imgui.image(texture_id, 512, 64, border_color=(1, 0, 0, 1))
        imgui.end_tooltip()
    imgui.button("button2")
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("This button is clickable.")
        imgui.text("This button has full window tooltip.")
        texture_id = imgui.get_io().fonts.texture_id
        imgui.image(texture_id, 512, 64, border_color=(1, 0, 0, 1))
        imgui.end_tooltip()
    imgui.button("button3")
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("This button is clickable.")
        imgui.text("This button has full window tooltip.")
        texture_id = imgui.get_io().fonts.texture_id
        imgui.image(texture_id, 512, 64, border_color=(1, 0, 0, 1))
        imgui.end_tooltip()

    imgui.separator()
    imgui.text("ubah jumlah gacha")
    imgui.text("[kelompok] : [mhsiswa]")
    imgui.separator()
    imgui.begin_child(
        "Table Data",
        border=True,
        flags=imgui.WINDOW_NO_MOVE
        | imgui.WINDOW_NO_RESIZE
        | imgui.HOVERED_ALLOW_WHEN_DISABLED,
    )
    imgui.separator()
    kel_changed, kelompok = imgui.input_int('KELOMPOK', kelompok,)
    imgui.text('JML KELOMPOK: %i' % kelompok)
    imgui.separator()
    mh_changed, mhsiswa = imgui.input_int('MAHASISWA', mhsiswa,)
    imgui.text('JML MAHASISWA: %i' % mhsiswa)
    imgui.end_child()

    imgui.end()


def bottom_menu(f_widht, f_height):
    h = f_height-100
    imgui.begin_child(
        "Bottom Menu",
        f_widht-WIDHT_SB,
        f_height-h,
        flags=imgui.WINDOW_NO_DECORATION
        | imgui.WINDOW_NO_RESIZE
    )
    imgui.text("ini bottom menu")
    imgui.end_child()


def main_gui():
    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    show_custom_window = True
    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        w, h = glfw.get_window_size(window)

        imgui.new_frame()
        imgui.core.style_colors_dark()

        with imgui.begin_main_menu_bar() as main_menu_bar:
            if main_menu_bar.opened:
                # first menu dropdown
                with imgui.begin_menu('File', True) as file_menu:
                    if file_menu.opened:
                        imgui.menu_item('New', 'Ctrl+N', False, True)
                        imgui.menu_item('Open ...', 'Ctrl+O', False, True)

                        # submenu
                        with imgui.begin_menu('Open Recent', True) as open_recent_menu:
                            if open_recent_menu.opened:
                                imgui.menu_item('doc.txt', None, False, True)

        main_window(w, h)

        gl.glClearColor(1., 1., 1., 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()
    return 0


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "minimal ImGui/GLFW3 example"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        raise SystemExit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        raise SystemExit(1)

    return window


if __name__ == "__main__":
    main()
