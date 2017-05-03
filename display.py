import screen
import dht
import time
import requests
import json

LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

header = {
    'X-Api-Key': '<OCTOPRINT-API-KEY>',
}

def octoprintProgress(host):
  response = requests.get(host, headers=header)
  if response is None or response.status_code != 200:
      return None
  return response.json()["progress"]

def printTime(json):
  hours = int(json["printTime"])/3600
  minutes = int(json["printTime"]%3600)/60
  return "Elapsed: {}h{}m".format(hours,minutes)

def main():
  # Main program block

  # Initialise display
  screen.lcd_init()

  while(True):    
    progress = octoprintProgress("http://<octoprint-server-ip>/api/job")
    if progress and type(progress["completion"]) is float:
      if progress["printTime"] == 0:
          line1 = "Progress: Preparing"
      else:
          line1 = "Progress: {0:.2f}%".format(progress["completion"])
      line2 = printTime(progress)
      screen.lcd_string(line1,LCD_LINE_1)
      screen.lcd_string(line2,LCD_LINE_2)
      time.sleep(10)

    temperature,pressure,humidity = dht.readBME280All()
    line1 = "Temp    Humidity"
    line2 = "{}{}C    {}%".format(round(temperature,1), chr(223), int(humidity))
    
    screen.lcd_string(line1,LCD_LINE_1)
    screen.lcd_string(line2,LCD_LINE_2)
    time.sleep(5)

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    screen.lcd_byte(0x01, LCD_CMD)
