import ee
from geetools import collection
from ipywidgets import *
from traitlets import *

IDS = {
    'Landsat 8 SR': 'LANDSAT/LC08/C01/T1_SR',
    'Landsat 7 SR': 'LANDSAT/LE07/C01/T1_SR',
    'Landsat 5 SR': 'LANDSAT/LT05/C01/T1_SR',
    'Landsat 4 SR': 'LANDSAT/LT04/C01/T1_SR',
    'Sentinel 2 TOA': 'COPERNICUS/S2',
    'Sentinel 2 SR': 'COPERNICUS/S2_SR'
}


class Collections(SelectMultiple):
    years = List()
    bands = List()
    def __init__(self, **kwargs):
        super(Collections, self).__init__(**kwargs)
        self.options = ['Landsat 8 SR','Landsat 7 SR','Landsat 5 SR',
                        'Landsat 4 SR','Sentinel 2 TOA','Sentinel 2 SR']
        self.label = ('Sentinel 2 TOA',)
        self.description = 'Collections'

    @observe('value')
    def obval(self, change):
        new = change['new']

        group = self.group()
        # Update years
        start = group.start_date()
        end = group.end_date()
        start_year = int(start[:4])
        end_year = int(end[:4])
        self.years = list(range(start_year, end_year+1))

        # Update bands
        bands = group.commonBands(match='name')
        self.bands = bands + ['ndvi', 'nbr']

    def group(self):
        cols = [collection.fromId(IDS[opt]) for opt in self.value]
        return collection.CollectionGroup(*cols)
