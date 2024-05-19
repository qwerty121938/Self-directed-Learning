import tkinter as tk
import math

class LoadingCircleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loading Circle with Variable Speed")

        self.canvas = tk.Canvas(root, width=50, height=50, bg="black")
        self.canvas.pack()

        self.center_x = 25
        self.center_y = 25
        self.radius = 25
        self.angle = 0
        self.speed = 0.02  # 提高初始速度
        self.line_length = 15  # 初始線長度
        self.line = None

        self.create_line()
        self.rotate_line()

    def create_line(self):
        self.angle_increment = self.line_length / self.radius
        self.line_points = []

        for i in range(int(self.angle_increment * 360)):
            angle = self.angle + i * (2 * math.pi / 360)
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            self.line_points.append((x, y))

        self.line = self.canvas.create_line(self.line_points, fill="white", width=2)

    def rotate_line(self):
        self.canvas.delete(self.line)
        self.angle += self.speed
        self.update_speed_and_length()

        self.line_points = []
        for i in range(int(self.angle_increment * 360)):
            angle = self.angle + i * (2 * math.pi / 360)
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            self.line_points.append((x, y))

        self.line = self.canvas.create_line(self.line_points, fill="white", width=2)
        self.root.after(20, self.rotate_line)  # 縮短定時器時間間隔

    def update_speed_and_length(self):
        # 模擬速度變化，例如正弦函數
        time_factor = (self.angle / (2 * math.pi)) % 1
        self.speed = 0.08 + 0.02 * math.sin(time_factor * 2 * math.pi)  # 提高基線速度和變化幅度
        self.line_length = 15 + 2 * math.sin(time_factor * 2 * math.pi)
        self.angle_increment = self.line_length / self.radius

if __name__ == "__main__":
    root = tk.Tk()
    app = LoadingCircleApp(root)
    root.mainloop()

