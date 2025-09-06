# main.py
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Vec3, CardMaker, loadPrcFileData

# （必要なら）FPS表示OFFやウィンドウ設定
loadPrcFileData("", "show-frame-rate-meter false")

class MyApp(ShowBase):
    def __init__(self):
        super().__init__()

        # ====== カメラ ======
        self.disableMouse()  # マウスの自動カメラ制御を切る
        self.camera.setPos(0, -35, 18)
        self.camera.lookAt(0, 0, 0)

        # ====== 入力管理 ======
        self.keys = {"w": False, "s": False, "a": False, "d": False, "q": False, "e": False}
        for k in self.keys.keys():
            self.accept(k, self._set_key, [k, True])
            self.accept(k + "-up", self._set_key, [k, False])
        self.accept("escape", self.userExit)

        # ====== 地面（カードで簡易作成）======
        cm = CardMaker("ground")
        cm.setFrame(-50, 50, -50, 50)  # X: -50~50, Y: -50~50 の一枚板
        ground = self.render.attachNewNode(cm.generate())
        ground.setP(-90)                # 寝かせる
        ground.setZ(0)                  # 高さ0
        ground.setColor(0.2, 0.6, 0.2)  # 草っぽい色

        # ====== プレイヤー（パンダ）======
        self.player = self.loader.loadModel("panda")  # 付属モデル
        self.player.reparentTo(self.render)
        self.player.setScale(0.35)
        self.player.setPos(0, 0, 0)

        # ====== コイン配置（とりあえず小さな黄色パンダをコイン扱い）======
        # 本来は .glb のコインモデル等に差し替えを推奨
        coin_positions = [(-10, 10, 0), (15, -5, 0), (20, 20, 0), (-18, -15, 0), (0, 25, 0)]
        self.coins = []
        for i, pos in enumerate(coin_positions):
            c = self.loader.loadModel("panda")
            c.reparentTo(self.render)
            c.setScale(0.15)
            c.setPos(*pos)
            c.setColorScale(1.0, 1.0, 0.3, 1)  # 黄色っぽく
            c.setH(i * 15)  # ちょっと向きの差
            self.coins.append(c)

        self.collected = 0
        self.total_coins = len(self.coins)

        # ====== HUD ======
        self.hud = OnscreenText(text=self._hud_text(), pos=(-1.29, 0.95), mayChange=True, scale=0.05, fg=(1,1,1,1), align=0)
        self.notice = OnscreenText(text="", pos=(0, 0.85), mayChange=True, scale=0.07, fg=(1,1,0.3,1))

        # ====== 更新タスク ======
        self.speed = 12.0       # 移動速度
        self.turn_speed = 90.0  # 回転速度(度/秒)
        self.taskMgr.add(self.update, "update")

    def _set_key(self, key, val):
        self.keys[key] = val

    def _hud_text(self):
        return f"[WASDで移動 / Q,Eで回転]  Coins: {self.collected}/{self.total_coins}   ESCで終了"

    def _move_player(self, dt):
        # 回転
        if self.keys["q"]:
            self.player.setH(self.player, self.turn_speed * dt)
        if self.keys["e"]:
            self.player.setH(self.player, -self.turn_speed * dt)

        # 前後左右（ローカル座標で移動）
        move = Vec3(0, 0, 0)
        if self.keys["w"]:
            move += Vec3(0, 1, 0)
        if self.keys["s"]:
            move += Vec3(0, -1, 0)
        if self.keys["a"]:
            move += Vec3(-1, 0, 0)
        if self.keys["d"]:
            move += Vec3(1, 0, 0)

        if move.length() > 0:
            move.normalize()
            self.player.setPos(self.player, move * self.speed * dt)

        # カメラを追従（ゆるく）
        target = self.player.getPos() + Vec3(0, -30, 16)
        self.camera.setPos(self.camera.getPos() * 0.9 + target * 0.1)
        self.camera.lookAt(self.player)

    def _check_coin_collect(self):
        # 距離しきい値で簡易判定（本格的にはCollisionSystem推奨）
        threshold = 2.0
        p = self.player.getPos()
        remain = []
        got = 0
        for c in self.coins:
            if (c.getPos() - p).length() < threshold:
                c.removeNode()
                got += 1
            else:
                remain.append(c)
        if got:
            self.collected += got
            self.hud.setText(self._hud_text())
        self.coins = remain

        if self.collected >= self.total_coins:
            self.notice.setText("🎉 ALL COINS! YOU WIN! 🎉")

    def update(self, task):
        dt = globalClock.getDt()
        self._move_player(dt)
        self._check_coin_collect()
        return task.cont


app = MyApp()
app.run()

