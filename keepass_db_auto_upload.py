#!/usr/bin/env python3
# coding=utf-8
import platform
import time

import dropbox
from dropbox.files import WriteMode
from watchdog.events import FileSystemEventHandler, FileModifiedEvent


# add your dropbox access token
DROPBOX_ACCESS_TOKEN = ''
# the dropbox folder to store your keepass db
DROPBOX_FOLDER = ''
# add the file path of your keepass db
KEEPASS_DB_PATH = ''


class FileModifiedEventHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        if not isinstance(event, FileModifiedEvent):
            return
        if event.src_path == KEEPASS_DB_PATH + '.tmp':
            time.sleep(0.5)
            upload_to_dropbox(KEEPASS_DB_PATH)


def upload_to_dropbox(file_path):
    print('uploading...')
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    file_name = file_path.split('/')[-1]
    if DROPBOX_FOLDER:
        dropbox_path = '/{0}/{1}'.format(DROPBOX_FOLDER, file_name)
    else:
        dropbox_path = '/{0}'.format(file_name)
    with open(file_path, 'rb') as f:
        dbx.files_upload(
            f, dropbox_path, mode=WriteMode('overwrite', None))
    print('upload completed!')


def get_system_observer():
    # Only Linux and macOS are supported
    system = platform.system()
    if system == 'Linux':
        from watchdog.observers import Observer
        return Observer()
    if system == 'Darwin':
        from watchdog.observers.fsevents import FSEventsObserver
        return FSEventsObserver()
    else:
        raise Exception('System not supported!')


def get_folder_path(path):
    return '/'.join(path.split('/')[:-1])


def start_monitoring():
    observer = get_system_observer()
    event_handler = FileModifiedEventHandler()
    folder_path = get_folder_path(KEEPASS_DB_PATH)
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    start_monitoring()
