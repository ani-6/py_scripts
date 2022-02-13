import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os.path
from datetime import datetime

dir= "../Pictures/"
logfile_name = dir + "log.txt"
#check if logfile exists
file_exists = os.path.exists(logfile_name)
if file_exists == False:
    f= open(logfile_name, "w")
    print("New logfile created in working directory")
else:
    print("Log file already exists. Appending logs in same file")

logfile = open(logfile_name,'a')
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %I:%M:%S %p")
logfile.write("\n------------------------------------------------------\n")
logfile.write(f"Log generation date and time = {dt_string} \n")
logfile.write("------------------------------------------------------\n\n")


class Watcher:
    DIRECTORY_TO_WATCH = dir

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            #print(event.src_path)
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            log = f"File created - {event.src_path} "
            lognow = datetime.now()
            print(log)
            logfile.write(lognow.strftime("%I:%M:%S %p "))
            logfile.write(log + '\n')

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            log = f"File modified -{event.src_path} "
            lognow = datetime.now()
            print(log)
            logfile.write(lognow.strftime("%I:%M:%S %p "))
            logfile.write(log + '\n')
        
        elif event.event_type == 'deleted':
            # Taken any action here when a file is deleted.
            log = f"File deleted - {event.src_path} "
            lognow = datetime.now()
            print(log)
            logfile.write(lognow.strftime("%I:%M:%S %p "))
            logfile.write(log + '\n')
        
        elif event.event_type == 'moved':
            log = f"File moved - {event.src_path} to {event.dest_path} "
            lognow = datetime.now()
            print(log)
            logfile.write(lognow.strftime("%I:%M:%S %p "))
            logfile.write(log + '\n')


if __name__ == '__main__':
    w = Watcher()
    w.run()
