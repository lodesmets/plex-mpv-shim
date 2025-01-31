#!/usr/bin/env python3

import getpass
import queue
import logging
import sys
import time
import os.path

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format="%(asctime)s [%(levelname)8s] %(message)s")

from . import conffile
from .client import HttpServer
from .conf import settings
from .gdm import gdm
from .player import playerManager
from .timeline import timelineManager


HTTP_PORT   = 3000
APP_NAME = 'plex-mpv-shim'

log = logging.getLogger('')

logging.getLogger('requests').setLevel(logging.CRITICAL)

def update_gdm_settings(name=None, value=None):
    gdm.clientDetails(settings.client_uuid, settings.player_name,
        settings.http_port, "Plex MPV Shim", "1.0")

def main():
    conf_file = conffile.get(APP_NAME,'conf.json')
    if os.path.isfile('settings.dat'):
        settings.migrate_config('settings.dat', conf_file)
    settings.load(conf_file)
    settings.add_listener(update_gdm_settings)
    
    update_gdm_settings()
    gdm.start_all()

    log.info("Started GDM service")

    myqueue = queue.Queue()

    while not gdm.discovery_complete:
        time.sleep(1)

    gdm.discover()

    server = HttpServer(myqueue, int(settings.http_port))
    server.start()

    timelineManager.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("")
        log.info("Stopping services...")
    finally:
        playerManager.stop()
        server.stop()
        timelineManager.stop()
        gdm.stop_all()

if __name__ == "__main__":
    main()

