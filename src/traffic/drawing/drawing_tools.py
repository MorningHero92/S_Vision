import cv2
import matplotlib.pyplot as plt


class ZoneDrawer:
    def __init__(self, frame):
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.polygons = []
        self.current_points = []

        self.fig = None

    def onclick(self, event):
        if event.xdata is not None and event.ydata is not None:
            self.current_points.append((event.xdata, event.ydata))
            self.redraw()

    def onkey(self, event):
        # Undo
        if event.key == 'z':
            if self.current_points:
                self.current_points.pop()
            self.redraw()

        # Finish polygon
        elif event.key == 'enter':
            if len(self.current_points) >= 3:
                self.polygons.append(self.current_points.copy())
                self.current_points.clear()
            self.redraw()

        # Clear all
        elif event.key == 'c':
            self.current_points.clear()
            self.polygons.clear()
            self.redraw()

    def redraw(self):
        plt.clf()
        plt.imshow(self.frame)

        # Draw finished polygons
        for poly in self.polygons:
            xs, ys = zip(*poly)
            xs = list(xs) + [xs[0]]
            ys = list(ys) + [ys[0]]

            plt.plot(xs, ys)
            plt.scatter(xs, ys)

        # Draw current polygon
        if len(self.current_points) > 0:
            xs, ys = zip(*self.current_points)
            plt.plot(xs, ys)
            plt.scatter(xs, ys)

        plt.title("Click: add point | Z: undo | Enter: finish polygon | C: clear")
        plt.draw()

    def run(self):
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('key_press_event', self.onkey)

        plt.imshow(self.frame)
        plt.show()

        return self.polygons


def draw_zones_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise ValueError("Cannot read video")

    drawer = ZoneDrawer(frame)
    polygons = drawer.run()

    return polygons
