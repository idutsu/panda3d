from direct.showbase.ShowBase import ShowBase
class App(ShowBase):
    def __init__(self):
        super().__init__()
        m = self.loader.loadModel("panda")  # まずは付属モデルでOK
        m.reparentTo(self.render)
        m.setScale(0.4); m.setPos(0, 10, 0)
App().run()
