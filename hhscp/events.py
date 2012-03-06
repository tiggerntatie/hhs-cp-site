__author__ = 'ericdennison'

from flask import url_for
from datetime import date, timedelta
from dateutil import parser
from dateutil.relativedelta import *
import csv


class CalendarEvent(object):

    Name = 'CalendarEvent'

    def __init__(self, datestr="January 1, 2000", name=""):
        self.date = parser.parse(datestr).date()
        self.name = name

    def __str__(self):
        d = self.date
        return "%s: %04d-%02d-%02d" % (self.name, d.year, d.month, d.day)

    def __lt__(self, other):
        return self.date < other.date

    def __gt__(self, other):
        return self.date > other.date

    def __eq__(self, other):
        return self.date == other.date

    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month

    @property
    def day(self):
        return self.date.day

class HolidayEvent(CalendarEvent):

    Name = 'HolidayEvent'

    def __init__(self, datestr, name):
        super(HolidayEvent,self).__init__(datestr, name)


class AssignmentEvent(CalendarEvent):

    Name = 'AssignmentEvent'

    def __init__(self, datestr, name, shortname, showdatestr = ''):
        super(AssignmentEvent,self).__init__(datestr, name)
        self.showdate = parser.parse(showdatestr).date()
        self.shortname = shortname
        self.url = url_for('site_assignment', short_name=shortname)


class EventList(object):

    def __init__(self, filename):
        self.events = []
        self.dict = {}
        if len(filename):
            self.data = list(csv.reader(open(filename,'r'), skipinitialspace=True))


    def __add__(self, other):
        newlist = EventList('')
        newlist.events = self.events + other.events
        newlist.events.sort()
        newlist.refreshDict()
        return newlist

    def __getitem__(self, item):
        return self.dict.get(item,[])

    def refreshDict(self):
        self.dict = {}
        for event in self.events:
            if event.date in self.dict:
                self.dict[event.date].append(event)
            else:
                self.dict[event.date] = [event]


class Holidays(EventList):

    def __init__(self, filename):
        super(Holidays,self).__init__(filename)
        self.events = [HolidayEvent(datestr, name) for datestr,name in self.data]
        self.events.sort()
        self.refreshDict()

class Assignments(EventList):

    def __init__(self, filename):
        super(Assignments,self).__init__(filename)
        self.today = date.today()
        self.events = [AssignmentEvent(datestr, name, shortname, showdate)
                       for datestr, name, shortname, showdate in self.data]

        self.events = filter(lambda x: x.showdate <= self.today, self.events)
        self.events.sort()
        self.refreshDict()
        self.refreshNameDict()

    def refreshNameDict(self):
        self.nameDict = {}
        for event in self.events:
            self.nameDict[event.shortname] = event



class Calendar(object):

    def __init__(self, holstr='./data/holidays.csv', assstr='./data/assignments.csv'):
        self.holidays = Holidays(holstr)
        self.assignments = Assignments(assstr)
        lastevent = self.assignments.events[-1]
        lastdate = lastevent.date
        firstevent = self.assignments.events[0]
        firstdate = firstevent.date
        firstcaldate = firstdate + relativedelta(weekday=SU(-1))
        lastcaldate = lastdate + relativedelta(weekday=SA)
        totaldays = (lastcaldate - firstcaldate).days
        addaday = timedelta(1)
        addaweek = addaday * 7
        ###  now build a list of weeks, each with a list of days. each day is a tuple: date and list of events
        weeks = [[firstcaldate + weekcount*addaweek + dayofweek*addaday  for dayofweek in range(1,6)]
            for weekcount in range(0, (totaldays // 7) + 1)]
        self.weeks = [[(date, self.holidays[date], self.assignments[date]) for date in week] for week in weeks]

