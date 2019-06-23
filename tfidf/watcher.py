import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher():
    DIRECTORY_TO_WATCH = ''

    def __init__(self, dirPath, callback):
        self.observer = Observer()
        self.DIRECTORY_TO_WATCH = dirPath
        self.callback = callback

    def run(self):
        event_handler = Handler(self.callback)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH,recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "Error"
        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        
    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            self.callback(event.src_path)
