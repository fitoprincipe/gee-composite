from ipywidgets import *
import os
import json

HOME = os.path.expanduser('~')
DEFAULT_PATH = os.path.join(HOME, 'gee-composite')


class Save(VBox):
    ext = 'json'
    def __init__(self, **kwargs):
        super(Save, self).__init__(**kwargs)
        self.bapwidget = kwargs.get('bapwidget')
        self.path = Text(description='Path', value=DEFAULT_PATH,
                         layout=Layout(width='800px'))
        self.name = Text(description='Name', value='BAP')
        self.saveB = Button(description='Save')

        self.saveB.on_click(self.save)

        self.children = [
            Label('Save BAP data into a configuration file'),
            self.path,
            HBox([self.name, Label('.{}'.format(self.ext))]),
            self.saveB
        ]

    def getValues(self):
        b = self.bapwidget
        # site
        sitePath = b.site_widget.asset.value
        prop = b.site_widget.property.value
        objid = b.site_widget.id.value
        # collections
        col = b.collections_widget.value
        # season
        startm = b.season_widget.startC.month.value
        startd = b.season_widget.startC.day.value
        endm = b.season_widget.endC.month.value
        endd = b.season_widget.endC.day.value
        # Year
        year = b.years_widget.years.value
        back = b.years_widget.back.value
        forth = b.years_widget.forth.value
        # Clouds
        cover = b.clouds_widget.cloud_cover.value
        mask = b.clouds_widget.mask_clouds.value
        # Scores
        doyC = b.scores_widget.get_check(0)
        doym = b.scores_widget.doy.month.value
        doyd = b.scores_widget.doy.day.value
        satC = b.scores_widget.get_check(1)
        satR = b.scores_widget.satellite.value
        cldC = b.scores_widget.get_check(2)
        cldmax = b.scores_widget.cloud_distance.children[0].value
        cldmin = b.scores_widget.cloud_distance.children[1].value
        mskC = b.scores_widget.get_check(3)
        mskK = b.scores_widget.maskcover.value
        indicesC = b.scores_widget.get_check(4)
        indicesB = b.scores_widget.index.value
        outC = b.scores_widget.get_check(5)
        outB = b.scores_widget.outliers.value
        medC = b.scores_widget.get_check(6)
        medB = b.scores_widget.medoid.value

        params = {
            'site': {
                'path': sitePath,
                'property': prop,
                'value': objid
            },
            'collections': col,
            'season': {
                'start_day': startd,
                'start_month': startm,
                'end_day': endd,
                'end_month': endm
            },
            'year': {
                'year': year,
                'back': back,
                'forth': forth
            },
            'clouds': {
                'cover': cover,
                'mask': mask
            },
            'scores': {
                'doy': {
                    'check': doyC,
                    'month': doym,
                    'day': doyd
                },
                'satellite': {
                    'check': satC,
                    'ratio': satR
                },
                'cloud_distance': {
                    'check': cldC,
                    'max': cldmax,
                    'min': cldmin
                },
                'mask_cover':{
                    'check': mskC,
                    'kernel': mskK
                },
                'index': {
                    'check': indicesC,
                    'bands': indicesB
                },
                'outliers': {
                    'check': outC,
                    'bands': outB
                },
                'medoid': {
                    'check': medC,
                    'bands': medB
                }
            }
        }
        return params

    def save(self, v=None):
        obj = self.getValues()
        path = self.path.value
        name = self.name.value
        finalpath = os.path.join(path, name)
        final = '{}.{}'.format(finalpath, self.ext)

        with open(final, 'w+') as thefile:
            json.dump(obj, thefile, indent=2)


class Open(VBox):
    def __init__(self, **kwargs):
        super(Open, self).__init__(**kwargs)
        self.bapwidget = kwargs.get('bapwidget')
        self.path = Text(description='Path', value=DEFAULT_PATH,
                         layout=Layout(width='800px'))
        self.name = Text(description='Name', value='BAP')
        self.openB = Button(description='Open')

        self.openB.on_click(self.openFile)

        self.children = [
            Label('Open BAP data from a configuration file'),
            self.path,
            HBox([self.name, Label('.json')]),
            self.openB]

    def openFile(self, v):
        b = self.bapwidget
        path = '{}/{}.json'.format(self.path.value, self.name.value)

        if os.path.exists(path):
            with open(path, 'r') as thefile:
                data = json.load(thefile)

                # collections
                b.collections_widget.value = data['collections']
                # season
                b.season_widget.startC.month.value = data['season']['start_month']
                b.season_widget.startC.day.value = data['season']['start_day']
                b.season_widget.endC.month.value = data['season']['end_month']
                b.season_widget.endC.day.value = data['season']['end_day']
                # Year
                b.years_widget.years.value = data['year']['year']
                b.years_widget.back.value = data['year']['back']
                b.years_widget.forth.value = data['year']['forth']
                # Clouds
                b.clouds_widget.cloud_cover.value = data['clouds']['cover']
                b.clouds_widget.mask_clouds.value = data['clouds']['mask']
                # Scores
                b.scores_widget.set_check(0, data['scores']['doy']['check'])
                b.scores_widget.doy.month.value = data['scores']['doy']['month']
                b.scores_widget.doy.day.value = data['scores']['doy']['day']
                b.scores_widget.set_check(1, data['scores']['satellite']['check'])
                b.scores_widget.satellite.value = data['scores']['satellite']['ratio']
                b.scores_widget.set_check(2, data['scores']['cloud_distance']['check'])
                b.scores_widget.cloud_distance.children[0].value = data['scores']['cloud_distance']['max']
                b.scores_widget.cloud_distance.children[1].value = data['scores']['cloud_distance']['min']
                b.scores_widget.set_check(3, data['scores']['mask_cover']['check'])
                b.scores_widget.maskcover.value = data['scores']['mask_cover']['kernel']
                b.scores_widget.set_check(4, data['scores']['index']['check'])
                b.scores_widget.index.value = data['scores']['index']['bands']
                b.scores_widget.set_check(5, data['scores']['outliers']['check'])
                b.scores_widget.outliers.value = data['scores']['outliers']['bands']
                b.scores_widget.set_check(6, data['scores']['medoid']['check'])
                b.scores_widget.medoid.value = data['scores']['medoid']['bands']

                # site
                b.site_widget.asset.value = data['site']['path']
                try:
                    b.site_widget.fetchProperties()
                except Exception as e:
                    raise e
                else:
                    b.site_widget.property.value = data['site']['property']
                try:
                    b.site_widget.fetchOptions()
                except Exception as e:
                    raise e
                else:
                    b.site_widget.id.value = data['site']['value']
                self.openB.button_style = 'success'
        else:
            self.openB.button_style = 'danger'
