from ipywidgets import *
import ipygee as ui
from ipyleaflet import LayersControl


class Map(VBox):
    def __init__(self, **kwargs):
        super(Map, self).__init__(**kwargs)
        self.bapwidget = kwargs.get('bapwidget')
        self.map = ui.Map()
        lc = LayersControl()
        self.map.add_control(lc)
        self.name = Text(description='Name', value='BAP_composite')
        self.make_name_button = Button(description='Make name')
        self.visualization = Select(description='VisParams', options=['NSR', 'RGB'], value='NSR')
        self.add_map_button = Button(description='Add using map bounds',
                                     tooltip='Add composite to Map using Map bounds')
        self.add_site_button = Button(description='Add using Site',
                                      tooltip='Add composite to Map using the Site')

        self.add_map_button.on_click(self.addMapComposite)
        self.add_site_button.on_click(self.addSiteComposite)
        self.make_name_button.on_click(self.makeName)

        # Tabs
        self.tabs = Tab([
            VBox([
                HBox([self.name, self.make_name_button]),
                self.visualization,
                self.add_map_button,
                self.add_site_button
            ]),
            self.map.inspector_wid,
            self.map.layers_widget
        ])

        self.tabs.set_title(0, 'Composite')
        self.tabs.set_title(1, 'Inspector')
        self.tabs.set_title(2, 'Layers')

        self.children = [self.map, self.tabs]

    def makeName(self, v=None):
        vis = self.visualization.value
        year = self.bapwidget.getYear()
        period = self.bapwidget.getPeriod()
        site = self.bapwidget.getSiteName()

        name = 'BAP {site} {vis} {period}'.format(
            site=site, vis=vis, period=period
        )
        self.name.value = name

    def addComposite(self, site):
        composite = self.bapwidget.makeComposite(site)
        bap = self.bapwidget.BAP()
        vis = bap.target_collection.visualization(self.visualization.value, True)
        name = self.name.value
        self.map.addLayer(composite, vis, name)

    def addMapComposite(self, v=None):
        bounds = self.map.getBounds()
        self.addComposite(bounds)

    def addSiteComposite(self, v=None):
        site = self.bapwidget.site_widget.getSite()
        self.addComposite(site)
