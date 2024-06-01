import tkinter as tk
from tkinter import Canvas

# 棋盘大小
BOARD_SIZE = 8
SQUARE_SIZE = 60

class ChessGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Chess Game")
        self.geometry(f"{BOARD_SIZE * SQUARE_SIZE}x{BOARD_SIZE * SQUARE_SIZE}")

        self.canvas = Canvas(self, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE)
        self.canvas.pack()

        self.draw_board()
        self.place_pieces()
        self.selected_piece = None

        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = 'white' if (row + col) % 2 == 0 else 'gray'
                self.canvas.create_rectangle(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                             (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                                             fill=color)

    def place_pieces(self):
        self.pieces = {}
        initial_positions = {
            'R': [(0, 0), (0, 7), (7, 0), (7, 7)],
            'N': [(0, 1), (0, 6), (7, 1), (7, 6)],
            'B': [(0, 2), (0, 5), (7, 2), (7, 5)],
            'Q': [(0, 3), (7, 3)],
            'K': [(0, 4), (7, 4)],
            'P': [(1, col) for col in range(BOARD_SIZE)] + [(6, col) for col in range(BOARD_SIZE)]
        }

        for piece, positions in initial_positions.items():
            for pos in positions:
                row, col = pos
                color = 'black' if row < BOARD_SIZE // 2 else 'black'
                self.pieces[(row, col)] = self.canvas.create_text(
                    col * SQUARE_SIZE + SQUARE_SIZE // 2,
                    row * SQUARE_SIZE + SQUARE_SIZE // 2,
                    text=piece, fill=color, font=('Arial', 24)
                )

    def on_click(self, event):
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        if (row, col) in self.pieces:
            if self.selected_piece:
                self.canvas.itemconfig(self.pieces[self.selected_piece], fill='black' if self.selected_piece[0] < BOARD_SIZE // 2 else 'black')
            self.selected_piece = (row, col)
            self.canvas.itemconfig(self.pieces[self.selected_piece], fill='red')
        elif self.selected_piece:
            self.move_piece(self.selected_piece, (row, col))

    def move_piece(self, from_pos, to_pos):
        piece = self.pieces.pop(from_pos)
        self.canvas.coords(piece,
                           to_pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2,
                           to_pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2)
        self.pieces[to_pos] = piece
        self.selected_piece = None

if __name__ == "__main__":
    game = ChessGame()
    game.mainloop()
