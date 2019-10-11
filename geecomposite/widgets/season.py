from ipywidgets import *
from .calendar import Calendar
from geebap import season


class Season(HBox):
    def __init__(self, **kwargs):
        super(Season, self).__init__(**kwargs)
        start = kwargs.get('start', '01-01')
        startm = start[:2]
        startd = start[3:5]
        end = kwargs.get('end', '12-31')
        endm = end[:2]
        endd = end[3:5]

        self.startC = Calendar(day=startd, month=startm)
        self.endC = Calendar(day=endd, month=endm)

        self.startA = Accordion([self.startC], layout=Layout(width='400px'))
        self.endA = Accordion([self.endC], layout=Layout(width='400px'))
        self.startA.set_title(0, 'start')
        self.endA.set_title(0, 'end')

        self.children = [self.startA, self.endA]

    def getStart(self):
        return self.startC.getValue()

    def getEnd(self):
        return self.endC.getValue()

    def getSeason(self):
        return season.Season(self.getStart(), self.getEnd())