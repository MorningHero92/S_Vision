import cv2
import matplotlib.pyplot as plt
from IPython.display import display
import ipywidgets as widgets
from IPython.display import clear_output
import numpy as np


class ZoneDrawerColab:
    def __init__(self, frame):
        self.original_frame = frame
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.polygons = []
        self.current_points = []
        self.selected_point = None
        self.drag_mode = False
        
        # Izveido interaktīvo figūru
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.fig.canvas.toolbar_visible = False
        self.fig.canvas.header_visible = False
        self.fig.canvas.footer_visible = False
        
        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        
        self.redraw()
        
    def on_press(self, event):
        if event.xdata is None or event.ydata is None:
            return
            
        if event.button == 1:  # Kreisā poga
            # Pārbauda vai noklikšķināts uz esoša punkta
            if self.current_points:
                for i, (x, y) in enumerate(self.current_points):
                    if abs(x - event.xdata) < 5 and abs(y - event.ydata) < 5:
                        self.selected_point = i
                        self.drag_mode = True
                        return
            
            # Ja nav klikšķināts uz punkta, pievieno jaunu punktu
            self.current_points.append((event.xdata, event.ydata))
            self.redraw()
            
    def on_release(self, event):
        self.drag_mode = False
        self.selected_point = None
        
    def on_motion(self, event):
        if self.drag_mode and self.selected_point is not None and event.xdata is not None:
            self.current_points[self.selected_point] = (event.xdata, event.ydata)
            self.redraw()
        
    def on_key(self, event):
        if event.key == 'z':  # Undo pēdējo punktu
            if self.current_points:
                self.current_points.pop()
            self.redraw()
            
        elif event.key == 'enter':  # Pabeidz poligonu
            if len(self.current_points) >= 3:
                self.polygons.append(self.current_points.copy())
                self.current_points = []
            self.redraw()
            
        elif event.key == 'c':  # Notīra visu
            self.current_points = []
            self.polygons = []
            self.redraw()
            
    def redraw(self):
        self.ax.clear()
        self.ax.imshow(self.frame)
        
        # Zīmē pabeigtos poligonus
        for poly in self.polygons:
            xs, ys = zip(*poly)
            xs = list(xs) + [xs[0]]
            ys = list(ys) + [ys[0]]
            self.ax.plot(xs, ys, 'b-', linewidth=2)
            self.ax.scatter(xs[:-1], ys[:-1], c='blue', s=50, zorder=5)
            
            # Iekrāso poligonu
            self.ax.fill(xs, ys, alpha=0.3, color='blue')
        
        # Zīmē esošo poligonu
        if len(self.current_points) > 0:
            xs, ys = zip(*self.current_points)
            self.ax.plot(xs, ys, 'r-', linewidth=2)
            self.ax.scatter(xs, ys, c='red', s=50, zorder=5)
            
            # Parāda savienojumu ar pirmo punktu
            if len(self.current_points) >= 3:
                first_x, first_y = self.current_points[0]
                self.ax.plot([xs[-1], first_x], [ys[-1], first_y], 'r--', alpha=0.5)
        
        self.ax.set_title("Kreisā poga: pievienot/vilkt punktu | Z: atcelt | Enter: pabeigt | C: notīrīt")
        self.fig.canvas.draw()
        
    def get_polygons(self):
        return self.polygons


def draw_zones_from_video_colab(video_path):
    """Funkcija zonas zīmēšanai Google Colab"""
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise ValueError("Cannot read video")
    
    # Samazina kadru ja pārāk liels
    height, width = frame.shape[:2]
    max_size = 800
    if height > max_size or width > max_size:
        scale = max_size / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        frame = cv2.resize(frame, (new_width, new_height))
    
    drawer = ZoneDrawerColab(frame)
    plt.show()
    
    return drawer.get_polygons()


# Alternatīvs risinājums - izmanto ipywidgets pogas
def draw_zones_with_buttons(video_path):
    """Versija ar pogām, kas var būt stabilāka Colab"""
    
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise ValueError("Cannot read video")
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    polygons = []
    current_points = []
    
    # Izveido figūru
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(frame_rgb)
    
    img_display = ax.imshow(frame_rgb)
    points_scatter = ax.scatter([], [], c='red', s=50)
    lines = []
    
    def update_display():
        nonlocal lines
        # Notīra vecās līnijas
        for line in lines:
            line.remove()
        lines.clear()
        
        # Zīmē esošo poligonu
        if len(current_points) > 0:
            xs, ys = zip(*current_points)
            line, = ax.plot(xs, ys, 'r-', linewidth=2)
            lines.append(line)
            points_scatter.set_offsets(np.array(current_points))
            
            # Parāda savienojumu ar pirmo punktu
            if len(current_points) >= 3:
                first_x, first_y = current_points[0]
                dash_line, = ax.plot([xs[-1], first_x], [ys[-1], first_y], 'r--', alpha=0.5)
                lines.append(dash_line)
        else:
            points_scatter.set_offsets(np.empty((0, 2)))
        
        # Zīmē pabeigtos poligonus
        for poly in polygons:
            xs, ys = zip(*poly)
            xs = list(xs) + [xs[0]]
            ys = list(ys) + [ys[0]]
            line, = ax.plot(xs, ys, 'b-', linewidth=2)
            lines.append(line)
            ax.fill(xs, ys, alpha=0.3, color='blue')
        
        fig.canvas.draw()
    
    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            current_points.append((event.xdata, event.ydata))
            update_display()
    
    def finish_polygon(b):
        if len(current_points) >= 3:
            polygons.append(current_points.copy())
            current_points.clear()
            update_display()
    
    def undo_last(b):
        if current_points:
            current_points.pop()
            update_display()
    
    def clear_all(b):
        current_points.clear()
        polygons.clear()
        update_display()
    
    # Pievieno notikumu apstrādātāju
    fig.canvas.mpl_connect('button_press_event', onclick)
    
    # Izveido pogas
    finish_btn = widgets.Button(description="Pabeigt poligonu")
    finish_btn.on_click(finish_polygon)
    
    undo_btn = widgets.Button(description="Atsaukt punktu")
    undo_btn.on_click(undo_last)
    
    clear_btn = widgets.Button(description="Notīrīt visu")
    clear_btn.on_click(clear_all)
    
    # Rāda figūru un pogas
    display(widgets.HBox([finish_btn, undo_btn, clear_btn]))
    plt.show()
    
    return polygons


# Lietošanas piemērs
if __name__ == "__main__":
    # Izmanto vienu no metodēm:
    # polygons = draw_zones_from_video_colab(source_video)
    # polygons = draw_zones_with_buttons(source_video)
    pass
