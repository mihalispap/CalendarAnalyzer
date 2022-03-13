# CalendarAnalyzer

A calendar analyzer dashboard implemented as a user-friendly way to analyze your calendar activity.

Currently, works with a *.ics* export and was tested with the one generated
from [Google Calendar](https://takeout.google.com/).

## Installation & Execution

To successfully install and run the dashboard an environment variable file needs to be created containing the
directories:

* **CALENDARS_DIR**, where the .ics file(s) are,
* **JSON_DIR**, where the json file containing all the events should be stored,
* **IMG_DIR**, where generated images will be stored,
* [**TOPN**], signifying the top-n participants that will be shown in the respective table (this is an *optional*
  variable).

The file exported by Google Calendar should be placed in the **CALENDARS_DIR**
directory.

An example of such is a file is as follows:

```commandline
CALENDARS_DIR=data/calendars/
JSON_DIR=data/json/
IMG_DIR=assets/images/
TOPN=10
```

The easiest way to install and run the dashboard is in a Docker container using the provided files.

Executing:

```commandline
docker-compose up
```

will download all the required packages and start the dashboard.

By default, it is available at [http://127.0.0.1:8050](http://127.0.0.1:8050)

## Assumptions

During the implementation of the dashboard assumptions were made when it comes to the distinction between meetings &
personal events.

More specifically meetings are considered the events that contain >1 participant. This is an assumption made based on
the way my personal Google Calendar is organized and may not apply to others'.

## Contributions

This repo contains the work done during a weekend as a fun project. Any ideas/contributions to make it more useful are
more than welcome.