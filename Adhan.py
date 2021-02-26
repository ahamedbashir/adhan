from datetime import date, datetime, timedelta
from os import name, waitpid
from threading import Event, Thread, Timer, main_thread
import json
import time

from audioplayer import AudioPlayer


class Adhan(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
        self.PrayerName = ['Fajr',	'Dhuhr',	'Asr',	'Maghrib',	'Isha']
        self.currentPrayerName = ""
        self.currentPrayerTime = ""
        self.nextPrayerName = ""
        self.nextPrayerTime = ""

    def start(self):
        stopFlag = Event()
        thread = self(stopFlag)
        thread.run()
        # stop the timer
        stopFlag.set()

    def run(self):
        waitTime = 0
        firstRun = True
        now = datetime.now()
        nextDay = now + timedelta(days=1)
        nextDay = nextDay.replace(hour=1, minute=0, second=0, microsecond=0)
        waitTime2 = (nextDay - now).total_seconds()
        finalWaitTime = (timedelta(days=1)).total_seconds()

        while not self.stopped.wait(waitTime):
            today = datetime.now()
            print("Start Time", today)
            waitTime = waitTime2 if firstRun else finalWaitTime
            waitTime = 30
            firstRun = False
            self.scheduleAdhan()
            print("Next day will start")

    def playAdhan(self, prayerTime, prayerName):
        adhan = AudioPlayer("./Adhans/AdhanFajr.mp3") if prayerName == "Fajr" \
            else AudioPlayer("./Adhans/Adhan.mp3")
        print(prayerName, prayerTime)
        adhan.play(block=True)
        time.sleep(10)
        adhan.stop()
        adhan.close()

    def scheduleAdhan(self):
        date = datetime.now()
        with open(f"./prayerTimes/{date.strftime('%B') }.json") as f:
            monthlyPrayerTimes = json.load(f)
            self.playDailyPrayerAlert(monthlyPrayerTimes[date.day-1])
            # print(monthlyPrayerTimes[str(date.day)])

    def playDailyPrayerAlert(self, PrayerTimes):
        i = 0
        while i < 5 and (waitTime := self.calcWaitTime(PrayerTimes[self.PrayerName[i]], self.PrayerName[i])) and not self.stopped.wait(waitTime):
            if waitTime >= 0:
                print("Time for ", self.PrayerName[i])
                self.playAdhan(
                    PrayerTimes[self.PrayerName[i]], self.PrayerName[i])
            i += 1

    def calcWaitTime(self, nextTimeStr, nextPrayerName):
        nextPrayerTime = datetime.strptime(
            nextTimeStr, '%H:%M:%S').time()
        timeNow = datetime.today()
        delta_t = datetime.combine(
            timeNow.today(), nextPrayerTime) - timeNow
        waitTime = delta_t.total_seconds()
        if waitTime >= 0:
            print("Time Now : ", timeNow.time())
            print("Next Prayer Time : ", nextPrayerName, nextPrayerTime)
        return waitTime


if __name__ == "__main__":
    Adhan.start(Adhan)
