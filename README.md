## Gravity Plotting using Google Maps API
### Dependencies: 
* Determined using pipreqs https://github.com/bndr/pipreqs 
* Requirements stored into requirements.txt 
* Install packages using "pip install -r requirements.txt"
* May require some admin privileges for installation (Command Prompt in admin mode)
<br/>
<br/>

### Usage:
* Navigate to the "Web" folder and run app.py.

* You should see this something like this
```
C:\Users\kwekz\PycharmProjects\ATAP\GravityPlot\Web>python app.py
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 684-004-080
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

* Open the link <http://127.0.0.1:5000/> in a browser, preferably Chrome. 
* The script will then log 200 data points and store them in both **CSV**
and **JSON** formats.
* These 2 files will be created in a folder name current_logs. This folder is marked in 
gitignore and will not be tracked.
```
Not yet in float or fixed mode. Proceed to log data? Y/N
y
Press Ctrl-C to stop logging
JSON file stored in C:\Users\kwekz\PycharmProjects\ATAP\Serial\GPS\current_logs\log-20210607-173930.json
CSV file stored in C:\Users\kwekz\PycharmProjects\ATAP\Serial\GPS\current_logs\log-20210607-173930.csv
```

* Filename will be in this format: `log-YYYYMMDD-HHMMSS.json/csv`


<br/>
<br/>

### Examples:
**In SPP Mode**


```
C:\Users\kwekz\PycharmProjects\ATAP\Serial\GPS>python gpslogging.py
start
116519.2000, SPP
116519.3000, SPP
116519.4000, SPP
116519.5000, SPP
116519.6000, SPP
116519.7000, SPP
116519.8000, SPP
Not yet in float or fixed mode. Proceed to log data? Y/N
y
Press Ctrl-C to stop logging
JSON file stored in C:\Users\kwekz\PycharmProjects\ATAP\Serial\GPS\current_logs\log-20210607-173930.json
CSV file stored in C:\Users\kwekz\PycharmProjects\ATAP\Serial\GPS\current_logs\log-20210607-173930.csv
```
<br/>
<br/>

### Past Logs:
Contains past log data.
* `csv` -> csv logs
* `json` -> json logs
* `sbpmessages` -> Deciphered SBP messages in individual packets
* `swiftconsole` -> Output from Swift Console GUI




### Additional Stuff (For 14/7/2021 trial):

The GPS script is gpslogging.py, located in Serial/GPS
After running the script, a folder named "current_logs" will be created in the same directory. It will contain the CSV and JSON logs, timestamped according to when
you started running the script.


The post processing of the data, I am not too familiar with. I mostly tried out the methods over here https://support.swiftnav.com/support/solutions/articles/44001907895-sbp-to-rinex-converter-and-data-post-processing
sbp2rinex the json file produced, then using the RTKPOST tool from RTKLIB, process the resultant obs and nav files. 



For running of the script, it will be on some other laptop. Hence there are some things which might need to be changed.
I have been able to run the script on command prompt with no issue, just need to configure some stuff:

* 1) May need to install the dependencies in "requirements.txt". This is done using "pip install -r requirements.txt"
<br/>
<br/>

* 2) May need to change the COM port. Default one is now COM5. You can check which COM port is being used through *Windows Device Manager -> Ports*  
Either supply a new port argument when you run it or change it directly in the script.

```
def main():
    parser = argparse.ArgumentParser(
        description="Swift Navigation SBP Example.")
    parser.add_argument(
        "-p",
        "--port",
        default=['COM5'],     (HERE)
        nargs=1,
        help="specify the serial port to use.")
    args = parser.parse_args()
```
<br/>
<br/>

* 3) The script is set to log for 30 seconds or after 200 readings, which might not be enough. You can just change the values in the script accordingly

```
def data_logging(filename, source):
    json_file = open(filename + ".json", "a")
    csv_file = open(filename + ".csv", "a", newline='')
    start_time = time.perf_counter()

    try:
        logger = JSONBinLogger(json_file)
        parser = CSVLogger(csv_file)
        print("Press Ctrl-C to stop logging")

        for msg, metadata in source:
            logger(msg, **metadata)  # JSON Logging
            parser.parses_switch(msg)

            if parser.count >= 200:  # Stop at 200 entries  (HERE)
                break

            if time.perf_counter() - start_time > 30:  # Stop at 30 seconds  (HERE)
                print("Timeout - Less than 200 valid entries")
                break
```
<br/>
<br/>

* 4) The script is set to log data only when in FLOAT or FIXED mode. This check is made here:
```
           if msg.flags == solutions["FIXED"] or msg.flags == solutions["FLOAT"]:
```

You can remove the float portion if you want the GPS sensor to only start logging at FIXED mode.

<br/>
<br/>

* 5) You can interrupt the logging, or even the checking for FIXED mode, using Ctrl-C. The script will just skip ahead.
<br/>
<br/>

From my trial on the roof, it takes a while for RTK Fixed mode to be achieved when both Rover and Base Station are turned on.
Might even need to restart the devices (unplug power bank) if they are stuck in SPP mode for too long.

They will also take some time to respond to "loss of RTK fixed mode" (If you suddenly unplug the base station, the rover will still 
indicate "RTK FIXED" for a while.)

When starting a connection, you may get some unregistered bytes at the start. It should change after a while to something like
868.9000, INVALID
869.0000, INVALID
869.1000, INVALID
869.2000, INVALID
869.3000, INVALID
but if it doesnt, then just restart the GPS sensor and reconnect. 



