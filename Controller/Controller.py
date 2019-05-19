import time
import threading
from Controller import UserDialogLogic


class Controller:
    def __init__(self, digest_interval, activities):
        self.stop = False
        self.activities = []
        self.digest_interval = digest_interval
        self.last_digest = time.time()
        self.digest_timer = threading.Timer(self.digest_interval, self.interval_function)
        self.user_interaction_parser = UserDialogLogic.UserDialogLogic()

    def stop(self):
        self.stop = True

    def interval_function(self):
        start_time = time.time()
        for activity in self.activities:
            activity()
        tick_processing_time = start_time - time.time()
