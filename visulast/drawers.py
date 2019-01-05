class Drawer:
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def draw_histogram(self):
        pass


class ArtistDrawer(Drawer):
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)