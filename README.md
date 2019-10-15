# Google Earth Engine (GEE) compositing
Make a [*Best Available Pixel (BAP)*](https://github.com/fitoprincipe/geebap) composite using GEE's Python API in a User Interface within a Jupyter Notebook.

### Requirements

1. [Google Earth Engine](https://earthengine.google.com/) account
2. [Python 3+](https://www.python.org/downloads/) (3.6+ preferred)
3. Jupyter:
    - In Windows you can use [Anaconda](https://www.anaconda.com/)
    - In Linux it will be installed with the python packages needed

### Install

- Windows
    - Install Anaconda
    - Open Anaconda Prompt (search for it in Programs Menu)
    - (OPTIONAL) Create a new environment: [link](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
    - Use `pip` to install this package:
        > pip install geecomposite
    - If this is the first time you use GEE's Python API you have to authenticate:
        > earthengine authenticate
    - (JUST IN CASE) Enable `ipyleaflet`:
        > jupyter nbextension enable --py --sys-prefix ipyleaflet
    - open a notebook
        > jupyter notebook
    - open [this]() file

- Linux    
    - Open a terminal
    - (OPTIONAL) Create a new environment: [link](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
    - Use `pip` to install this package:
        > pip install geecomposite
    - If this is the first time you use GEE's Python API you have to authenticate:
        > earthengine authenticate
    - (JUST IN CASE) Enable `ipyleaflet`:
        > jupyter nbextension enable --py --sys-prefix ipyleaflet
    - open a notebook
        > jupyter notebook
    - open [this]() file
    
### Usage

Running all cells in `bap.ipynb` will get you to the User Interface:

```python
import ee
ee.Initialize()
import ipygee as ui
import geecomposite

bapwidget = geecomposite.Bap()
bapwidget
```

- File Manager
    - Once you have set the parameters for creating a composite, you can save
    them using the `Save` Tab. And if you have already saved one, you can open
    it using the `Open` Tab. Configuration files are stored in `json` format
- Site
    - Here you can choose an EE Asset using its path. Once you write the `assetPath`
    click on `Fetch Properties`, then choose the property that segregates your
    sites, click on `Fetch Options` and finally select the site.
- Collections
    - choose one from: Landsat 8, 7, 5, 4 and/or Sentinel 2
- Season
    - Choose the day and month for the start and end of the season
- Year
    - if the season goes over the end of the year, then:
        - startday-startmonth-year to endday-endmonth-year+1
        - example: 15-11-2010 to 15-02-2011
    - if not:
        - startday-startmonth-year to endday-endmonth-year
        - example: 15-06-2010 to 15-11-2010
    - Back & Forth: if these parameters are greater than zero then it will take
    images from `back` years back and `forth` years forth
- Clouds
    - Choose a cloud cover percentage to filter the collection
    - Choose whether to mask the clouds out or not
- Scores
    - Doy
        - Maximum score for a given "day of year"
    - Satellite
        - Maximum score for the best satellite in the given period
    - Cloud distance
        - Minimum score for the pixels next to clouds (mask in general)
    - Mask cover
        - Maximum score to the image with less masked pixels
    - Index
        - Maximum score for pixels with a given vegetation index (momentarily set to 0.8)
    - Outliers
        - Maximum score for pixels with values between mean+-std for the chosen bands
    - Medoid
        - Maximum score for pixels with the minimum euclidean distance to the median for the chosen bands
        - **NOTE**: to make a "medoid" composite use only this score
- Export
    - Section for exporting the result to an EE asset (to Drive not currently available directly)
- Map
    - Visualize in a map the composite resulted from the set parameters. You can
    use the chosen site (`Add using site`) or the map's bounds (`Add using map bounds`)
    
Alternatively you can get the `BAP` object

> bap = bapwidget.BAP()

and also get the resulting composite

> composite = bapwidget.composite()