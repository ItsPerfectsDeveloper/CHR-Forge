from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import pyqtSignal


class TileEditor(QWidget):
    tileChanged = pyqtSignal()
    pixelSelected = pyqtSignal(
        int,
        int,
        int
    )
    def __init__(self):
        super().__init__()

        self.tile = [[0 for _ in range(8)] for _ in range(8)]
        
        self.drawing = False
        
        self.edit_tile = 8

        self.palette = [
            QColor(0, 0, 0),
            QColor(85, 85, 85),
            QColor(170, 170, 170),
            QColor(255, 255, 255)
        ]

        self.current_color = 3

        self.nes_colors = [
            QColor(124, 124, 124),
            QColor(0, 0, 252),
            QColor(0, 0, 188),
            QColor(68, 40, 188),
            QColor(148, 0, 132),
            QColor(168, 0, 32),
            QColor(168, 16, 0),
            QColor(136, 20, 0),

            QColor(80, 48, 0),
            QColor(0, 120, 0),
            QColor(0, 104, 0),
            QColor(0, 88, 0),
            QColor(0, 64, 88),
            QColor(0, 0, 0),
            QColor(0, 0, 0),
            QColor(0, 0, 0),

            QColor(188, 188, 188),
            QColor(0, 120, 248),
            QColor(0, 88, 248),
            QColor(104, 68, 252),
            QColor(216, 0, 204),
            QColor(228, 0, 88),
            QColor(248, 56, 0),
            QColor(228, 92, 16),

            QColor(172, 124, 0),
            QColor(0, 184, 0),
            QColor(0, 168, 0),
            QColor(0, 168, 68),
            QColor(0, 136, 136),
            QColor(120, 120, 120),
            QColor(200, 200, 200),
            QColor(252, 252, 252)
        ]

        self.setMinimumSize(500, 340)

    def set_tile(self, tile):
        self.tile = [row[:] for row in tile]
        self.update()

    def get_tile_copy(self):
        return [row[:] for row in self.tile]

    def set_tile_copy(self, tile):
        self.tile = [row[:] for row in tile]
        self.tileChanged.emit()
        self.update()

    def clear_tile(self):
        for y in range(8):
            for x in range(8):
                self.tile[y][x] = 0

        self.tileChanged.emit()
        self.update()

    def flip_horizontal(self):
        for y in range(8):
            self.tile[y].reverse()

        self.tileChanged.emit()
        self.update()

    def flip_vertical(self):
        self.tile.reverse()

        self.tileChanged.emit()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        scale = 32

        # Tile editor
        for y in range(8):
            for x in range(8):
                color = self.palette[self.tile[y][x]]

                painter.fillRect(
                    x * scale,
                    y * scale,
                    scale,
                    scale,
                    color
                )

                painter.setPen(
                    QPen(QColor(100, 100, 100))
                )

                painter.drawRect(
                    x * scale,
                    y * scale,
                    scale,
                    scale
                )

        # Palette slots
        palette_y = 270

        for i, color in enumerate(self.palette):
            px = 20 + (i * 55)

            painter.fillRect(
                px,
                palette_y,
                40,
                40,
                color
            )

            painter.setPen(QPen(QColor(0, 0, 0)))
            painter.drawRect(
                px,
                palette_y,
                40,
                40
            )

            if i == self.current_color:
                painter.setPen(
                    QPen(QColor(255, 0, 0), 2)
                )

                painter.drawRect(
                    px - 2,
                    palette_y - 2,
                    44,
                    44
                )

        # NES color picker
        picker_x = 260
        picker_y = 20
        cell = 24

        for i, color in enumerate(self.nes_colors):
            row = i // 8
            col = i % 8

            x = picker_x + col * cell
            y = picker_y + row * cell

            painter.fillRect(
                x,
                y,
                cell,
                cell,
                color
            )

            painter.setPen(QPen(QColor(0, 0, 0)))
            painter.drawRect(
                x,
                y,
                cell,
                cell
            )

    def mousePressEvent(self, event):
        mx = int(event.position().x())
        my = int(event.position().y())

        self.drawing = True

    # Palette slot selection
        palette_y = 270

        for i in range(4):
            px = 20 + (i * 55)

            if (
                px <= mx < px + 40 and
                palette_y <= my < palette_y + 40
            ):
                self.current_color = i
                self.update()
                return

    # NES color picker
        picker_x = 260
        picker_y = 20
        cell = 24

        for i in range(len(self.nes_colors)):
            row = i // 8
            col = i % 8

            x = picker_x + col * cell
            y = picker_y + row * cell

            if (
                x <= mx < x + cell and
                y <= my < y + cell
            ):
                self.palette[self.current_color] = self.nes_colors[i]
                self.update()
                return

        self.draw_pixel(mx, my)

        def mouseMoveEvent(self, event):
            self.handle_click(event)

        def handle_click(self, event):
            mx = int(event.position().x())
            my = int(event.position().y())

            # Palette slots
            palette_y = 270

            for i in range(4):
                px = 20 + (i * 55)

                if (
                    px <= mx < px + 40 and
                    palette_y <= my < palette_y + 40
                ):
                    self.current_color = i
                    self.update()
                    return

            # NES color picker
            picker_x = 260
            picker_y = 20
            cell = 24

            for i in range(len(self.nes_colors)):
                row = i // 8
                col = i % 8

                x = picker_x + col * cell
                y = picker_y + row * cell

                if (
                    x <= mx < x + cell and
                    y <= my < y + cell
                ):
                    self.palette[self.current_color] = (
                        self.nes_colors[i]
                    )

                    self.update()
                    return

            # Tile editing
            scale = 32

            x = mx // scale
            y = my // scale

            if 0 <= x < 8 and 0 <= y < 8:
                if self.tile[y][x] != self.current_color:
                    self.tile[y][x] = self.current_color
                    self.tileChanged.emit()
                    self.update()

        def save_palette(self, filename):
            with open(filename, "w") as f:
                for color in self.palette:
                    f.write(
                        f"{color.red()} "
                        f"{color.green()} "
                        f"{color.blue()}\n"
                    )

        def load_palette(self, filename):
            with open(filename, "r") as f:
                lines = f.readlines()

            for i, line in enumerate(lines[:4]):
                r, g, b = map(
                    int,
                    line.strip().split()
                )

                self.palette[i] = QColor(
                    r,
                    g,
                    b
                )

            self.update()
            
    def draw_pixel(self, mx, my):
        scale = 32

        x = mx // scale
        y = my // scale

        if 0 <= x < 8 and 0 <= y < 8:
            self.tile[y][x] = (
                self.current_color
            )
            
            self.pixelSelected.emit(
                x,
                y,
                self.current_color
            )

            self.tileChanged.emit()

            self.update()
    def mouseMoveEvent(self, event):
        if not self.drawing:
            return

        mx = int(event.position().x())
        my = int(event.position().y())

        self.draw_pixel(mx, my)
    def mouseReleaseEvent(self, event):
        self.drawing = False 
        
    def set_edit_size(self, size):
        self.edit_size = size
        print(f"Edit size changed to {size}x{size}")                   