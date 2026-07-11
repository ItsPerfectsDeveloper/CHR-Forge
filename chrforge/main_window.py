import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QWidget,
    QHBoxLayout,
    QMessageBox,
    QComboBox,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtGui import QAction

from tile_view import TileView
from tile_editor import TileEditor
from chr import encode_tile

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_file = None
        self.current_tile_index = -1
        self.clipboard_tile = None
        
        self.undo_stack = []
        self.redo_stack = []

        self.setWindowTitle("CHR Forge")
        self.resize(1200, 700)

        self.tile_view = TileView()
        self.tile_editor = TileEditor()

        self.size_combo.currentTextChanged.connect(
            self.change_edit_size
        )

        self.tile_view.tileSelected.connect(
            self.select_tile
        )

        self.tile_editor.tileChanged.connect(
            self.tile_modified
        )

        central = QWidget()
        layout = QHBoxLayout()

# Left side
        addWidget(self.tile_view)

# Right side
        right_layout = QVBoxLayout()

        toolbar_layout = QHBoxLayout()

        toolbar_layout.addWidget(
            QLabel("Edit Size:")
        )

        self.size_combo = QComboBox()

        self.size_combo.addItems([
            "8×8",
            "16×16",
            "32×32",
            "64×64"
        ])

        self.size_combo.currentTextChanged.connect(
            self.change_edit_size
        )

        toolbar_layout.addWidget(
            self.size_combo
        )

        right_layout.addLayout(toolbar_layout)
        right_layout.addWidget(self.tile_editor)

        layout.addLayout(right_layout)

        central.setLayout(layout)
        self.setCentralWidget(central)
        self.setCentralWidget(central)

        self.create_menu()
        
        self.statusBar().showMessage(
            "No tile selected"
        )
        self.tile_editor.pixelSelected.connect(
            self.pixel_selected
        )
    def push_undo(self):
        if self.current_tile_index < 0:
            return

        self.undo_stack.append(
            self.tile_editor.get_tile_copy()
        )

        self.redo_stack.clear()    

    def create_menu(self):
        menu_bar = self.menuBar()

        # FILE MENU

        file_menu = menu_bar.addMenu("File")

        open_action = file_menu.addAction(
            "Open ROM..."
        )
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(
            self.open_file
        )

        save_rom_action = file_menu.addAction(
            "Save ROM..."
        )
        save_rom_action.setShortcut("Ctrl+S")
        save_rom_action.triggered.connect(
            self.save_rom
        )
        save_chr_action = file_menu.addAction(
            "Save CHR..."
        )

        save_chr_action.setShortcut(
            "Ctrl+Shift+C"
        )

        save_chr_action.triggered.connect(
            self.save_chr
        )

        # EDIT MENU

        edit_menu = menu_bar.addMenu("Edit")

        copy_tile_action = edit_menu.addAction(
            "Copy Tile"
        )
        copy_tile_action.setShortcut("Ctrl+C")
        copy_tile_action.triggered.connect(
            self.copy_tile
        )

        paste_tile_action = edit_menu.addAction(
            "Paste Tile"
        )
        paste_tile_action.setShortcut("Ctrl+V")
        paste_tile_action.triggered.connect(
            self.paste_tile
        )

        edit_menu.addSeparator()

        clear_tile_action = edit_menu.addAction(
            "Clear Tile"
        )
        clear_tile_action.triggered.connect(
            self.clear_tile
        )

        flip_h_action = edit_menu.addAction(
            "Flip Horizontal"
        )
        flip_h_action.triggered.connect(
            self.flip_horizontal
        )

        flip_v_action = edit_menu.addAction(
            "Flip Vertical"
        )
        flip_v_action.triggered.connect(
            self.flip_vertical
        )
        
        undo_action = edit_menu.addAction("Undo")
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)

        redo_action = edit_menu.addAction("Redo")
        redo_action.setShortcut("Ctrl+Shift+Z")
        redo_action.triggered.connect(self.redo)

        edit_menu.addSeparator()

        # PALETTE MENU

        palette_menu = menu_bar.addMenu(
            "Palette"
        )

        save_palette_action = (
            palette_menu.addAction(
                "Save Palette (.pal)"
            )
        )

        save_palette_action.setShortcut(
            "Ctrl+Shift+S"
        )

        save_palette_action.triggered.connect(
            self.save_palette
        )

        load_palette_action = (
            palette_menu.addAction(
                "Load Palette (.pal)"
            )
        )

        load_palette_action.setShortcut(
            "Ctrl+Shift+O"
        )

        load_palette_action.triggered.connect(
            self.load_palette
        )

        # HELP MENU

        help_menu = menu_bar.addMenu("Help")

        about_action = QAction(
            "About",
            self
        )

        about_action.setMenuRole(
            QAction.MenuRole.NoRole
        )

        about_action.triggered.connect(
            self.show_about
        )

        help_menu.addAction(about_action)
        
        view_menu = menu_bar.addMenu("View")
        
        view_16 = view_menu.addAction(
            "16 × 16 Tiles"
        )
        view_16.triggered.connect(
            lambda: self.tile_view.set_grid_size(16)
        )

        view_32 = view_menu.addAction(
            "32 × 32 Tiles"
        )
        view_32.triggered.connect(
            lambda: self.tile_view.set_grid_size(32)
        )

        view_64 = view_menu.addAction(
            "64 × 64 Tiles"
        )
        view_64.triggered.connect(
            lambda: self.tile_view.set_grid_size(64)
        )
        
        zoom_50 = view_menu.addAction("50%")
        zoom_50.triggered.connect(
            lambda: self.tile_view.set_zoom(2)
        )

        zoom_100 = view_menu.addAction("100%")
        zoom_100.triggered.connect(
            lambda: self.tile_view.set_zoom(4)
        )

        zoom_200 = view_menu.addAction("200%")
        zoom_200.triggered.connect(
            lambda: self.tile_view.set_zoom(8)
        )

        zoom_400 = view_menu.addAction("400%")
        zoom_400.triggered.connect(
            lambda: self.tile_view.set_zoom(16)
        )
        
        view_menu.addSeparator()

        grid_action = view_menu.addAction(
            "Show Grid"
        )

        grid_action.setCheckable(True)
        grid_action.setChecked(True)
        
        grid_action.setShortcut(
            "G"
        )

        grid_action.triggered.connect(
            
            self.tile_view.toggle_grid
        )

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open CHR or NES File",
            "",
            (
                "NES Files (*.nes);;"
                "CHR Files (*.chr);;"
                "All Files (*)"
            )
        )

        if filename:
            self.current_file = filename
            self.tile_view.load_chr(filename)

    def select_tile(self, index):
        if 0 <= index < len(
            self.tile_view.tiles
        ):
            self.current_tile_index = index

            self.tile_editor.set_tile(
                self.tile_view.tiles[index]
            )
            
            self.update_status()

    def tile_modified(self):
        if self.current_tile_index < 0:
            return

        self.tile_view.tiles[
            self.current_tile_index
        ] = self.tile_editor.get_tile_copy()

        self.tile_view.update()

    def copy_tile(self):
        self.clipboard_tile = (
            self.tile_editor.get_tile_copy()
        )

    def paste_tile(self):
        if self.clipboard_tile:
            self.tile_editor.set_tile_copy(
                self.clipboard_tile
            )

            self.tile_modified()

    def clear_tile(self):
        self.push_undo()
        
        self.tile_editor.clear_tile()
        
        self.tile_modified()

    def flip_horizontal(self):
        self.push_undo()
        
        self.tile_editor.flip_horizontal()
        
        self.tile_modified()

    def flip_vertical(self):
        self.push_undo()
        
        self.tile_editor.flip_vertical()
        
        self.tile_modified()

    def save_palette(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Palette",
            "",
            "Palette Files (*.pal)"
        )

        if filename:
            self.tile_editor.save_palette(
                filename
            )

    def load_palette(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Palette",
            "",
            "Palette Files (*.pal)"
        )

        if filename:
            self.tile_editor.load_palette(
                filename
            )

    def show_about(self):
        QMessageBox.about(
            self,
            "About CHR Forge",
            (
                "CHR Forge\n\n"
                "A NES CHR and ROM editor "
                "for macOS.\n\n"
                "Features:\n"
                "- Open .nes and .chr files\n"
                "- Edit CHR tiles\n"
                "- Custom palettes\n"
                "- Save palettes (.pal)\n"
                "- Save ROMs\n\n"
                "Version 0.2 (Development)"
            )
        )

    def save_rom(self):
        if not self.current_file:
            return

        if not self.current_file.lower().endswith(
            ".nes"
        ):
            QMessageBox.warning(
                self,
                "Save ROM",
                "Current file is not a NES ROM."
            )
            return

        with open(
            self.current_file,
            "rb"
        ) as f:
            rom = bytearray(f.read())

        prg_banks = rom[4]
        chr_banks = rom[5]

        if chr_banks == 0:
            QMessageBox.warning(
                self,
                "Save ROM",
                "CHR RAM ROMs are not supported."
            )
            return

        prg_size = prg_banks * 16384
        chr_offset = 16 + prg_size

        for i, tile in enumerate(
            self.tile_view.tiles
        ):
            encoded = encode_tile(tile)

            start = (
                chr_offset +
                (i * 16)
            )

            rom[start:start + 16] = (
                encoded
            )

        filename, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Save ROM",
                "",
                "NES Files (*.nes)"
            )
        )
    def save_chr(self):
        if not self.tile_view.tiles:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save CHR",
            "",
            "CHR Files (*.chr)"
        )

        if not filename:
            return

        with open(filename, "wb") as f:
            for tile in self.tile_view.tiles:
                f.write(
                    encode_tile(tile)
                )
                
    def undo(self):
        if not self.undo_stack:
            return

        current = self.tile_editor.get_tile_copy()

        self.redo_stack.append(current)

        tile = self.undo_stack.pop()

        self.tile_editor.set_tile_copy(tile)

        self.tile_modified()
        
        print("Undo")


    def redo(self):
        if not self.redo_stack:
            return

        current = self.tile_editor.get_tile_copy()

        self.undo_stack.append(current)

        tile = self.redo_stack.pop()

        self.tile_editor.set_tile_copy(tile)

        self.tile_modified() 
        
        print("Redo")
        
    def change_edit_size(self, text):
        size = int(text.split("×")[0])

        self.tile_editor.set_edit_size(size)    
        
    def update_status(
        self,
        pixel_x=None,
        pixel_y=None,
        color=None
    ):
        if self.current_tile_index < 0:
            return

        tile_hex = (
            f"${self.current_tile_index:02X}"
        )

        text = f"Tile: {tile_hex}"

        if pixel_x is not None:
            text += (
                f"    Pixel: "
                f"({pixel_x},{pixel_y})"
            )

        if color is not None:
            text += (
            f"    Color: {color}"
        )

        self.statusBar().showMessage(text)
        
    def pixel_selected(
        self,
        x,
        y,
        color
    ):
        self.update_status(
            x,
            y,
            color
        )                    