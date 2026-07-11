from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import pyqtSignal

from chr import load_tiles


class TileView(QWidget):
    tileSelected = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.tiles = []
        self.selected_tile = -1
        
        self.tiles_per_row = 16
        self.scale = 4
        
        self.show_grid = True

        self.palette = [
            QColor(0, 0, 0),
            QColor(90, 90, 90),
            QColor(180, 180, 180),
            QColor(255, 255, 255)
        ]

        self.setMinimumSize(512, 512)

    def load_chr(self, filename):
        self.tiles = load_tiles(filename)
        self.update()

    def mousePressEvent(self, event):
        tile_size = 8 * self.scale

        col = int(event.position().x()) // tile_size
        row = int(event.position().y()) // tile_size

        tile_index = (
            row * self.tiles_per_row
            + col
        )

        if 0 <= tile_index < len(self.tiles):
            self.selected_tile = tile_index
            self.tileSelected.emit(tile_index)
            self.update()
            
    def set_grid_size(self, size):
        self.tiles_per_row = size
        self.update()        

    def paintEvent(self, event):
        painter = QPainter(self)

        scale = self.scale
        tile_size = 8 * scale

        for i, tile in enumerate(self.tiles):
            tx = (i % self.tiles_per_row) * tile_size
            ty = (i // self.tiles_per_row) * tile_size

            for y in range(8):
                for x in range(8):
                    color = self.palette[tile[y][x]]

                    painter.fillRect(
                        tx + x * scale,
                        ty + y * scale,
                        scale,
                        scale,
                        color
                    )
                    
            if self.show_grid:
                painter.setPen(
                QPen(QColor(80, 80, 80))
            )

            for y in range(9):
                painter.drawLine(
                tx,
                ty + y * scale,
                tx + tile_size,
                ty + y * scale
            )

            for x in range(9):
                painter.drawLine(
                tx + x * scale,
                ty,
                tx + x * scale,
                ty + tile_size
            )        

            if i == self.selected_tile:
                painter.setPen(QPen(QColor(255, 0, 0), 2))
                painter.drawRect(
                    tx,
                    ty,
                    tile_size - 1,
                    tile_size - 1
                )
                
    def toggle_grid(self):
        self.show_grid = not self.show_grid
        self.update()            
    def set_zoom(self, scale):
        self.scale = scale

        tile_size = 8 * scale

        rows = (
            len(self.tiles)
            + self.tiles_per_row
            - 1
        ) // self.tiles_per_row

        self.resize(
            self.tiles_per_row * tile_size,
            rows * tile_size
        )

        self.update()          