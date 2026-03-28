import cv2
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import ipywidgets as widgets
import numpy as np
from matplotlib.backend_bases import MouseButton

# Ieslēdz interaktīvo režīmu
%matplotlib notebook

class ZoneDrawerColab:
    def __init__(self, frame):
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.polygons = []
        self.current_points = []
        self.drawing = True
        
        # Izveido figūru
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.imshow(self.frame)
        self.ax.set_title("Klikšķini, lai pievienotu punktus")
        
        # Pievieno notikumu apstrādātājus
        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        
        # Saglabā zīmētos elementus
        self.current_line = None
        self.current_scatter = None
        self.polygon_lines = []
        
        plt.show()
    
    def on_click(self, event):
        if event.xdata is not None and event.ydata is not None and event.inaxes:
            if self.drawing:
                self.current_points.append((event.xdata, event.ydata))
                self.update_drawing()
                print(f"Pievienots punkts: ({event.xdata:.1f}, {event.ydata:.1f})")
    
    def on_key(self, event):
        if event.key == 'enter':
            if len(self.current_points) >= 3:
                self.polygons.append(self.current_points.copy())
                self.current_points = []
                self.update_drawing()
                print(f"Poligons pabeigts! Kopā poligoni: {len(self.polygons)}")
            else:
                print("Nepieciešami vismaz 3 punkti!")
                
        elif event.key == 'z':
            if self.current_points:
                self.current_points.pop()
                self.update_drawing()
                print("Pēdējais punkts atcelts")
                
        elif event.key == 'c':
            self.current_points = []
            self.polygons = []
            self.update_drawing()
            print("Viss notīrīts")
    
    def update_drawing(self):
        # Notīra esošos zīmējumus
        if self.current_line:
            self.current_line.remove()
        if self.current_scatter:
            self.current_scatter.remove()
        
        # Zīmē pabeigtos poligonus
        for line in self.polygon_lines:
            line.remove()
        self.polygon_lines.clear()
        
        for poly in self.polygons:
            xs, ys = zip(*poly)
            # Aizver poligonu
            xs = list(xs) + [xs[0]]
            ys = list(ys) + [ys[0]]
            line, = self.ax.plot(xs, ys, 'b-', linewidth=2, marker='o', markersize=6)
            self.polygon_lines.append(line)
            # Iekrāso
            self.ax.fill(xs, ys, alpha=0.3, color='blue')
        
        # Zīmē esošo poligonu
        if len(self.current_points) > 0:
            xs, ys = zip(*self.current_points)
            self.current_line, = self.ax.plot(xs, ys, 'r-', linewidth=2)
            self.current_scatter = self.ax.scatter(xs, ys, c='red', s=50, zorder=5)
            
            # Parāda savienojumu ar pirmo punktu
            if len(self.current_points) >= 3:
                first_x, first_y = self.current_points[0]
                self.ax.plot([xs[-1], first_x], [ys[-1], first_y], 'r--', alpha=0.5)
        
        self.fig.canvas.draw()
    
    def get_polygons(self):
        return self.polygons


