import yaml
from tempfile import NamedTemporaryFile

def get_tracker_yaml(**kwargs):
    """
    Создаёт временный YAML-файл с настройками трекера,
    используя переданные параметры, и возвращает путь к нему.
    """
    # 1️⃣ Базовые настройки (по умолчанию)
    tracker_config = {
        "tracker_type": "botsort",
        "max_age": 30,
        "min_hits": 3,
        "iou_threshold": 0.5,
        "high_confidence_threshold": 0.6
    }

    # 2️⃣ Обновляем их теми, что передали извне
    tracker_config.update(kwargs)

    # 3️⃣ Создаём временный YAML-файл
    with NamedTemporaryFile(mode="w+", suffix=".yaml", delete=False) as f:
        yaml.dump(tracker_config, f)
        tracker_yaml_path = f.name

    return tracker_yaml_path
