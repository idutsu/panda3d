from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight

class App(ShowBase):
    def __init__(self):
        super().__init__()
        m = self.loader.loadModel("panda")  # まずは付属モデルでOK
        m.reparentTo(self.render)
        m.setScale(0.4);
        m.setPos(0, 10, 0)

        # ライトを当てる
        dlight = DirectionalLight('dlight')
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(45, -60, 0)
        self.render.setLight(dlnp)
App().run()
