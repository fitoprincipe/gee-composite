from ipywidgets import *
from traitlets import *


class Years(HBox):
    all_years = List()
    year_back = Int()
    year_forth = Int()
    year = Int()

    def __init__(self, **kwargs):
        super(Years, self).__init__(**kwargs)
        self.back = Text(description='Back', value='0')
        self.forth = Text(description='Forth', value='0')
        self.years = Select(description='Year', options=[2019])
        self.year = self.years.value

        self.children = [self.years, VBox([self.back, self.forth])]

        link((self.years, 'value'), (self, 'year'))
        self.back.observe(self.obback, names=['value'])
        self.forth.observe(self.obforth, names=['value'])
        self.back.value = '0'
        self.forth.value = '0'

    def obforth(self, change):
        new = change['new']
        try:
            value = int(new)
            self.year_forth = self.year + value
            self.all_years = list(range(self.year_back, self.year_forth+1))
        except ValueError:
            pass

    def obback(self, change):
        new = change['new']
        try:
            value = int(new)
            self.year_back = self.year - int(value)
            self.all_years = list(range(self.year_back, self.year_forth+1))
        except ValueError:
            pass

    @observe('year')
    def obyear(self, change):
        value = change['new']
        self.year_back = value - int(self.back.value)
        self.year_forth = value + int(self.forth.value)
        self.all_years = list(range(self.year_back, self.year_forth+1))
