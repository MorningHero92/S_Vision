import cv2
import matplotlib.pyplot as plt
from IPython.display import display
import ipywidgets as widgets
import numpy as np

def draw_zones_simple(video_path):
    """Vienkārša zonas zīmēšana Colab"""
    
    # Nolasa video
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
        if event.xdata is not None and event.ydata is not None and event.inaxes:
            current_points.append((event.xdata, event.ydata))
            update_display()
            print(f"✓ Pievienots punkts {len(current_points)}: ({event.xdata:.0f}, {event.ydata:.0f})")
    
    def finish_polygon(b):
        if len(current_points) >= 3:
            polygons.append(current_points.copy())
            current_points.clear()
            update_display()
            print(f"✓ Poligons pabeigts! Kopā poligoni: {len(polygons)}")
        else:
            print(f"❌ Vajag vismaz 3 punktus (pašlaik: {len(current_points)})")
    
    def undo_point(b):
        if current_points:
            current_points.pop()
            update_display()
            print(f"↶ Pēdējais punkts atcelts. Atlikuši {len(current_points)} punkti")
        else:
            print("Nav ko atcelt")
    
    def clear_all(b):
        current_points.clear()
        polygons.clear()
        update_display()
        print("✓ Viss notīrīts")
    
    # Pievieno klikšķu notikumu
    fig.canvas.mpl_connect('button_press_event', on_click)
    
    # Izveido pogas
    finish_btn = widgets.Button(
        description="✓ Pabeigt poligonu", 
        button_style='success',
        layout=widgets.Layout(width='180px')
    )
    finish_btn.on_click(finish_polygon)
    
    undo_btn = widgets.Button(
        description="↶ Atsaukt punktu", 
        button_style='warning',
        layout=widgets.Layout(width='180px')
    )
    undo_btn.on_click(undo_point)
    
    clear_btn = widgets.Button(
        description="✗ Notīrīt visu", 
        button_style='danger',
        layout=widgets.Layout(width='180px')
    )
    clear_btn.on_click(clear_all)
    
    # Rāda figūru un pogas
    print("=" * 50)
    print("INSTRUKCIJA:")
    print("1. Klikšķini uz attēla, lai pievienotu punktus")
    print("2. Pēc 3+ punktiem spied 'Pabeigt poligonu'")
    print("3. Spied 'Atsaukt punktu', lai izdzēstu pēdējo punktu")
    print("4. Spied 'Notīrīt visu', lai sāktu no jauna")
    print("=" * 50)
    
    display(widgets.HBox([finish_btn, undo_btn, clear_btn]))
    plt.show()
    
    return polygons

# ============================================
# LIETOŠANA:
# ============================================

# Ielādē video (aizstāj ar savu video ceļu)
source_video = "/content/sample_video.mp4"  # Ievietojiet šeit savu video ceļu

# Palaist zīmēšanu
zones = draw_zones_simple(source_video)

# Pēc zīmēšanas beigām varat apskatīt rezultātu
print("\n" + "=" * 50)
print(f"Iegūtās zonas: {len(zones)} poligoni")
print(zones)
