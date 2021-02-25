# Adhan


## A python application that shedules Adhan <br/> everyday at 01:00:00 AM.

This application runs until manually stopped
Can be added to the startup application so that this application <br/> run even after system reboot/restart
You can use this application for personal purpose using your own local prayer time schedule




# Prayer Times

## Required Data and Format
- Filename must be named Month.json
- Array Index must follow date
- "Fajr": "HH:MM:SS"
- "Dhuhr": "HH:MM:SS"
- "Asr": "HH:MM:SS"
- "Maghrib": "HH:MM:SS"
- "Isha": "HH:MM:SS",


      FileName = MonthName.json
      [
        {
            "Date": "Month Date 1",
            "Day": "Day",
            "Sunrise": "HH:MM:SS",
            "Dhuhr": "HH:MM:SS",
            "Asr": "HH:MM:SS",
            "Maghrib": "HH:MM:SS",
            "Isha": "HH:MM:SS",
            "Arabic Date": "Arabic Month Date"
        },
          {
            "Date": "Month Date 2",
            "Day": "Day",
            "Fajr": "HH:MM:SS",
            "Sunrise": "HH:MM:SS",
            "Dhuhr": "HH:MM:SS",
            "Asr": "HH:MM:SS",
            "Maghrib": "HH:MM:SS",
            "Isha": "HH:MM:SS",
            "Arabic Date": "Arabic Month Date"
        }

      ]

