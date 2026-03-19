# src/traffic/tracking/tracker.py
class Tracker:
    def __init__(self, tracker_yaml=None):
        self.tracker_yaml = tracker_yaml
        self.persist = True  # store track IDs

    def track(self, frame, detector_results):
        results = detector_results
        return results
