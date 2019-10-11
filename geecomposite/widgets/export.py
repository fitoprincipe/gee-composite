from geetools import batch
from ipywidgets import *


class toAsset(VBox):
    def __init__(self, **kwargs):
        super(toAsset, self).__init__(**kwargs)
        layout = Layout(width='500px')
        self.bapwidget = kwargs.get('bapwidget')
        self.root = kwargs.get('root', '')
        self.scale = Text(description='scale', value='10')
        self.destination = Select(description='Destination',
                                  options=['ImageCollection', 'Folder'],
                                  value='ImageCollection',
                                  layout=layout)
        self.folder = Text(description='Path to the ImageCollection',
                           value=self.root,
                           layout=layout,
                           style = {'description_width': 'initial'})
        self.nameSub = Text(description='Name of/for the ImageCollection',
                            layout=layout,
                            style = {'description_width': 'initial'})
        self.name = Text(description='Name for the Image',
                         layout=layout,
                         style = {'description_width': 'initial'})
        self.exportB = Button(description='Export')
        self.bands = SelectMultiple(description='Bands', layout=layout)
        self.bands.observe(self.observeBands)

        self.exportB.on_click(self.export)
        self.destination.observe(self.observeDestination)

        self.children = [self.destination, self.folder, self.nameSub,
                         self.name, self.bands, self.exportB]

    def observeDestination(self, v):
        if v['name'] == 'value':
            value = v['new']
            self.folder.description = "Path to the {}".format(value)
            self.nameSub.description = "Name of/for the {}".format(value)

    def observeBands(self, v):
        extra = ['col_id', 'date', 'score']
        if v['name'] == 'options':
            bands = list(v['new'])
            condition = all([b in bands for b in extra])
            if not condition:
                self.bands.options = bands+extra

    def getAssetPath(self):
        return "{}/{}".format(self.folder.value, self.nameSub.value)

    def getAssetId(self):
        return "{}/{}".format(self.getAssetPath(), self.name.value)

    def export(self, v=None):
        bands = self.bands.value
        composite = self.bapwidget.composite().select(bands)
        batch.Export.image.toAsset(composite, self.getAssetPath(),
                                   self.name.value, self.destination.value,
                                   float(self.scale.value),
                                   self.bapwidget.site_widget.getRegion())
