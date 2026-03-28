import cv2
import matplotlib.pyplot as plt
import numpy as np

class InteractiveZoneDrawer:
    def __init__(self, video_path):
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise ValueError("Не могу загрузить видео")
        
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.polygons = []
        self.current_points = []
        
        # Создаем интерактивный график
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.ax.imshow(self.frame)
        self.ax.set_title("КЛИКНИТЕ МЫШКОЙ ДЛЯ ДОБАВЛЕНИЯ ТОЧЕК | Enter - закончить | Z - отменить | C - очистить")
        
        # Подключаем события
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        
        # Сохраняем объекты для рисования
        self.current_line = None
        self.current_scatter = None
        self.polygon_fills = []
        
        self.redraw()
        plt.show()
    
    def on_click(self, event):
        # Проверяем, что клик был внутри графика
        if event.xdata is not None and event.ydata is not None and event.inaxes:
            x, y = event.xdata, event.ydata
            self.current_points.append((x, y))
            print(f"✅ Точка {len(self.current_points)}: ({x:.0f}, {y:.0f})")
            self.redraw()
    
    def on_key(self, event):
        if event.key == 'enter':  # Завершить полигон
            if len(self.current_points) >= 3:
                self.polygons.append(self.current_points.copy())
                self.current_points = []
                print(f"✅ Полигон {len(self.polygons)} завершен!")
                self.redraw()
            else:
                print(f"❌ Нужно минимум 3 точки (сейчас {len(self.current_points)})")
        
        elif event.key == 'z':  # Отменить последнюю точку
            if self.current_points:
                self.current_points.pop()
                print(f"↶ Точка удалена. Осталось {len(self.current_points)}")
                self.redraw()
        
        elif event.key == 'c':  # Очистить всё
            self.current_points = []
            self.polygons = []
            print("🗑 Всё очищено")
            self.redraw()
    
    def redraw(self):
        # Очищаем старые объекты
        self.ax.clear()
        self.ax.imshow(self.frame)
        
        # Рисуем все завершенные полигоны
        for poly in self.polygons:
            xs, ys = zip(*poly)
            xs = list(xs) + [xs[0]]
            ys = list(ys) + [ys[0]]
            self.ax.plot(xs, ys, 'b-', linewidth=2, marker='o', markersize=6)
            self.ax.fill(xs, ys, alpha=0.3, color='blue')
        
        # Рисуем текущий полигон
        if len(self.current_points) > 0:
            xs, ys = zip(*self.current_points)
            self.ax.plot(xs, ys, 'r-', linewidth=2, marker='o', markersize=6, markerfacecolor='red')
            
            # Показываем линию к первой точке
            if len(self.current_points) >= 3:
                first_x, first_y = self.current_points[0]
                self.ax.plot([xs[-1], first_x], [ys[-1], first_y], 'r--', alpha=0.5)
        
        # Добавляем подписи координат
        self.ax.set_xlabel("X координата")
        self.ax.set_ylabel("Y координата")
        self.ax.set_title(f"Точек: {len(self.current_points)} | Полигонов: {len(self.polygons)} | Кликните для добавления")
        
        self.fig.canvas.draw()
    
    def get_polygons(self):
        return self.polygons

# Использование
# Укажите путь к вашему видео
video_path = "/content/drive/MyDrive/Machine_Vision/Source_videos/Vansu_Tilts_End.mp4"  # ЗАМЕНИТЕ НА ВАШ ВИДЕОФАЙЛ

# Создаем рисовалку
drawer = InteractiveZoneDrawer(video_path)

# После закрытия окна получим результат
zones = drawer.get_polygons()
print(f"\n🎉 Получено полигонов: {len(zones)}")
print(zones)
