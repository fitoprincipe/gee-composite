from ipywidgets import *


class Clouds(VBox):
    def __init__(self, **kwargs):
        super(Clouds, self).__init__(**kwargs)
        self.cloud_cover = Select(
            description='Cloud Cover less than',
            options=list(range(100, -1, -1)),
            value=100
        )
        self.mask_clouds = Checkbox(description='Mask out clouds', value=True)

        self.children = [self.cloud_cover, self.mask_clouds]