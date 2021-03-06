#!/usr/bin/env python3
import dropbox
import requests
import time
import subprocess
from secrets import TOKEN
import logging


logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s')
LOG = logging.getLogger('dropbox-tool')
LOG.setLevel(logging.DEBUG)


class Watcher:
    def __init__(self, watch_file, command, local_path, upload_file,
            upload_path, rate):
        """Creates a watcher to run commands when file updates

        :param watch_file: the file to watch, in format
            '/root_dropbox_folder/path/to/file'
        :param command: a list of strings to run in the command line
        :param local_path: the local path to download the watch_file to (must
            be a filename)
        :param upload_file: the local path file to the file to upload
        :param upload_path: the location in dropbox to upload the resulting
            file to
        :param rate: number of seconds between checks
        :returns: new Watcher
        :rtype: Watcher

        """
        self.watch_file = watch_file
        self.command = command
        self.local_path = local_path
        self.upload_file = upload_file
        self.upload_path = upload_path
        self.rate = rate
        self.hash = None

    def run(self):
        while True:
            time.sleep(self.rate)
            hash = self._get_hash()
            if self.hash != hash:
                if self.hash is None:
                    LOG.info('no previous hash to compare, triggering action')
                else:
                    LOG.info('hash changed')
                self._download()
                self._do_command()
                self._upload()
            else:
                LOG.debug('hash did not change')
            self.hash = hash

    def _download(self):
        self.dropbox.files_download_to_file(self.local_path, self.watch_file)

    def _upload(self):
        with open(self.upload_file, 'rb') as ft:
            self.dropbox.files_upload(ft.read(), self.upload_path,
                                      mode=dropbox.files.WriteMode.overwrite)

    def _do_command(self):
        subprocess.run(self.command)

    def _get_hash(self):
        self.dropbox = dropbox.dropbox.Dropbox(TOKEN)
        return self.dropbox.files_get_metadata(self.watch_file).content_hash


def start():
    w = Watcher(
        watch_file='/Life/todo/todo.org',
        command=['emacs', 'runtime/todo.org', '--batch', '-f',
                'org-html-export-to-html', '--kill'],
        local_path='./runtime/todo.org',
        upload_file='./runtime/todo.html',
        upload_path='/Life/todo/todo.html',
        rate=5
    )
    w.run()


def main():
    while True:
        try:
            start()
        except (KeyboardInterrupt, SystemExit):
            LOG.info('Exiting on Keyboard Interrupt')
            return()
        except Exception as e:
            LOG.exception("Logging an uncaught exception", e)
            LOG.info('retrying in 30 seconds')
            time.sleep(30)


if __name__ == '__main__':
    main()
