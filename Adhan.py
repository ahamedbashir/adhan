from datetime import date, datetime, timedelta
from os import name
from threading import Event, Thread, Timer, main_thread
import json
import time

from audioplayer import AudioPlayer


class Adhan(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
        self.currentPrayerName = ""
        self.currentPrayerTime = ""
        self.nexttPrayerName = ""
        self.nexttPrayerTime = ""

    def start(self):
        stopFlag = Event()
        thread = self(stopFlag)
        thread.run()
        # stop the timer
        stopFlag.set()

    def run(self):
        waitTime = 0
        firsRun = True
        now = datetime.now()
        nextDay = now + timedelta(days=1)
        nextDay = nextDay.replace(hour=1, minute=0, second=0, microsecond=0)
        waitTime2 = (nextDay - now).total_seconds()
        finalWaitTime = (timedelta(days=1)).total_seconds()
        while not self.stopped.wait(waitTime):
            today = datetime.now()
            print("Start Time", today)
            print("Next day", nextDay)
            waitTime = waitTime2 if firsRun else finalWaitTime
            firsRun = False
            self.scheduAdhan()

    def playAdhan(self, prayerTime, prayerName):
        adhan = AudioPlayer("./Adhans/Adhan.mp3") if prayerName > 0 \
            else AudioPlayer("./Adhans/AdhanFajr.mp3")
        adhan.play(block=True)
        time.sleep(10)
        adhan.stop()
        adhan.close()

    def scheduAdhan(self):
        date = datetime.now()
        with open(f"./prayerTimes/{date.strftime('%B') }.json") as f:
            monthlyPrayerTimes = json.load(f)
            self.playDailyPrayerAlert(monthlyPrayerTimes[date.day-1])
            # print(monthlyPrayerTimes[str(date.day)])

    def playDailyPrayerAlert(self, PrayerTimes):
        for nextPrayerName in ('Fajr',	'Dhuhr',	'Asr',	'Maghrib',	'Isha'):
            nextPrayerTime = PrayerTimes[nextPrayerName]
            nextPrayerTime = datetime.strptime(
                nextPrayerTime, '%H:%M:%S').time()

            timeNow = datetime.today()
            delta_t = datetime.combine(
                timeNow.today(), nextPrayerTime) - timeNow

            secs = delta_t.total_seconds()

            if secs > 0:
                Timer(secs, self.playAdhan, [
                    nextPrayerTime, nextPrayerName]).start()


if __name__ == "__main__":
    Adhan.start(Adhan)
