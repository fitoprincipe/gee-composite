from ipywidgets import *


class Calendar(HBox):
    MD = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    def __init__(self, **kwargs):
        super(Calendar, self).__init__(**kwargs)
        defm = int(kwargs.get('month', 1))
        defm = defm if defm <= 12 else 1
        defd = int(kwargs.get('day', 1))
        defd = defd if defd <= self.MD[defm] else 1
        self.month = Select(description='Month', options=list(range(1, 13)), value=defm,
                            layout=Layout(width='150px'))
        days = list(range(1, self.MD[self.month.value]+1))
        self.day = Select(description='Day', options=days, value=int(defd),
                          layout=Layout(width='150px'))

        self.month.observe(self.update)
        self.children = [self.month, self.day]

    def update(self, data):
        if data['name'] == 'value':
            m = data['new']
            days = list(range(1, self.MD[m]+1))
            self.day.options = days

    def getValue(self):
        month = self.month.value
        month = str(month) if month >= 10 else '0{}'.format(month)
        day = self.day.value
        day = str(day) if day>= 10 else '0{}'.format(day)
        return '{}-{}'.format(month, day)