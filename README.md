# Sensor Dashboard #

A unified location to log and graph all your IoT sensor data.
Powered by Python and MongoDB, this is a super flexible data logging system which handles whatever data you throw at it as long as it's JSON.

You can create a new 'collection' just by posting data to `/api/log/<collection>`, no need to create a new one for every new device you add, it does it all for you.

After a collection is created by POSTing your first data item to it, you can choose from any of the pre-defined graphing templates to display your data.
Or just create your own new custom one.

For every bit of data logged, it's recorded with a timestamp.
The latest logged data element can always be found at `/api/log/<collection>/latest`

## Installation ##

Install the dependencies (you may need to add the MongoDB repositories, see their site for specific instructions)
```
$ sudo apt update
$ sudo apt install git python3 python3-pip python3-venv mongodb-org
```

Clone this repository

```
$ git clone git@github.com:Jamie-/sensor-dashboard.git
```

Create the python virtual environment
```
$ cd sensor-dashboard
$ make setup
```

Copy and edit the included sample config to your requirements
```
$ cp config.sample.json config.json
```

Start up the application
```
$ ./start.sh
```

Optionally, you can add the app as a systemd service, to do this, make sure `sensor-dashboard` is moved and renamed to `/opt/logger` or edit the `logger.service` file as appropriate
```
$ sudo cp /opt/logger/logger.service /etc/systemd/system/
```
