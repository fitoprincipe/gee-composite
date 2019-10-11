from ipywidgets import *
from .season import Season
from .collections import Collections
from .site import Site
from .years import Years
from .clouds import Clouds
from .scores import Scores
from .manager import Save, Open
from .export import toAsset
from .map import Map
import ee
import geebap


class Bap(Tab):
    def __init__(self, **kwargs):
        super(Bap, self).__init__(**kwargs)
        self.root = kwargs.get('root', ee.data.getAssetRoots()[0]['id'])
        self.site_widget = Site(root=self.root)
        self.collections_widget = Collections()
        self.season_widget = Season()
        self.years_widget = Years()
        self.clouds_widget = Clouds()
        self.scores_widget = Scores()
        self.map_widget = Map(bapwidget=self)

        # Export
        self.asset_widget = toAsset(bapwidget=self, root=self.root)
        self.export_widget = Tab([self.asset_widget])
        self.export_widget.set_title(0, 'to Asset')

        # File Manager
        self.save_widget = Save(bapwidget=self)
        self.open_widget = Open(bapwidget=self)
        self.manager_widget = Tab([self.open_widget, self.save_widget])
        self.manager_widget.set_title(0, 'Open')
        self.manager_widget.set_title(1, 'Save')

        # Link Properties
        link((self.collections_widget, 'years'), (self.years_widget.years, 'options'))
        link((self.collections_widget, 'bands'), (self.scores_widget.outliers, 'options'))
        link((self.collections_widget, 'bands'), (self.scores_widget.medoid, 'options'))
        link((self.collections_widget, 'bands'), (self.asset_widget.bands, 'options'))

        self.children = [self.manager_widget, self.site_widget, self.collections_widget,
                         self.season_widget, self.years_widget, self.clouds_widget,
                         self.scores_widget, self.export_widget, self.map_widget]

        # Set titles for the Tab
        titles = [
            'File Manager',
            'Site',
            'Collections',
            'Season',
            'Year',
            'Clouds',
            'Scores',
            'Export',
            'Map'
        ]
        for i, title in enumerate(titles):
            self.set_title(i, title)

    def getScores(self):
        scores = []
        if self.scores_widget.get_check(0):
            doy = geebap.scores.Doy(self.scores_widget.doy.getValue(),
                                    self.season_widget.getSeason())
            scores.append(doy)
        if self.scores_widget.get_check(1):
            sat = geebap.scores.Satellite(float(self.scores_widget.satellite.value))
            scores.append(sat)
        if self.scores_widget.get_check(2):
            cld = geebap.scores.CloudDist(
                int(self.scores_widget.cloud_distance.children[1].value),
                int(self.scores_widget.cloud_distance.children[0].value))
            scores.append(cld)
        if self.scores_widget.get_check(3):
            if self.scores_widget.maskcover.value:
                msk = geebap.scores.MaskPercentKernel()
            else:
                msk = geebap.scores.MaskPercent()
            scores.append(msk)
        if self.scores_widget.get_check(4):
            for index in self.scores_widget.index.value:
                scores.append(geebap.scores.Index(index))
        if self.scores_widget.get_check(5):
            outlier = geebap.scores.Outliers(self.scores_widget.outliers.value)
            scores.append(outlier)
        if self.scores_widget.get_check(6):
            medoid = geebap.scores.Medoid(self.scores_widget.medoid.value)
            scores.append(medoid)

        return scores

    def BAP(self):
        params = dict(
            range=(int(self.years_widget.back.value), int(self.years_widget.forth.value)),
            colgroup=self.collections_widget.group(),
            scores=self.getScores(),
            filters=[geebap.filters.CloudCover(int(self.clouds_widget.cloud_cover.value))]
        )

        mask = self.clouds_widget.mask_clouds.value
        if mask:
            params['masks'] = [geebap.masks.Mask()]
        else:
            params['masks'] = None

        return geebap.Bap(self.season_widget.getSeason(), **params)

    def makeComposite(self, site):
        """ Make a composite using a given site """
        bap = self.BAP()
        year = int(self.years_widget.years.value)

        return bap.build_composite_best(year, site, ['ndvi', 'nbr'])

    def composite(self):
        """ Get composite """
        return self.makeComposite(self.site_widget.getSite())

    def visualization(self, visType='NSR'):
        """ Visualization parameters """
        return self.BAP().target_collection.visualization(visType, True)

    def getSite(self):
        """ Get site """
        return self.site_widget.getSite()

    def getYear(self):
        return self.years_widget.years.value

    def getSiteName(self):
        return self.site_widget.id.value

    def getPeriod(self):
        year = self.getYear()
        start = self.season_widget.getStart()
        end = self.season_widget.getEnd()
        return '{start}-{year} to {end}-{year}'.format(start=start, end=end,
                                                       year=year)



