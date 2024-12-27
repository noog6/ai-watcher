import threading
import time

class EventHandler:
    def __init__(self):
        self.event_queue = []
        self.lock = threading.Lock()

    def add_event(self, event):
        with self.lock:
            self.event_queue.append(event)

    def process_events(self):
        while True:
            with self.lock:
                if self.event_queue:
                    event = self.event_queue.pop(0)
                    self.handle_event(event)
            time.sleep(0.1)

    def handle_event(self, event):
        # Implement event handling logic here
        print(f"Handling event: {event}")

class AudioEventHandler(EventHandler):
    def handle_event(self, event):
        # Implement audio-specific event handling
        print(f"Handling audio event: {event}")

class CameraEventHandler(EventHandler):
    def handle_event(self, event):
        # Implement camera-specific event handling
        print(f"Handling camera event: {event}")

class ServoEventHandler(EventHandler):
    def handle_event(self, event):
        # Implement servo-specific event handling
        print(f"Handling servo event: {event}")
