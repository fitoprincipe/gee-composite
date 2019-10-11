from ipywidgets import *


class Years(HBox):
    def __init__(self, **kwargs):
        super(Years, self).__init__(**kwargs)
        self.years = Select(description='Year')
        self.back = Text(description='Back', value='0')
        self.forth = Text(description='Forth', value='0')

        self.children = [self.years, VBox([self.back, self.forth])]