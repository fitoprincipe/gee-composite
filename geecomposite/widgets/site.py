from geetools import tools
from ipywidgets import *
import ee


class Site(VBox):
    def __init__(self, **kwargs):
        super(Site, self).__init__(**kwargs)
        self.root = kwargs.get('root', ee.data.getAssetRoots()[0]['id'])
        self.asset = Text(desciption='ID', value=self.root)
        self.fetchPropertiesB = Button(description='Fetch Properties')
        self.property = Select(description='property')
        self.fetchOptionsB = Button(description='Fetch Options')
        self.id = Select()

        self.children = [HBox([self.asset, self.fetchPropertiesB]),
                         HBox([self.property, self.fetchOptionsB]),
                         self.id]

        self.fetchPropertiesB.on_click(self.fetchProperties)
        self.fetchOptionsB.on_click(self.fetchOptions)

    def getAsset(self):
        assetId = self.asset.value
        return ee.FeatureCollection(assetId)

    def fetchProperties(self, v=None):
        fc = self.getAsset()
        props = ee.Feature(fc.first()).propertyNames()
        try:
            self.property.options = props.getInfo()
        except ee.EEException:
            pass
        except Exception as e:
            raise(e)

    def fetchOptions(self, v=None):
        value = self.property.value
        if value:
            options = tools.featurecollection.listOptions(self.getAsset(),
                                                          value).getInfo()
            self.id.options = options
            self.id.description = value

    def getSite(self):
        asset = self.getAsset()
        filtered = asset.filterMetadata(self.property.value, 'equals',
                                        self.id.value).first()
        return ee.Feature(filtered)

    def getRegion(self):
        return tools.geometry.getRegion(self.getSite())