# Alternatīva versija ar pogām - stabilāka Colab
def draw_zones_with_controls(video_path):
    """Versija ar atsevišķām pogām - visstabilākā Colab"""
    
    # Nolasa video pirmo kadru
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise ValueError("Cannot read video")
    
    # Pārveido uz RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Globālie mainīgie
    polygons = []
    current_points = []
    
    # Izveido figūru
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(frame_rgb)
    ax.set_title("Klikšķini uz attēla, lai pievienotu punktus")
    
    # Saglabā zīmējumus
    current_line = None
    current_scatter = None
    polygon_elements = []
    
    def update_display():
        nonlocal current_line, current_scatter, polygon_elements
        
        # Notīra esošos elementus
        if current_line:
            current_line.remove()
        if current_scatter:
            current_scatter.remove()
        
        for elem in polygon_elements:
            elem.remove()
        polygon_elements.clear()
        
        # Zīmē pabeigtos poligonus
        for poly in polygons:
            xs, ys = zip(*poly)
            xs = list(xs) + [xs[0]]
            ys = list(ys) + [ys[0]]
            line, = ax.plot(xs, ys, 'b-', linewidth=2, marker='o', markersize=6)
            fill = ax.fill(xs, ys, alpha=0.3, color='blue')
            polygon_elements.extend([line] + list(fill))
        
        # Zīmē esošo poligonu
        if len(current_points) > 0:
            xs, ys = zip(*current_points)
            current_line, = ax.plot(xs, ys, 'r-', linewidth=2)
            current_scatter = ax.scatter(xs, ys, c='red', s=50, zorder=5)
            
            if len(current_points) >= 3:
                first_x, first_y = current_points[0]
                dash_line, = ax.plot([xs[-1], first_x], [ys[-1], first_y], 'r--', alpha=0.5)
                polygon_elements.append(dash_line)
        
        fig.canvas.draw()
    
    def on_click(event):
        if event.xdata is not None and event.ydata is not None and event.inaxes:
            current_points.append((event.xdata, event.ydata))
            update_display()
            print(f"Punkts {len(current_points)}: ({event.xdata:.1f}, {event.ydata:.1f})")
    
    def finish_polygon(b):
        nonlocal current_points
        if len(current_points) >= 3:
            polygons.append(current_points.copy())
            current_points = []
            update_display()
            print(f"Poligons pabeigts! Kopā poligoni: {len(polygons)}")
        else:
            print(f"Nepieciešami vismaz 3 punkti (pašlaik: {len(current_points)})")
    
    def undo_point(b):
        nonlocal current_points
        if current_points:
            current_points.pop()
            update_display()
            print(f"Punkts atcelts. Atlikušas {len(current_points)} punkti")
    
    def clear_all(b):
        nonlocal current_points, polygons
        current_points = []
        polygons = []
        update_display()
        print("Viss notīrīts")
    
    # Pievieno klikšķu notikumu
    fig.canvas.mpl_connect('button_press_event', on_click)
    
    # Izveido pogas
    finish_btn = widgets.Button(
        description="✓ Pabeigt poligonu (Enter)", 
        button_style='success',
        layout=widgets.Layout(width='200px')
    )
    finish_btn.on_click(finish_polygon)
    
    undo_btn = widgets.Button(
        description="↶ Atsaukt punktu (Z)", 
        button_style='warning',
        layout=widgets.Layout(width='200px')
    )
    undo_btn.on_click(undo_point)
    
    clear_btn = widgets.Button(
        description="✗ Notīrīt visu (C)", 
        button_style='danger',
        layout=widgets.Layout(width='200px')
    )
    clear_btn.on_click(clear_all)
    
    # Rāda figūru un pogas
    display(widgets.HBox([finish_btn, undo_btn, clear_btn]))
    plt.show()
    
    return polygons


# Vienkāršākā versija - izmanto tikai pogas, bez taustiņiem
def draw_zones_simple(video_path):
    """Vienkāršākā versija - darbojas garantēti Colab"""
    
    # Nolasa video
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise ValueError("Cannot read video")
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Globālie mainīgie
    polygons = []
    current_points = []
    
    # Izveido figūru
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(frame_rgb)
    ax.set_title("Klikšķini, lai pievienotu punktus")
    
    points_list = []  # Saglabā punktu marķierus
    
    def update_display():
        ax.clear()
        ax.imshow(frame_rgb)
        
        # Zīmē pabeigtos poligonus
        for poly in polygons:
            xs, ys = zip(*poly)
            xs = list(xs) + [xs[0]]
            ys = list(ys) + [ys[0]]
            ax.plot(xs, ys, 'b-', linewidth=2, marker='o', markersize=6)
            ax.fill(xs, ys, alpha=0.3, color='blue')
        
        # Zīmē esošo poligonu
        if len(current_points) > 0:
            xs, ys = zip(*current_points)
            ax.plot(xs, ys, 'r-', linewidth=2, marker='o', markersize=6, markerfacecolor='red')
            
            if len(current_points) >= 3:
                first_x, first_y = current_points[0]
                ax.plot([xs[-1], first_x], [ys[-1], first_y], 'r--', alpha=0.5)
        
        ax.set_title(f"Punkti: {len(current_points)} | Poligoni: {len(polygons)}")
        fig.canvas.draw()
    
    def on_click(event):
        if event.xdata is not None and event.ydata is not None:
            current_points.append((event.xdata, event.ydata))
            update_display()
            print(f"Pievienots punkts {len(current_points)}")
    
    def finish_polygon(b):
        if len(current_points) >= 3:
            polygons.append(current_points.copy())
            current_points.clear()
            update_display()
            print(f"Poligons pabeigts! Kopā: {len(polygons)}")
        else:
            print(f"Vajag vismaz 3 punktus (ir {len(current_points)})")
    
    def reset_all(b):
        current_points.clear()
        polygons.clear()
        update_display()
        print("Viss notīrīts")
    
    # Pievieno notikumu
    fig.canvas.mpl_connect('button_press_event', on_click)
    
    # Izveido pogas
    finish_btn = widgets.Button(description="Pabeigt poligonu")
    finish_btn.on_click(finish_polygon)
    
    reset_btn = widgets.Button(description="Notīrīt visu")
    reset_btn.on_click(reset_all)
    
    display(widgets.HBox([finish_btn, reset_btn]))
    plt.show()
    
    return polygons


# Lietošana Colab:
# ================
# Izmanto vienu no funkcijām:

# 1. Vienkāršākā versija (ieteicama):
# zones = draw_zones_simple("jūsu_video.mp4")

# 2. Versija ar vairāk pogām:
# zones = draw_zones_with_controls("jūsu_video.mp4")

# Pēc zīmēšanas zonas būs saglabātas mainīgajā 'zones'
