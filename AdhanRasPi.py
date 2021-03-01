from datetime import date, datetime, timedelta
from os import name, waitpid
from threading import Event, Thread, Timer
import json
import time
import sys, os


class Adhan(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stopped = Event()
        self.PrayerName = ['Fajr',	'Dhuhr',	'Asr',	'Maghrib',	'Isha']
        self.currentPrayerName = ""
        self.currentPrayerTime = ""
        self.nextPrayerName = ""
        self.nextPrayerTime = ""

    def start(self):
        stopFlag = self.stopped
        thread = self
        thread.run()
        # stop the timer
        stopFlag.set()

    def run(self):
        print("Adhan Application started on", datetime.strftime(datetime.now(), '%B %d %Y at %H:%M:%S'))
        waitTime = 0
        while not self.stopped.wait(waitTime):
            print("Today is", datetime.strftime(datetime.now(), '%B %d %Y'))
            self.scheduleAdhan()
            now = datetime.now()
            nextDay = now + timedelta(days=1)
            nextDay = nextDay.replace(hour=1, minute=0, second=0, microsecond=0)
            waitTime = (nextDay - now).total_seconds()
            print("Next day will start in", timedelta(waitTime))

    def playAdhan(self, prayerTime, prayerName):
        path = os.path.dirname(os.path.realpath(__file__))
        if prayerName == "Fajr":
            self.soundPlayer(path+"/Adhans/AdhanFajr.mp3")
        else:
            self.soundPlayer(path+"/Adhans/Adhan.mp3")
        time.sleep(10)

    def soundPlayer(self, fileName):
        os.system('omxplayer -o alsa ' + fileName)

    def scheduleAdhan(self):
        date = datetime.now()
        path = os.path.dirname(os.path.realpath(__file__))
        fileName = path + "/prayerTimes/" + date.strftime('%B') + ".json"
        # print(fileName)
        with open(fileName) as f:
            monthlyPrayerTimes = json.load(f)
            self.playDailyPrayerAlert(monthlyPrayerTimes[date.day-1])
            # print(monthlyPrayerTimes[str(date.day)])

    def playDailyPrayerAlert(self, PrayerTimes):
        print("Starting Todays Adhan")
        i = 0
        waitTime = self.calcWaitTime(PrayerTimes[self.PrayerName[i]], self.PrayerName[i])
        while not self.stopped.wait(waitTime):
            if waitTime >= 0:
                print("Time for ", self.PrayerName[i])
                # self.playAdhan(
                #     PrayerTimes[self.PrayerName[i]], self.PrayerName[i])
            i += 1
            if(i >= 5):
                break
            waitTime = self.calcWaitTime(PrayerTimes[self.PrayerName[i]], self.PrayerName[i])

    def calcWaitTime(self, nextTimeStr, nextPrayerName):
        nextPrayerTime = datetime.strptime(
            nextTimeStr, '%H:%M:%S').time()
        timeNow = datetime.today()
        delta_t = datetime.combine(
            timeNow.today(), nextPrayerTime) - timeNow
        waitTime = delta_t.total_seconds()
        if waitTime >= 0:
            print("Time Now : ", datetime.strftime(timeNow, '%H:%M:%S'))
            print("Next Prayer Time : ", nextPrayerName, nextPrayerTime)
        return waitTime


if __name__ == "__main__":
    adhan  = Adhan()
    adhan.start()
