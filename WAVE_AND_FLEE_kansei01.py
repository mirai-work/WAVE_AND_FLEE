import pyxel
import math
import random
import os

# --- 日本語フォントの設定 ---
FONT_FILE = "umplus_j10r.bdf"

# --- Constants ---
WIDTH = 256
HEIGHT = 144
FOV = math.pi / 2.5
MOVE_SPEED = 0.08
ROT_SPEED = 0.06
MAX_WAVES = 5

# --- Material Settings ---
WALL_MATERIALS = {
    1: {
        "name": "岩石洞窟", "base": 5, "light": 6, "dark": 1,
        "edge": 13, "accent": 10, "debris": [5, 6, 7, 13],
        "floor": 1, "ceiling": 0
    },
    2: {
        "name": "レンガ要塞", "base": 8, "light": 9, "dark": 2,
        "edge": 10, "accent": 7, "debris": [2, 8, 9, 10],
        "floor": 2, "ceiling": 1
    },
    3: {
        "name": "宇宙の塔", "base": 1, "light": 12, "dark": 0,
        "edge": 5, "accent": 7, "debris": [1, 5, 12, 7],
        "floor": 0, "ceiling": 1
    },
    4: {
        "name": "氷迷宮", "base": 12, "light": 13, "dark": 1,
        "edge": 7, "accent": 10, "debris": [7, 10, 11, 12, 13],
        "floor": 1, "ceiling": 0
    },
    5: {
        "name": "最終魔宮", "base": 4, "light": 10, "dark": 2,
        "edge": 9, "accent": 7, "debris": [2, 4, 7, 9, 10],
        "floor": 2, "ceiling": 0
    },
}

MAPS = [
    # Wave 1
    [
        "111111111111111111111111",
        "100000010000000100000001",
        "101110010111100101111001",
        "101000000100010000000101",
        "101011111010010111110101",
        "101000001000000100000101",
        "111101011111111111011111",
        "100001010000000001010001",
        "101111010111111001111101",
        "100000000100001000000001",
        "111101111110011111101111",
        "100001000000000000100001",
        "101101011111111110101101",
        "101100000000000000001101",
        "100001111011101111000001",
        "111101000010010000101111",
        "100000010100010101000001",
        "101111010111110101111101",
        "101000000000000000000101",
        "101011111011101111100101",
        "101000001000000100000101",
        "100001100011100011000001",
        "100001000000000000100001",
        "111111111111111111111111",
    ],
    # Wave 2
    [
        "111111111111111111111111",
        "100000000001000000000001",
        "101110111101011110111001",
        "101000100000000001000101",
        "101010101111111101010101",
        "100010000001000000010001",
        "111111110101010111111111",
        "100000010100010100000001",
        "101110010111110100111001",
        "101000000000000000000101",
        "101011110111110111100101",
        "100000010100010100000001",
        "111101010111110101011111",
        "100001000000000000100001",
        "101111110111110111111101",
        "100000000000000000000001",
        "101011101110011101110101",
        "101000100000000001000101",
        "101011101111111011100101",
        "100000000001000000000001",
        "101111111001001111111101",
        "101000000001000000000101",
        "100000000000000000000001",
        "111111111111111111111111",
    ],
    # Wave 3
    [
        "111111111111111111111111",
        "100000000010010000000001",
        "101111011010010110111101",
        "101000010000000010000101",
        "101011010111110101100101",
        "100011000001000000110001",
        "111011111001001111110111",
        "100000001001001000000001",
        "101111010000000010111101",
        "100001010111110101000001",
        "111001000100010000100111",
        "100001110101010111000001",
        "101100000000000000001101",
        "101011110111110111101101",
        "101000000001000000000101",
        "101011111001001111100101",
        "100000001000000100000001",
        "101111010111110101111101",
        "100001000000000000100001",
        "101101111011101111011001",
        "101000000001000000000101",
        "101011111001001111100101",
        "100000000000000000000001",
        "111111111111111111111111",
    ],
    # Wave 4
    [
        "111111111111111111111111",
        "100000000000000000000001",
        "101111011110011110111101",
        "101000010000000010000101",
        "101011010111110101100101",
        "101000000001000000000101",
        "101011111001001111100101",
        "100001000000000000100001",
        "111101011110011110101111",
        "100000001000000100000001",
        "101111010111110101111101",
        "100001000000000000100001",
        "111101111110011111101111",
        "100000000010010000000001",
        "101111110010010011111101",
        "100000010000000100000001",
        "101011100111110011101001",
        "100000000100010000000001",
        "101111100100010011111101",
        "101000100000000001000101",
        "101000111011101111000101",
        "101000000011100000000101",
        "100000000000000000000001",
        "111111111111111111111111",
    ],
    # Wave 5
    [
        "111111111111111111111111",
        "100000000001000000000001",
        "101111111010010111111101",
        "101000001010010100000101",
        "101011101000000010110101",
        "101011101011110101110101",
        "101000001000000100000101",
        "101111111011110111111101",
        "100000000011110000000001",
        "111101111111111111101111",
        "100001000000000000100001",
        "101101011110033330101101",
        "101100011110033330001101",
        "100001000000000000100001",
        "111101111111111111101111",
        "100000000000000000000001",
        "101111111101101111111101",
        "100000000010010000000001",
        "111111100010010001111111",
        "100000100000000001000001",
        "101101111100011111011001",
        "101000000000000000000101",
        "100000000000000000000001",
        "111111111111111111111111",
    ]
]

class App:
    def __init__(self):
        self.is_mobile = False
        try:
            import js
            ua = js.navigator.userAgent.lower()
            if any(k in ua for k in ["iphone", "ipad", "ipod", "android", "mobile"]):
                self.is_mobile = True
        except ImportError:
            pass
            
        win_h = HEIGHT
        pyxel.init(WIDTH, win_h, title="FPS迷路戦闘・波状戦", fps=60)
        
        try:
            self.font = pyxel.Font(FONT_FILE)
        except Exception:
            self.font = None

        self.init_sounds()
        
        if self.is_mobile:
            pyxel.mouse(True)
            
        self.BTN_ACT_A = pyxel.GAMEPAD1_BUTTON_Y
        self.BTN_ACT_C = pyxel.GAMEPAD1_BUTTON_BACK
        self.BTN_START = pyxel.GAMEPAD1_BUTTON_START

        self.state = "TITLE"
        self.prev_state = None
        self.state_timer = 0
        self.mobile_wait_release = self.is_mobile
        self.prev_state = "TITLE"
        self.state_timer = 0
        self.mobile_wait_release = self.is_mobile
        
        self.max_wave = MAX_WAVES 
        self.wave = 1
        self.ai_mode = False 
        
        self.invincible = False
        self.cheat_sequence = [pyxel.KEY_UP, pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_DOWN]
        self.cheat_index = 0
        
        self.px, self.py, self.pa = 2.5, 2.5, 0
        self.hp = 100
        
        self.flash_timer = 0
        self.damage_flash = 0
        self.shake = 0
        self.head_bob = 0.0
        self.wave_announce_timer = 0
        self.particles = []
        self.projectiles = []
        self.explosions = []
        self.health_items = []
        self.clear_timer = 0
        
        self.boss_death_timer = 0
        self.boss_spawn_timer = 0
        self.boss_spawned = False
        self.boss_ref = None
        
        self.gameover_choice = 0  # 0: はい, 1: いいえ
        
        pyxel.run(self.update, self.draw)

    def init_sounds(self):
        pyxel.sounds[1].set("a2g2c1", "n", "7", "f", 4)
        pyxel.sounds[2].set("c1c0", "s", "7", "v", 6)
        pyxel.sounds[3].set("c3e3g3c4", "t", "7", "v", 6)
        pyxel.sounds[4].set("g1f1e1d1c1", "n", "7", "f", 8)
        pyxel.sounds[5].set("c2e2g2c3e3g3c4", "s", "7", "f", 4)
        pyxel.sounds[6].set("c1c0g2c0", "s", "7654", "f", 15)
        pyxel.sounds[7].set("c3g3c4", "p", "7", "v", 8)
        pyxel.sounds[8].set("e3g3c4", "t", "7", "v", 8)
        
        # ボス撃破時の専用ダウンSE (サウンド9)
        pyxel.sounds[9].set("c2b1a1g1f1e1d1c1", "s", "7654", "f", 18)

        pyxel.sounds[20].set("c3e3g3c4 e3g3c4e4", "t", "6", "v", 12)
        pyxel.sounds[21].set("a2c3e3g3 f3a3c4e4", "t", "6", "v", 12)
        pyxel.sounds[22].set("c4g3e3g3 c4g3e3g3", "p", "4", "n", 12)
        pyxel.sounds[23].set("c1c1r c1 f1f1r f1", "s", "7", "f", 12)
        pyxel.musics[0].set([20, 21], [22, 22], [23, 23])

        bgm_data = [
            {"m": ["e2e2b1e2 g2e2d2e2", "c2c2g1c2 e2c2b1c2"], "a": "e3b2g2b2 e3b2g2b2", "b": "e1e1r e1 c1c1r c1"},
            {"m": ["c3c3g2c3 d#3c3a#2c3", "g2g2d2g2 a#2g2f2g2"], "a": "c4g3d#3g3 c4g3d#3g3", "b": "c2c2r c2 g1g1r g1"},
            {"m": ["f2g2a2b2 c3d3f3g3", "a2b2c3d3 f3g3a3b3"], "a": "f4c#4a3c#4 f4c#4a3c#4", "b": "f1a1c2a1 d#1g1b1g1"},
            {"m": ["d3f#3a3d4 c4a3f#3d3", "b2d3f#3b3 a3f#3d3b2"], "a": "d4a3f#3a3 d4a3f#3a3", "b": "d2r d2r b1r b1r"},
            {"m": ["a2c3e3a3 b3g3e3d3", "f2a2c3f3 g3e3c3b2"], "a": "a3e3c3e3 a3e3c3e3", "b": "a1a1a1a1 f1f1f1f1"}
        ]
        
        for w in range(5):
            snd_base = 24 + w * 4
            pyxel.sounds[snd_base].set(bgm_data[w]["m"][0], "t", "6", "v", 12)
            pyxel.sounds[snd_base+1].set(bgm_data[w]["m"][1], "t", "6", "v", 12)
            pyxel.sounds[snd_base+2].set(bgm_data[w]["a"], "p", "4", "n", 12)
            pyxel.sounds[snd_base+3].set(bgm_data[w]["b"], "s", "7", "f", 12)
            
            pyxel.musics[w+1].set(
                [snd_base, snd_base+1], 
                [snd_base+2, snd_base+2], 
                [snd_base+3, snd_base+3]
            )

        pyxel.sounds[44].set("c3e3g3c4 e4g4c4g4", "t", "6", "v", 12)
        pyxel.sounds[45].set("a3c4e4g4 f4a4c4a4", "t", "6", "v", 12)
        pyxel.sounds[46].set("c4g3e3g3 c4g3e3g3", "p", "4", "n", 12)
        pyxel.sounds[47].set("c1c1r c1 f1f1r f1", "s", "7", "f", 12)
        pyxel.musics[6].set([44, 45], [46, 46], [47, 47])

        pyxel.sounds[48].set("g3e3d3c3 b2a2g2f#2", "t", "6", "v", 10)
        pyxel.sounds[49].set("e2d2c2b1 a1g1f#1e1", "t", "6", "v", 10)
        pyxel.sounds[50].set("e3b2g2b2 e3b2g2b2", "p", "4", "n", 10)
        pyxel.sounds[51].set("e1r e1r e1r e1r", "s", "7", "f", 10)
        pyxel.musics[7].set([48, 49], [50, 50], [51, 51])

        # 最終決戦（最高司令官出現）用のサウンド定義（サウンド52〜55）
        pyxel.sounds[52].set("g3g3c4d4 e4f4g4a4", "t", "6", "v", 15)
        pyxel.sounds[53].set("c3d3e3f3 g3a3b3c4", "t", "6", "v", 15)
        pyxel.sounds[54].set("c4g3c3g3 c4g3c3g3", "p", "4", "n", 15)
        pyxel.sounds[55].set("c1r c1r c1r c1r", "s", "7", "f", 15)

    def load_map(self):
        m_data = MAPS[min(self.wave - 1, len(MAPS) - 1)]
        self.map = [[int(c) for c in row] for row in m_data]
        self.map_w = len(self.map[0])
        self.map_h = len(self.map)

    def is_open_space(self, x, y):
        ix, iy = int(x), int(y)
        if self.wall(ix, iy) > 0: return False
        open_count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if 0 <= ix + dx < self.map_w and 0 <= iy + dy < self.map_h:
                    if self.map[iy + dy][ix + dx] == 0:
                        open_count += 1
        return open_count >= 5

    def init_wave(self):
        self.load_map()
        self.px, self.py, self.pa = 2.5, 2.5, math.pi/4
        self.head_bob = 0.0
        
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = int(self.px) + dx, int(self.py) + dy
                if 0 <= nx < self.map_w and 0 <= ny < self.map_h:
                    self.map[ny][nx] = 0

        self.hp = 100
        self.flash_timer = 0
        self.wave_announce_timer = 120
        self.particles = []
        self.projectiles = []
        self.explosions = []
        self.enemies = []
        self.health_items = []
        self.boss_spawned = False
        self.boss_spawn_timer = 0
        
        pyxel.play(3, 5) 
        pyxel.playm(self.wave, loop=True) 
        
        for _ in range(2):
            while True:
                rx, ry = random.uniform(2, self.map_w-2), random.uniform(2, self.map_h-2)
                if self.is_open_space(rx, ry) and math.sqrt((rx-self.px)**2 + (ry-self.py)**2) > 4:
                    self.health_items.append({"x": rx, "y": ry, "alive": True})
                    break

        boss_hp = 15 + (self.wave * 5)
        if self.wave < self.max_wave:
            while True:
                rx, ry = random.uniform(2, self.map_w-2), random.uniform(2, self.map_h-2)
                if self.is_open_space(rx, ry) and math.sqrt((rx-self.px)**2 + (ry-self.py)**2) > 8:
                    boss_type = f"boss{self.wave}"
                    self.enemies.append({"x": rx, "y": ry, "alive": True, "type": boss_type, "hp": boss_hp, "max_hp": boss_hp, "timer": 0})
                    break

        num_enemies = self.wave * 2 + 1
        for _ in range(num_enemies):
            while True:
                rx, ry = random.uniform(2, self.map_w-2), random.uniform(2, self.map_h-2)
                if self.is_open_space(rx, ry) and math.sqrt((rx-self.px)**2 + (ry-self.py)**2) > 6:
                    r = random.random()
                    if r < 0.3 + (self.wave * 0.05): etype = "brute"
                    elif r < 0.7: etype = "soldier"
                    else: etype = "drone"
                    
                    hp = 8 if etype == "brute" else (4 if etype == "soldier" else 2)
                    self.enemies.append({"x": rx, "y": ry, "alive": True, "type": etype, "hp": hp, "max_hp": hp, "timer": random.randint(0,100)})
                    break

    def wall(self, x, y):
        if x < 0 or y < 0 or x >= self.map_w or y >= self.map_h: return 1
        return self.map[int(y)][int(x)]

    def add_particles(self, x, y, count, col_choices, is_blood=False):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(0.05, 0.3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            vz = random.uniform(-0.15, 0.4) if not is_blood else random.uniform(0, 0.3)
            life = random.randint(15, 35)
            col = random.choice(col_choices)
            self.particles.append([x, y, 0.5, vx, vy, vz, life, col])
        if len(self.particles) > 120:
            self.particles = self.particles[-120:]

    def add_explosion(self, x, y, colors=None, power=1.0):
        if colors is None:
            colors = [7, 10, 12, 9]
        self.explosions.append({
            "x": x, "y": y, "life": 24, "max_life": 24, "power": power,
            "colors": colors, "seed": random.randint(0, 9999)
        })
        if len(self.explosions) > 15:
            self.explosions.pop(0)
        self.add_particles(x, y, int(20 + 15 * power), colors)
        pyxel.play(3, 4)

    def update(self):
        if self.prev_state != self.state:
            self.state_timer = 0
            if self.state == "TITLE":
                pyxel.playm(0, loop=True) 
                if self.is_mobile:
                    self.mobile_wait_release = True
            elif self.state == "GAMEOVER":
                pyxel.playm(7, loop=False) 
                self.gameover_choice = 0
            elif self.state == "CLEAR":
                pyxel.playm(6, loop=True) 
            self.prev_state = self.state
        else:
            self.state_timer += 1

        if self.shake > 0: self.shake -= 1
        if self.damage_flash > 0: self.damage_flash -= 1
        if self.wave_announce_timer > 0: self.wave_announce_timer -= 1

        if self.state == "TITLE":
            if pyxel.play_pos(0) is None:
                pyxel.playm(0, loop=True)

            for key in [pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_LEFT, pyxel.KEY_RIGHT]:
                if pyxel.btnp(key):
                    if key == self.cheat_sequence[self.cheat_index]:
                        self.cheat_index += 1
                        if self.cheat_index == len(self.cheat_sequence):
                            self.invincible = True
                            self.cheat_index = 0
                    else:
                        self.cheat_index = 1 if key == self.cheat_sequence[0] else 0

            # 15秒（900フレーム）放置でデモ画面（ATTRACT_DEMO）へ移行
            if self.state_timer >= 900:
                self.state = "ATTRACT_DEMO"
                self.state_timer = 0
                self.wave = 1
                self.ai_mode = True
                self.invincible = False
                self.init_wave()
                return

            if self.is_mobile:
                # 起動時・タイトル表示直後の誤タップ判定を無視するガード処理（20フレーム = 約0.3秒）
                if self.state_timer < 20:
                    return

                if self.mobile_wait_release:
                    if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                        return

                    self.mobile_wait_release = False
                    return

                if pyxel.btnp(self.BTN_START):
                    pyxel.play(3, 7)
                    self.state = "MISSION"
                    return

                return
            # PC・ゲームパッド
            if (
                pyxel.btnp(pyxel.KEY_A)
                or pyxel.btnp(pyxel.KEY_SPACE)
                or pyxel.btnp(self.BTN_ACT_A)
                or pyxel.btnp(self.BTN_START)
                or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X)
            ):
                pyxel.play(3, 7)
                self.state = "MISSION"

        elif self.state == "ATTRACT_DEMO":
            # ユーザー入力があったらタイトルへ戻る
            any_input = (
                pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_C) or
                pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START) or
                pyxel.btnp(self.BTN_ACT_A) or pyxel.btnp(self.BTN_ACT_C) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or
                (self.is_mobile and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT))
            )
            if any_input:
                self.state = "TITLE"
                self.state_timer = 0
                self.ai_mode = False
                self.invincible = False
                pyxel.playm(0, loop=True)
                return

            # デモプレイ：40秒（2400フレーム）。1〜4面を交互に繰り返す（各面10秒 = 600フレーム）
            target_wave = (self.state_timer // 600) % 4 + 1
            if self.wave != target_wave:
                self.wave = target_wave
                self.init_wave()
                self.ai_mode =True 
                self.invincible = False

            if self.hp < 30:
                self.hp = 100

            self.update_play()

            # 40秒経過したらチュートリアル（ATTRACT_TUTORIAL）へ
            if self.state_timer >= 2400:
                self.state = "ATTRACT_TUTORIAL"
                self.state_timer = 0

        elif self.state == "ATTRACT_TUTORIAL":
            # ユーザー入力があったらタイトルへ戻る
            any_input = (
                pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_C) or
                pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT) or
                pyxel.btnp(self.BTN_ACT_A) or pyxel.btnp(self.BTN_ACT_C) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or
                (self.is_mobile and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT))
            )
            if any_input:
                self.state = "TITLE"
                self.state_timer = 0
                self.ai_mode = False
                self.invincible = False
                pyxel.playm(0, loop=True)
                return

            # チュートリアル：10秒（600フレーム）流れたらデモプレイに戻る（ループ）
            if self.state_timer >= 600:
                self.state = "ATTRACT_DEMO"
                self.state_timer = 0
                self.wave = 1
                self.ai_mode = True
                self.invincible = False
                self.init_wave()

        elif self.state == "MISSION":
            if self.is_mobile and self.mobile_wait_release:
                if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                    self.mobile_wait_release = False
            elif pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(self.BTN_ACT_A) or pyxel.btnp(self.BTN_START) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or (self.is_mobile and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
                pyxel.play(3, 7) 
                self.state = "TUTORIAL"

        elif self.state == "TUTORIAL":
            if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(self.BTN_ACT_A) or pyxel.btnp(self.BTN_START) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or (self.is_mobile and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
                pyxel.play(3, 7) 
                self.state = "PLAY"
                self.wave = 1
                self.init_wave()
                
        elif self.state == "PLAY" or self.state == "BOSS_SPAWN":
            if self.state == "PLAY" and pyxel.play_pos(0) is None: 
                pyxel.playm(self.wave, loop=True)
                
            if pyxel.btnp(pyxel.KEY_C) or pyxel.btnp(pyxel.KEY_CTRL) or pyxel.btnp(self.BTN_ACT_C):
                pyxel.play(3, 7) 
                self.ai_mode = not self.ai_mode
                
            self.update_play()
            
            if self.state == "BOSS_SPAWN":
                self.update_boss_spawn()
            
        elif self.state == "BOSS_DEATH":
            self.update_boss_death()
            
        elif self.state == "GAMEOVER":
            gameover_duration = 600  # 10秒 (60fps * 10)
            if self.state_timer >= gameover_duration:
                self.state = "TITLE"
                self.invincible = False
                return

            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
                pyxel.play(3, 7)
                self.gameover_choice = 1 - self.gameover_choice

            if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(self.BTN_ACT_A) or pyxel.btnp(self.BTN_START) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or (self.is_mobile and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
                pyxel.play(3, 7)
                if self.is_mobile and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    mx = pyxel.mouse_x
                    if mx < WIDTH // 2:
                        self.gameover_choice = 0
                    else:
                        self.gameover_choice = 1

                if self.gameover_choice == 0:
                    # はい（コンティニュー）
                    self.hp = 100
                    self.init_wave()
                    self.state = "PLAY"
                else:
                    # いいえ（タイトルへ）
                    self.state = "TITLE"
                    self.invincible = False
                
        elif self.state == "CLEAR":
            self.clear_timer += 1
            self.shake = 0

            if self.clear_timer > 2620:
                self.state = "TITLE"
                self.invincible = False

    def update_boss_spawn(self):
        self.boss_spawn_timer += 1
        progress = min(1.0, self.boss_spawn_timer / 180.0)
        
        if self.boss_ref:
            start_x, start_y = float(self.map_w - 2.5), float(self.map_h - 2.5)
            target_x, target_y = float(self.map_w - 6.5), float(self.map_h - 6.5)
            self.boss_ref["x"] = start_x + (target_x - start_x) * progress
            self.boss_ref["y"] = start_y + (target_y - start_y) * progress

        if self.boss_spawn_timer >= 180:
            self.state = "PLAY"
            pyxel.playm(5, loop=True)

    def update_play(self):
        move_forward, move_backward, turn_left, turn_right, shoot_trigger = False, False, False, False, False

        if self.ai_mode:
            nearest_enemy, min_dist = None, 999.0
            for en in self.enemies:
                if en["alive"]:
                    dist = math.sqrt((en["x"] - self.px)**2 + (en["y"] - self.py)**2)
                    if dist < min_dist:
                        min_dist, nearest_enemy = dist, en
            
            if nearest_enemy:
                target_angle = math.atan2(nearest_enemy["y"] - self.py, nearest_enemy["x"] - self.px)
                angle_diff = (target_angle - self.pa + math.pi) % (math.pi * 2) - math.pi
                
                ai_turn_speed = ROT_SPEED * 2.5
                if abs(angle_diff) > ai_turn_speed:
                    if angle_diff > 0: self.pa += ai_turn_speed
                    else: self.pa -= ai_turn_speed
                else:
                    self.pa = target_angle
                
                check_dx, check_dy = math.cos(self.pa) * 1.5, math.sin(self.pa) * 1.5
                if self.wall(self.px + check_dx, self.py + check_dy):
                    self.pa += 0.3
                    
                if min_dist > 4.0: move_forward = True
                elif min_dist < 3.0: move_backward = True
                
                if min_dist < 15.0 and abs(angle_diff) < 1.2 and self.flash_timer == 0:
                    shoot_trigger = True
            else:
                self.pa += ROT_SPEED * 2.0
        else:
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX) < -30: turn_left = True
            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX) > 30: turn_right = True
            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY) < -30: move_forward = True
            if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY) > 30: move_backward = True
            
            if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(self.BTN_ACT_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_X): 
                shoot_trigger = True
                

        if turn_left: self.pa -= ROT_SPEED
        if turn_right: self.pa += ROT_SPEED
        
        dx, dy = math.cos(self.pa) * MOVE_SPEED, math.sin(self.pa) * MOVE_SPEED
        
        is_actually_moving = False
        if move_forward:
            if not self.wall(self.px + dx, self.py): self.px += dx; is_actually_moving = True
            if not self.wall(self.px, self.py + dy): self.py += dy; is_actually_moving = True
        if move_backward:
            if not self.wall(self.px - dx, self.py): self.px -= dx; is_actually_moving = True
            if not self.wall(self.px, self.py - dy): self.py -= dy; is_actually_moving = True

        self.is_moving = is_actually_moving
        if self.is_moving:
            self.head_bob += 0.28
        else:
            self.head_bob *= 0.8

        for item in self.health_items:
            if item["alive"]:
                dist = math.hypot(item["x"] - self.px, item["y"] - self.py)
                if dist < 0.6:
                    self.hp = min(100, self.hp + 25)
                    item["alive"] = False
                    pyxel.play(3, 3) 
                    self.add_particles(self.px, self.py, 15, [11, 7, 10], is_blood=False)

        if shoot_trigger and self.flash_timer == 0:
            self.flash_timer = 12
            self.shake = 3
            pyxel.play(3, 1) 
            vx = math.cos(self.pa) * 0.45
            vy = math.sin(self.pa) * 0.45
            self.projectiles.append({"x": self.px, "y": self.py, "vx": vx, "vy": vy, "type": "player"})
            if len(self.projectiles) > 40:
                self.projectiles.pop(0)

        if self.flash_timer > 0: self.flash_timer -= 1

        for en in self.enemies:
            if not en["alive"]: continue
            if self.state == "BOSS_SPAWN" and en["type"] == "final_boss":
                continue
                
            en["timer"] += 1
            dist = math.sqrt((en["x"]-self.px)**2 + (en["y"]-self.py)**2)
            
            edx, edy = 0, 0
            if en["type"] == "brute":
                speed = 0.02
                edx = speed if self.px > en["x"] else -speed
                edy = speed if self.py > en["y"] else -speed
                if dist < 0.8 and pyxel.frame_count % 30 == 0:
                    if not self.invincible:
                        self.hp -= 20
                        self.damage_flash = 10
                        self.shake = 5
                        pyxel.play(3, 2) 
                    
            elif en["type"] == "soldier":
                speed = 0.03
                if dist > 5:
                    edx = speed if self.px > en["x"] else -speed
                    edy = speed if self.py > en["y"] else -speed
                elif dist < 3:
                    edx = -speed if self.px > en["x"] else speed
                    edy = -speed if self.py > en["y"] else speed
                    
                if dist < 8 and en["timer"] % 60 == 0:
                    ex, ey = (self.px - en["x"])/max(0.001, dist), (self.py - en["y"])/max(0.001, dist)
                    self.projectiles.append({"x": en["x"], "y": en["y"], "vx": ex*0.15, "vy": ey*0.15, "type": "enemy"})
                    if len(self.projectiles) > 40:
                        self.projectiles.pop(0)

            elif en["type"].startswith("boss") or en["type"] == "final_boss":
                speed = 0.012 if en["type"] == "final_boss" else 0.015
                edx = speed if self.px > en["x"] else -speed
                edy = speed if self.py > en["y"] else -speed
                shoot_freq = 30 if en["type"] == "final_boss" else 40
                if dist < 12 and en["timer"] % shoot_freq == 0:
                    ex, ey = (self.px - en["x"])/max(0.001, dist), (self.py - en["y"])/max(0.001, dist)
                    proj_speed = 0.22 if en["type"] == "final_boss" else 0.2
                    self.projectiles.append({"x": en["x"], "y": en["y"], "vx": ex*proj_speed, "vy": ey*proj_speed, "type": "enemy"})
                    if len(self.projectiles) > 40:
                        self.projectiles.pop(0)
                    
            elif en["type"] == "drone":
                speed = 0.05
                base_dx = speed if self.px > en["x"] else -speed
                base_dy = speed if self.py > en["y"] else -speed
                zig = math.sin(en["timer"] * 0.1) * 0.05
                edx = base_dx + zig * (-base_dy)
                edy = base_dy + zig * base_dx
                if dist < 0.6 and pyxel.frame_count % 15 == 0:
                    if not self.invincible:
                        self.hp -= 5
                        self.damage_flash = 5
                        pyxel.play(3, 2) 

            if not self.wall(en["x"] + edx, en["y"]): en["x"] += edx
            if not self.wall(en["x"], en["y"] + edy): en["y"] += edy

        for proj in self.projectiles[:]:
            proj["x"] += proj["vx"]
            proj["y"] += proj["vy"]
            
            if self.wall(proj["x"], proj["y"]):
                mx, my = int(proj["x"]), int(proj["y"])
                if proj["type"] == "player":
                    if 0 < mx < self.map_w - 1 and 0 < my < self.map_h - 1:
                        self.map[my][mx] = 0
                        mat = WALL_MATERIALS.get(self.wave, WALL_MATERIALS[1])
                        pyxel.play(3, 6) 
                        self.add_explosion(proj["x"], proj["y"], [mat["dark"], mat["base"], mat["light"], 7], 1.6)
                        self.add_particles(proj["x"], proj["y"], 45, mat["debris"], is_blood=False)
                    else:
                        cols = [8, 9, 10, 5, 1]
                        self.add_explosion(proj["x"], proj["y"], cols, 1.2)
                else:
                    cols = [8, 9, 10, 5, 1]
                    self.add_explosion(proj["x"], proj["y"], cols, 0.9)
                
                self.projectiles.remove(proj)
                continue
            
            if proj["type"] == "enemy":
                p_dist = math.sqrt((proj["x"]-self.px)**2 + (proj["y"]-self.py)**2)
                if p_dist < 0.5:
                    if not self.invincible:
                        self.hp -= 15
                        self.damage_flash = 10
                        self.shake = 5
                        pyxel.play(3, 2) 
                    self.projectiles.remove(proj)
                    self.add_explosion(self.px, self.py, [8, 10, 7, 2], 1.0)
            else:
                hit_enemy = False
                for en in self.enemies:
                    if not en["alive"]: continue
                    if self.state == "BOSS_SPAWN" and en["type"] == "final_boss":
                        continue
                        
                    e_dist = math.sqrt((proj["x"]-en["x"])**2 + (proj["y"]-en["y"])**2)
                    if e_dist < 0.6:
                        en["hp"] -= 4
                        pyxel.play(3, 8) 
                        self.add_explosion(en["x"], en["y"], [10, 9, 8, 2, 5], 1.0)
                        self.add_particles(en["x"], en["y"], 12, [8, 2, 0], is_blood=True)
                        
                        if en["hp"] <= 0 and en["alive"]:
                            if self.wave == self.max_wave and en["type"] == "final_boss":
                                en["hp"] = 0
                                if self.state != "BOSS_DEATH":
                                    self.state = "BOSS_DEATH"
                                    self.boss_death_timer = 0
                                    self.boss_ref = en
                                    pyxel.stop()
                                    pyxel.play(3, 9)
                            else:
                                en["alive"] = False
                                self.add_explosion(en["x"], en["y"], [9, 10, 8, 5, 1], 1.8)
                                self.add_particles(en["x"], en["y"], 35, [9, 8, 5, 1, 0])
                                
                        hit_enemy = True
                        break
                if hit_enemy:
                    self.projectiles.remove(proj)

        for ex in self.explosions[:]:
            ex["life"] -= 1
            if ex["life"] <= 0:
                self.explosions.remove(ex)

        for p in self.particles[:]:
            p[0] += p[3]; p[1] += p[4]; p[2] += p[5]
            p[5] -= 0.015
            if p[2] < 0: 
                p[2] = 0
                p[5] *= -0.4
                p[3] *= 0.7
                p[4] *= 0.7
            p[6] -= 1
            if p[6] <= 0: self.particles.remove(p)

        if self.hp <= 0:
            if self.state == "ATTRACT_DEMO":
                self.hp = 100
                self.init_wave()
            else:
                self.state = "GAMEOVER"
                return
            
        if self.state == "PLAY" and len(self.enemies) > 0 and not any(en["alive"] for en in self.enemies):
            if self.wave == self.max_wave and not self.boss_spawned:
                self.boss_spawned = True
                self.state = "BOSS_SPAWN"
                self.boss_spawn_timer = 0
                boss_hp = 35 
                
                bx, by = float(self.map_w - 2.5), float(self.map_h - 2.5)
                self.boss_ref = {
                    "x": bx, "y": by, "alive": True, "type": "final_boss",
                    "hp": boss_hp, "max_hp": boss_hp, "timer": 0
                }
                self.enemies.append(self.boss_ref)
                pyxel.stop()
                pyxel.musics[5].set([52, 53], [54, 54], [55, 55])
                pyxel.playm(5, loop=True)
                self.wave_announce_timer = 180
            else:
                self.wave += 1
                if self.wave > self.max_wave:
                    if self.state == "ATTRACT_DEMO":
                        self.wave = 1
                        self.init_wave()
                    else:
                        self.state = "CLEAR"
                        self.clear_timer = 0
                        pyxel.play(3, 5) 
                else:
                    self.init_wave()

        # デモモード中で敵全滅またはウェーブ進行時のケア
        if self.state == "ATTRACT_DEMO" and len(self.enemies) > 0 and not any(en["alive"] for en in self.enemies):
            self.init_wave()

    def update_boss_death(self):
        self.boss_death_timer += 1
        max_death_time = 300  
        
        if self.boss_death_timer % 30 == 0 and self.boss_death_timer < max_death_time - 60:
            pyxel.play(3, 8)
            ex_x = self.boss_ref["x"] + random.uniform(-0.6, 0.6)
            ex_y = self.boss_ref["y"] + random.uniform(-0.6, 0.6)
            self.add_explosion(ex_x, ex_y, [10, 9, 8, 2, 5], 1.2)
            self.shake = 2
            
        if self.boss_death_timer % 3 == 0:
            for p in self.particles[:]:
                p[0] += p[3] * 0.4; p[1] += p[4] * 0.4; p[2] += p[5] * 0.4
                p[5] -= 0.01
                if p[2] < 0: 
                    p[2] = 0; p[5] *= -0.4; p[3] *= 0.7; p[4] *= 0.7
                p[6] -= 1
                if p[6] <= 0: self.particles.remove(p)
                
            for ex in self.explosions[:]:
                ex["life"] -= 0.5
                if ex["life"] <= 0:
                    self.explosions.remove(ex)
                    
        if self.boss_death_timer == max_death_time - 60:
            pyxel.play(3, 6)
            self.shake = 12
            self.damage_flash = 6 
            self.add_explosion(self.boss_ref["x"], self.boss_ref["y"], [9, 10, 8, 5, 1], 2.5)
            self.add_particles(self.boss_ref["x"], self.boss_ref["y"], 50, [9, 8, 5, 1, 0])
            
        if self.boss_death_timer >= max_death_time:
            self.boss_ref["alive"] = False
            self.state = "CLEAR"
            self.clear_timer = 0
            pyxel.play(3, 5)

    def draw(self):
        cx = random.randint(-self.shake, self.shake) if self.shake else 0
        cy = random.randint(-self.shake, self.shake) if self.shake else 0
        pyxel.camera(cx, cy)

        if self.state == "TITLE": self.draw_title()
        elif self.state == "ATTRACT_DEMO":
            self.draw_play()
            self._jtext_center(HEIGHT - 14, "【デモ画面】(スペース/A/スタートでタイトルへ)", 10)
        elif self.state == "ATTRACT_TUTORIAL":
            self.draw_tutorial()
            self._jtext_center(HEIGHT - 14, "【操作方法】(スペース/A/スタートでタイトルへ)", 10)
        elif self.state == "MISSION": self.draw_mission()
        elif self.state == "TUTORIAL": self.draw_tutorial()
        elif self.state == "PLAY" or self.state == "BOSS_DEATH" or self.state == "BOSS_SPAWN": self.draw_play()
        elif self.state == "GAMEOVER": self.draw_gameover()
        elif self.state == "CLEAR": self.draw_clear()

        pyxel.camera(0, 0)


    def _text_width(self, s):
        if hasattr(self, "font") and self.font:
            return self.font.text_width(str(s))
        return len(str(s)) * 8

    def _jtext(self, x, y, s, color):
        if hasattr(self, "font") and self.font:
            pyxel.text(x, y, str(s), color, self.font)
        else:
            pyxel.text(x, y, str(s), color)

    def _jtext_center(self, y, s, color):
        x = (WIDTH - self._text_width(s)) // 2
        self._jtext(x, y, s, color)

    def _panel(self, x, y, w, h, fill=0, border=5, accent=12):
        pyxel.rect(x, y, w, h, fill)
        pyxel.rectb(x, y, w, h, border)
        if w > 8 and h > 8:
            pyxel.line(x + 2, y + 2, x + w - 3, y + 2, accent)

    def _draw_shadow_text(self, x, y, s, color):
        self._jtext(x + 1, y + 1, s, 0)
        self._jtext(x, y, s, color)

    def draw_action_background(self):
        t = pyxel.frame_count
        half = HEIGHT // 2
        
        for y in range(half):
            q = y / max(1, half - 1)
            col = 1 if q < .3 else 5
            pyxel.line(0, y, WIDTH - 1, y, col)
            
        for y in range(half, HEIGHT):
            d = (y - half + 1) / (HEIGHT - half)
            col = 1 if d < .4 else 2
            pyxel.line(0, y, WIDTH - 1, y, col)

        horizon = half
        for i in range(-10, 11):
            bx = WIDTH // 2 + int(i * 16 + (t * 2) % 16)
            pyxel.line(WIDTH // 2, horizon, bx, HEIGHT, 1)

        enemy_type_idx = (t // 180) % 5 + 1
        sx = WIDTH // 2 + int(math.sin(t * 0.08) * 40)
        sy = half + int(math.cos(t * 0.05) * 10)
        
        self.draw_intro_graphic(enemy_type_idx, sx, sy)
        
        for i in range(12):
            lx = (i * 37 + t * 4) % WIDTH
            ly = (i * 19 + t * 2) % HEIGHT
            pyxel.line(lx, ly, lx + 8, ly + 2, 8 if i % 2 == 0 else 7)

    def draw_title(self):
        pyxel.cls(0)
        self.draw_action_background()

        progress = min(1.0, self.state_timer / 12.0)
        ease = (1.0 - progress) ** 2

        t = pyxel.frame_count
        title = "Ｔ.Ｋ PRESENTS"
        sub = "FPS迷路・波状戦"
        tx = (WIDTH - self._text_width(title)) // 2
        sx = (WIDTH - self._text_width(sub)) // 2

        ty_pos = int(30 + ease * -60)
        sub_y_pos = int(44 + ease * 60)

        self._jtext(tx + 2, ty_pos + 2, title, 1)
        self._jtext(tx, ty_pos, title, 10)
        self._jtext(tx - 1, ty_pos - 1, title, 7)
        self._jtext(sx, sub_y_pos, sub, 12)

        if self.invincible:
            self._jtext(WIDTH // 2 - 40, 56, "－ 無敵モード －", 10)

        panel_x_offset = int(ease * 250)
        self._panel(43 + panel_x_offset, 70, 170, 36, 0, 5, 12)
        self._jtext_center(75, "戦闘サバイバルゲーム", 6)
        
        if t % 60 < 42:
            if self.is_mobile:
                self._jtext(WIDTH // 2 - self._text_width("＞ スタートボタンで開始 ＜") // 2, 90, "＞ スタートボタンで開始 ＜", 10)
            else:
                self._jtext(WIDTH // 2 - self._text_width("＞スペース/A/スタートで開始＜") // 2, 90, "＞スペース/A/スタートで開始＜", 10)
        self._jtext(WIDTH // 2 - self._text_width("制作著作 T.K/M.T") // 2, 117, "制作著作 T.K/M.T", 7)
        self._jtext(WIDTH // 2 - self._text_width("Mirai Work Co., Ltd. 2026") // 2, 132, "Mirai Work Co., Ltd. 2026", 11)

    def draw_mission(self):
        pyxel.cls(0)
        self.draw_action_background()

        progress = min(1.0, self.state_timer / 10.0)
        ease = (1.0 - progress) ** 2
        p_offset = int(ease * -250)

        self._panel(18 + p_offset, 12, 220, 120, 0, 5, 10)
        self._draw_shadow_text(95 + p_offset, 20, "作戦目的", 10)
        
        self._jtext(32 + p_offset, 42, "未知の迷宮エリアに侵入した", 7)
        self._jtext(32 + p_offset, 58, "敵勢力を全滅させよ！", 7)
        self._jtext(32 + p_offset, 74, "全5ウェーブを突破し、", 7)
        self._jtext(32 + p_offset, 90, "最高司令官を撃破して生還せよ。", 7)

        self._jtext_center(114, "スペース/A/スタートで次へ", 11)

    def draw_tutorial(self):
        pyxel.cls(0)
        self.draw_action_background()

        progress = min(1.0, self.state_timer / 10.0)
        ease = (1.0 - progress) ** 2
        p_offset = int(ease * 250)

        self._panel(18 + p_offset, 12, 220, 120, 0, 5, 10)
        
        self._draw_shadow_text(95 + p_offset, 18, "操作方法 ＆ ルール", 10)
        
        self._jtext(32 + p_offset, 34, "上・下キー：移動", 7)
        self._jtext(32 + p_offset, 48, "左右キー：方向転換", 7)
        self._jtext(32 + p_offset, 62, "スペース/Aキー：射撃", 7)
        self._jtext(32 + p_offset, 76, "セレクト/CTRLキー：自動操縦切替", 7)
        
        self._jtext(44 + p_offset, 92, "ポーション：近づくと体力25回復", 11)
        ix = 32 + p_offset
        iy = 92
        pyxel.rect(ix, iy, 8, 10, 7)
        pyxel.rectb(ix, iy, 8, 10, 3)
        pyxel.rect(ix + 2, iy + 3, 4, 5, 11)
        pyxel.rect(ix + 3, iy + 1, 2, 2, 11)

        self._jtext_center(112, "スペース/A/スタートで開始", 11)

    def draw_gameover(self):
        pyxel.cls(0)
        t = pyxel.frame_count

        for y in range(HEIGHT):
            c = 8 if ((y + t // 3) % 13 == 0) else (2 if y % 5 == 0 else 0)
            pyxel.line(0, y, WIDTH - 1, y, c)

        for i in range(70):
            y = (i * 31 + t * (i % 3 + 1)) % HEIGHT
            x = (i * 53 + t) % WIDTH
            ln = 4 + (i * 7) % 35
            pyxel.line(x, y, min(WIDTH - 1, x + ln), y, random.choice([2, 8, 10]))

        progress = min(1.0, self.state_timer / 10.0)
        ease = (1.0 - progress) ** 2
        drop_y = int(ease * -100)

        self._panel(38, 26 + drop_y, 180, 96, 0, 8, 8)
        msg = "通信途絶"
        x = (WIDTH - self._text_width(msg)) // 2
        self._jtext(x + 2, 34 + 2 + drop_y, msg, 2)
        self._jtext(x, 34 + drop_y, msg, 8)
        
        self._jtext_center(50 + drop_y, "コンテニューしますか？", 7)

        yes_col = 10 if self.gameover_choice == 0 else 7
        no_col = 10 if self.gameover_choice == 1 else 7
        yes_str = ("> " if self.gameover_choice == 0 else "  ") + "はい"
        no_str = ("> " if self.gameover_choice == 1 else "  ") + "いいえ"

        self._jtext(WIDTH // 2 - 35, 68 + drop_y, yes_str, yes_col)
        self._jtext(WIDTH // 2 + 10, 68 + drop_y, no_str, no_col)

        gameover_duration = 600
        remaining_frames = max(0, gameover_duration - self.state_timer)
        remaining_secs = math.ceil(remaining_frames / 60)
        count_msg = f"タイトルへ戻るまで: {remaining_secs}秒"
        self._jtext_center(84 + drop_y, count_msg, 10)

        if t % 60 < 40:
            if self.is_mobile:
                self._jtext(WIDTH // 2 - self._text_width("左右で選択/画面タップで決定") // 2, 102 + drop_y, "左右で選択/画面タップで決定", 11)
            else:
                self._jtext(WIDTH // 2 - self._text_width("左右選択/スペース/A/スタート決定") // 2, 102 + drop_y, "左右選択/スペース/A/スタート決定", 11)

    def draw_clear(self):
        t = self.clear_timer
        
        if t < 600:
            self.flash_timer = 0
            self.draw_play()

            index = (t // 100) % 6
            
            intros = [
                ("プレイヤー", "生存者", "迷宮を生き抜いた勇敢な戦闘員。"),
                ("ドローン", "偵察機", "高速で飛行し追跡する機械。"),
                ("兵士", "突撃兵", "射撃武器を持つ敵兵。"),
                ("重装兵", "重装甲", "強力な近接攻撃を行う重装兵。"),
                ("総統", "赤縄主", "各エリアを支配する赤い強敵。"),
                ("最高司令官", "最終覇王", "全ての元凶である最強の敵。")
            ]
            name, role, desc = intros[index]

            sub_timer = t % 100
            progress = min(1.0, sub_timer / 8.0)
            ease = (1.0 - progress) ** 2
            scale_offset = int(ease * 150)

            pw, ph = 240, 68
            px_pos = WIDTH // 2 - pw // 2
            py_pos = HEIGHT // 2 - ph // 2
            
            pyxel.rect(px_pos - scale_offset, py_pos, pw, ph + scale_offset * 2 // 3, 0)
            pyxel.rectb(px_pos - scale_offset, py_pos, pw, ph + scale_offset * 2 // 3, 5)
            pyxel.rectb(px_pos - scale_offset + 2, py_pos + 2, pw - 4, ph + scale_offset * 2 // 3 - 4, 12)

            cx_icon = px_pos + 42 - scale_offset
            cy_icon = py_pos + ph // 2
            self.draw_intro_graphic(index, cx_icon, cy_icon)

            tx = px_pos + 82 - scale_offset
            self._jtext(tx, py_pos + 8, "CAST", 6)
            self._draw_shadow_text(tx, py_pos + 22, name, 10)
            self._jtext(tx, py_pos + 36, f"[{role}]", 7)
            self._jtext(tx, py_pos + 50, desc, 13)

        elif t <= 2200:
            pyxel.cls(0)
            
            for y in range(HEIGHT // 2):
                col = 2 if y % 2 == 0 else (8 if (y + t // 3) % 4 == 0 else 0)
                pyxel.line(0, y, WIDTH - 1, y, col)
                
            for y in range(HEIGHT // 2, HEIGHT):
                col = 8 if (y + t) % 3 == 0 else (9 if (y + t // 2) % 5 == 0 else 2)
                pyxel.line(0, y, WIDTH - 1, y, col)

            for x in range(0, WIDTH, 20):
                h_wall = 35 + (x * 17) % 20
                pyxel.rect(x, HEIGHT // 2 - h_wall, 18, h_wall, 1)
                pyxel.rect(x + 4, HEIGHT // 2 - h_wall + 8, 10, 12, 0)

            for i in range(14):
                bx = (i * 41 + t * 3) % WIDTH
                by = HEIGHT // 2 - 15 + (i * 23) % 45
                r = ((i * 11 + t * 4) % 18) + 6
                c = 8 if (t + i) % 3 == 0 else (10 if (t + i) % 3 == 1 else 9)
                pyxel.circ(bx, by, r, c)
                pyxel.circ(bx, by, r // 2, 7)

            for i in range(35):
                fx = (i * 59 - t * 4) % WIDTH
                fy = (i * 37 + t * 3) % HEIGHT
                if fy > HEIGHT // 2 - 30:
                    pyxel.pset(fx, fy, 7 if i % 2 == 0 else 10)

            panel_w, panel_h = 220, 120
            
            roll_progress = t - 600
            slide_offset = max(0, roll_progress * 0.4 - 400)
            
            panel_x = WIDTH // 2 - panel_w // 2
            panel_y = (HEIGHT // 2 - panel_h // 2) - slide_offset
            
            pyxel.rect(panel_x, panel_y, panel_w, panel_h, 0)
            pyxel.rectb(panel_x, panel_y, panel_w, panel_h, 5)
            pyxel.rectb(panel_x + 2, panel_y + 2, panel_w - 4, panel_h - 4, 12)

            cy = (HEIGHT // 2 + panel_h // 2) - roll_progress * 0.4
            
            credits_data = [
                ("ＭＩＳＳＩＯＮ ＣＯＭＰＬＥＴＥ", 10),
                ("おめでとうございます！", 7),
                ("", 0),
                ("監督・プログラム", 11),
                ("Ｔ．Ｋ", 7),
                ("", 0),
                ("アレンジ・音楽", 11),
                ("Ｍ．Ｔ", 7),
                ("", 0),
                ("協力", 11),
                ("チームＴ．Ｄ", 7),
                ("", 0),
                ("総合演出", 11),
                ("M．Ｔ", 7),
                ("", 0),
                ("あなたと全プレイヤーへ", 11),
                ("Ａ・ＲＩ・ＧＡ・ＴＯＵ！", 10),
                ("", 0),
                ("制作・著作 Ｔ．Ｋ/Ｍ．Ｔ", 13),
                ("Mirai Work Co., Ltd. 2026", 13)
            ]

            pyxel.clip(panel_x + 3, panel_y + 3, panel_w - 6, panel_h - 6)
            for i, (s, c) in enumerate(credits_data):
                yy = int(cy + i * 20)
                if s:
                    x = (WIDTH - self._text_width(s)) // 2
                    self._draw_shadow_text(x, yy, s, c)
            pyxel.clip()
        else:
            ft = t - 2200
            max_ft = 420
            progress = min(1.0, ft / max_ft)
            
            pyxel.cls(0)
            
            cx, cy = WIDTH // 2, HEIGHT // 2
            random.seed(100)
            
            if progress < 0.5:
                if int(ft * 0.5) % 2 == 0:
                    pyxel.cls(7 if progress < 0.1 else 10)
                
                for i in range(50):
                    ang = i * 1.7 + ft * 0.1
                    dist = (ft * 1.5 + (i * 13) % 40) * (1.0 - progress * 0.5)
                    px_pos = cx + math.cos(ang) * dist
                    py_pos = cy + math.sin(ang) * dist * 0.7
                    col = random.choice([7, 10, 9, 8])
                    pyxel.pset(int(px_pos), int(py_pos), col)

            for i in range(80):
                seed_x = (i * 37) % WIDTH - WIDTH // 2
                seed_y = (i * 23) % 40 - 20
                
                rise_speed = 0.4 + (i % 5) * 0.1
                spread = ft * rise_speed
                
                px_pos = cx + seed_x * (0.2 + progress * 1.2) + math.sin(ft * 0.05 + i) * 8
                py_pos = cy + seed_y - spread + math.cos(ft * 0.03 + i) * 5
                
                if py_pos < -10:
                    continue
                
                smoke_size = int(3 + progress * 14 + (i % 4))
                
                if progress < 0.25:
                    col = random.choice([10, 9, 8, 7])
                elif progress < 0.6:
                    col = random.choice([13, 6, 5])
                else:
                    col = random.choice([5, 1, 13]) if i % 2 == 0 else 1
                
                if 0 <= py_pos < HEIGHT + 10 and 0 <= px_pos < WIDTH + 10:
                    pyxel.circ(int(px_pos), int(py_pos), max(1, smoke_size), col)
                    if smoke_size > 4:
                        pyxel.circ(int(px_pos) - 1, int(py_pos) - 1, max(1, smoke_size // 2), 1 if col != 1 else 5)

            if progress > 0.3:
                fade_progress = (progress - 0.3) / 0.7
                for yy in range(0, HEIGHT, max(1, int(4 - fade_progress * 3))):
                    for xx in range(0, WIDTH, max(1, int(4 - fade_progress * 3))):
                        if (xx + yy + int(ft * 0.2)) % max(2, int(7 - fade_progress * 5)) == 0:
                            pyxel.pset(xx, yy, 0)
                            
            if progress > 0.85:
                pyxel.cls(0)

    def draw_intro_graphic(self, index, x, y):
        if index == 0:  # プレイヤー
            pyxel.rect(x - 8, y - 12, 16, 20, 1)
            pyxel.rect(x - 6, y - 10, 12, 10, 6)
            pyxel.rect(x - 2, y - 2, 4, 10, 12)
            pyxel.rect(x - 3, y - 14, 6, 4, 7)
        elif index == 1:  # ドローン
            pyxel.circ(x, y, 10, 13)
            pyxel.circb(x, y, 10, 12)
            pyxel.circ(x, y, 4, 10)
            pyxel.line(x - 12, y - 8, x + 12, y + 8, 7)
        elif index == 2:  # 兵士
            pyxel.rect(x - 8, y - 12, 16, 22, 3)
            pyxel.rect(x - 4, y - 8, 8, 8, 4)
            pyxel.line(x - 8, y + 2, x + 8, y + 2, 11)
        elif index == 3:  # 重装兵
            pyxel.rect(x - 12, y - 14, 24, 26, 2)
            pyxel.rectb(x - 12, y - 14, 24, 26, 4)
            pyxel.rect(x - 6, y - 8, 12, 8, 3)
            pyxel.rect(x - 4, y - 4, 8, 4, 10)
        elif index == 4:  # 総統（赤い敵）
            pyxel.rect(x - 14, y - 14, 28, 26, 8)
            pyxel.rectb(x - 14, y - 14, 28, 26, 2)
            pyxel.rect(x - 10, y - 8, 20, 10, 2)
            pyxel.circ(x, y - 2, 4, 10)
            pyxel.circ(x, y - 2, 1, 7)
        elif index == 5:  # 最高司令官（もっと豪華でリアルな敵）
            pyxel.rect(x - 16, y - 18, 32, 32, 2)
            pyxel.rectb(x - 16, y - 18, 32, 32, 8)
            pyxel.rect(x - 12, y - 14, 24, 24, 0)
            pyxel.rectb(x - 12, y - 14, 24, 24, 10)
            pyxel.rect(x - 8, y - 10, 16, 16, 9)
            pyxel.circ(x, y - 2, 6, 8)
            pyxel.circ(x, y - 2, 3, 10)
            pyxel.circ(x, y - 2, 1, 7)
            pyxel.tri(x - 16, y - 18, x - 22, y - 24, x - 10, y - 18, 10)
            pyxel.tri(x + 16, y - 18, x + 10, y - 18, x + 22, y - 24, 10)
            pyxel.line(x - 16, y + 14, x - 20, y + 18, 8)
            pyxel.line(x + 16, y + 14, x + 20, y + 18, 8)

    def _material(self):
        return WALL_MATERIALS.get(self.wave, WALL_MATERIALS[1])

    def _wall_texture(self, material_id, hit_x, hit_y, side, dist):
        m = WALL_MATERIALS.get(material_id, WALL_MATERIALS[1])
        fx = hit_x % 1.0
        fy = hit_y % 1.0
        
        is_edge = (fx < 0.08 or fx > 0.92 or fy < 0.08 or fy > 0.92)
        if is_edge:
            return m["dark"]

        if material_id == 1:  # 岩石洞窟
            n = int((hit_x * 23 + hit_y * 37) * 7) % 5
            return m["light"] if n == 0 else (m["dark"] if n == 1 else m["base"])

        elif material_id == 2:  # レンガ要塞
            bx = int(hit_x * 4)
            by = int(hit_y * 4)
            if by % 2 == 1:
                bx = int(hit_x * 4 + 0.5)
            if (hit_x * 4 % 1.0 < 0.15) or (hit_y * 4 % 1.0 < 0.15):
                return m["dark"]
            return m["light"] if (bx + by) % 2 == 0 else m["base"]

        elif material_id == 3:  # 宇宙の塔（デジタル・サイバーパネル）
            grid_x, grid_y = int(fx * 8), int(fy * 8)
            if grid_x == 0 or grid_y == 0 or grid_x == 7 or grid_y == 7:
                return m["accent"]
            if 2 <= grid_x <= 5 and 2 <= grid_y <= 5:
                return m["light"] if (grid_x + grid_y + pyxel.frame_count // 15) % 2 == 0 else m["base"]
            return m["dark"]

        elif material_id == 4:  # 氷迷宮（シャープな氷の結晶・ダイアモンドカット模様）
            cx = abs(fx - 0.5)
            cy = abs(fy - 0.5)
            pattern = int((cx + cy) * 16) % 3
            if pattern == 0:
                return 7  # 輝くハイライト（白）
            elif pattern == 1:
                return m["light"]
            return m["base"] if side == 0 else m["dark"]

        else:  # 最終魔宮
            plank = int(hit_x * 5) % 2
            if fx < 0.12 or fx > 0.88:
                return m["dark"]
            return m["light"] if plank == 0 else m["base"]

    def _draw_wall_detail(self, x, top, bottom, material_id, hit_x, hit_y, side, dist):
        if bottom <= top:
            return
        m = WALL_MATERIALS.get(material_id, WALL_MATERIALS[1])
        h = bottom - top + 1
        
        step = 1 if dist < 9 else 2
        for yy in range(top, bottom + 1, step):
            rel = (yy - top) / max(1, h)
            c = self._wall_texture(material_id, hit_x, hit_y + rel, side, dist)
            if dist > 8:
                if (x + yy) % 2 == 0: c = m["dark"]
            if dist < 12:
                pyxel.pset(x, yy, c)

        if dist < 10:
            pyxel.pset(x, top, m["accent"])
            pyxel.pset(x, bottom, m["dark"])

    def draw_play(self):
        bob = int(math.sin(self.head_bob) * 3)
        half = (HEIGHT // 2) + bob
        flash = self.flash_timer > 0
        t = pyxel.frame_count
        m = self._material()

        if self.wave == 3:
            for y in range(half):
                col = 0 if y < half // 2 else 1
                pyxel.line(0, y, WIDTH - 1, y, col)
            for i in range(40):
                sx = (i * 53 + 17) % WIDTH
                sy = (i * 29 + 3) % max(1, half)
                if (t + i) % 30 < 20:
                    pyxel.pset(sx, sy, 7 if i % 3 == 0 else 12)
        elif self.wave == 4:
            for y in range(half):
                q = y / max(1, half - 1)
                col = 12 if int(q * 10 + math.sin(t * 0.05 + y * 0.1) * 3) % 3 == 0 else 1
                if q < 0.3: col = 0
                pyxel.line(0, y, WIDTH - 1, y, col)
            for i in range(50):
                sx = (i * 41 + t * 2) % WIDTH
                sy = (i * 19 + t * 3) % max(1, half)
                pyxel.pset(sx, sy, 7 if i % 2 == 0 else 13)
        else:
            sky_top = 1 if self.wave != 4 else 0
            sky_mid = 5 if self.wave != 4 else 13
            for y in range(half):
                q = y / max(1, half - 1)
                col = sky_top if q < .18 else (5 if q < .55 else sky_mid)
                if q > 0.4 and (y + t) % 2 == 0: col = m["dark"]
                pyxel.line(0, y, WIDTH - 1, y, col)

        for i in range(58):
            sx = (i * 71 + 19 + self.wave * 13) % WIDTH
            sy = (i * 23 + 7) % max(1, HEIGHT // 2 - 10) + bob
            tw = (i + t // (6 + i % 5)) % 11
            if tw < 8 and 0 <= sy < half:
                pyxel.pset(sx, sy, 7 if i % 7 == 0 else 13 if self.wave == 4 else 1)

        for y in range(half, HEIGHT):
            d = (y - half + 1) / (HEIGHT - half)
            base_col = m["floor"] if d < .35 else (5 if d < .75 else m["dark"])
            if d < 0.2 and (y + t) % 2 == 0: base_col = m["dark"]
            pyxel.line(0, y, WIDTH - 1, y, base_col)

        for i in range(16):
            yy = half + int((i / 16) ** 2.05 * (HEIGHT - half))
            if yy < HEIGHT:
                pyxel.line(0, yy, WIDTH - 1, yy, 13 if i in (3, 9, 14) else m["dark"])

        angle_offset = (self.pa * 18) % 24
        for i in range(-16, 17):
            bx = WIDTH // 2 + int(i * 11 - angle_offset)
            pyxel.line(WIDTH // 2, half, bx, HEIGHT, m["dark"])

        if flash and self.flash_timer > 9:
            pyxel.rectb(0, 0, WIDTH, HEIGHT, 10)
            pyxel.rectb(1, 1, WIDTH-2, HEIGHT-2, 9)

        z_buffer = [999.0] * WIDTH

        for x in range(WIDTH):
            ray_angle = self.pa - FOV / 2 + FOV * x / WIDTH
            vx, vy = math.cos(ray_angle), math.sin(ray_angle)
            mx, my = int(self.px), int(self.py)

            delta_x = abs(1 / vx) if vx != 0 else 1e30
            delta_y = abs(1 / vy) if vy != 0 else 1e30

            if vx < 0:
                sx_dir, side_x = -1, (self.px - mx) * delta_x
            else:
                sx_dir, side_x = 1, (mx + 1 - self.px) * delta_x
            if vy < 0:
                sy_dir, side_y = -1, (self.py - my) * delta_y
            else:
                sy_dir, side_y = 1, (my + 1 - self.py) * delta_y

            side = 0
            for _ in range(64):
                if side_x < side_y:
                    side_x += delta_x
                    mx += sx_dir
                    side = 0
                else:
                    side_y += delta_y
                    my += sy_dir
                    side = 1
                if self.wall(mx, my) > 0:
                    break

            if side == 0:
                raw_dist = (mx - self.px + (1 - sx_dir) / 2) / vx
                hit = self.py + raw_dist * vy
                hit_x = hit
                hit_y = my
            else:
                raw_dist = (my - self.py + (1 - sy_dir) / 2) / vy
                hit = self.px + raw_dist * vx
                hit_x = mx
                hit_y = hit

            dist = max(0.05, raw_dist * math.cos(ray_angle - self.pa))
            z_buffer[x] = dist
            h = int(HEIGHT / dist)

            if dist > 14:
                col = m["dark"]
            else:
                tex = self._wall_texture(self.wave, hit_x, hit_y, side, dist)
                shade = 0
                if side == 0:
                    shade = -1
                if dist > 8:
                    shade -= 1
                col = max(0, tex + shade)

            top = max(0, half - h // 2)
            bottom = min(HEIGHT - 1, half + h // 2)
            
            if dist > 9 and x % 2 == 0:
                col = m["dark"]

            pyxel.line(x, top, x, bottom, col)

            if dist < 12:
                self._draw_wall_detail(x, top, bottom, self.wave, hit_x, hit_y, side, dist)

            if dist < 9 and x % 3 == 0:
                edge_y = top + max(1, int((bottom - top) * .08))
                if top < edge_y < bottom:
                    pyxel.pset(x, edge_y, m["edge"])

        self.draw_sprites(z_buffer)
        if self.state != "CLEAR":
            self.draw_ui()

        if self.wave_announce_timer > 0:
            ann_w, ann_h = 168, 34
            ax = WIDTH // 2 - ann_w // 2
            ay = HEIGHT // 2 - ann_h // 2
            pyxel.rect(ax, ay, ann_w, ann_h, 0)
            pyxel.rectb(ax, ay, ann_w, ann_h, m["accent"])
            pyxel.rectb(ax + 2, ay + 2, ann_w - 4, ann_h - 4, m["edge"])
            if self.state == "BOSS_SPAWN":
                self._jtext_center(ay + 5, "－ 最高司令官 出現 －", 8)
                self._jtext_center(ay + 18, "最終決戦！", 10)
            else:
                self._jtext_center(ay + 5, f"－ 波状戦 {self.wave} ／ {m['name']} －", 7)
                self._jtext_center(ay + 18, "任務開始", 10)

        if self.damage_flash > 0:
            intensity = 8 if self.damage_flash % 3 else 2
            pyxel.rectb(0, 0, WIDTH - 1, HEIGHT - 1, intensity)
            pyxel.rectb(2, 2, WIDTH - 5, HEIGHT - 5, intensity)

    def draw_sprites(self, z_buffer):
        sprites = []
        for en in self.enemies:
            if en["alive"]:
                dist = math.hypot(en["x"] - self.px, en["y"] - self.py)
                sprites.append((dist, en["x"], en["y"], en["type"], en))
        for item in self.health_items:
            if item["alive"]:
                dist = math.hypot(item["x"] - self.px, item["y"] - self.py)
                sprites.append((dist, item["x"], item["y"], "health", item))
        for ex in self.explosions:
            dist = math.hypot(ex["x"] - self.px, ex["y"] - self.py)
            sprites.append((dist, ex["x"], ex["y"], "explosion", ex))
        for p in self.particles:
            dist = math.hypot(p[0] - self.px, p[1] - self.py)
            sprites.append((dist, p[0], p[1], "particle", p))
        for pr in self.projectiles:
            dist = math.hypot(pr["x"] - self.px, pr["y"] - self.py)
            sprites.append((dist, pr["x"], pr["y"], "projectile", pr))

        sprites.sort(key=lambda s: s[0], reverse=True)
        for sp in sprites:
            self.draw_at_3d(sp[1], sp[2], sp[3], sp[0], z_buffer, sp[4])

    def draw_at_3d(self, x, y, sp_type, dist, z_buffer, obj_data):
        if dist < 0.01: return

        angle = math.atan2(y - self.py, x - self.px)
        rel_angle = (angle - self.pa + math.pi) % (math.pi * 2) - math.pi

        if abs(rel_angle) >= FOV / 2 + 0.25: return
        sx = int((rel_angle / FOV + 0.5) * WIDTH)
        if not (0 <= sx < WIDTH): return
        
        if dist > 0.8 and (z_buffer[sx] + 0.3 < dist): return

        size = min(max(2, int(HEIGHT / dist)), 800)
        t = pyxel.frame_count

        bob = int(math.sin(self.head_bob) * 3)

        if sp_type == "health":
            item_bob = int(math.sin(t * 0.15) * max(1, size // 10))
            yy = HEIGHT // 2 + item_bob + bob
            r = max(2, size // 6)
            pyxel.rect(sx - r // 2, yy - r, r, r * 2, 7)
            pyxel.rectb(sx - r // 2, yy - r, r, r * 2, 3)
            pyxel.rect(sx - r // 4, yy - r // 2, r // 2, r, 11)
            pyxel.rect(sx - r // 2, yy - r // 4, r, r // 2, 11)
            return

        if sp_type == "explosion":
            life = obj_data["life"]
            max_life = obj_data["max_life"]
            progress = 1.0 - life / max_life
            power = obj_data["power"]
            yy = HEIGHT // 2 + bob

            cols = obj_data["colors"]
            ring_radius = int(size * 0.8 * progress * power)
            
            if ring_radius > 0 and ring_radius < size * 1.5:
                thick = 2 if progress < 0.3 else 1
                out_col = cols[1] if progress < 0.4 else cols[-1]
                pyxel.circb(sx, yy, ring_radius, out_col)
                if thick == 2:
                    pyxel.circb(sx, yy, ring_radius - 1, cols[0])

            core_rad = int(size * 0.4 * (1.0 - progress) * power)
            if core_rad > 0:
                inner_col = cols[0] if progress < 0.2 else cols[1]
                smoke_col = cols[-1] if progress > 0.6 else cols[2]
                
                pyxel.circ(sx, yy, max(1, core_rad // 2), inner_col)
                pyxel.circb(sx, yy, core_rad, smoke_col)
                
                ray_count = 8
                for i in range(ray_count):
                    ang = i * math.pi * 2 / ray_count + obj_data["seed"] * 0.001
                    ray_len = int(core_rad * 1.5)
                    ex_x = sx + int(math.cos(ang) * ray_len)
                    ex_y = yy + int(math.sin(ang) * ray_len)
                    
                    if progress < 0.5:
                        pyxel.pset(ex_x, ex_y, random.choice([cols[0], cols[1]]))
                    elif progress < 0.8:
                        pyxel.pset(ex_x, ex_y, cols[-1])

            return

        if sp_type == "particle":
            pz = obj_data[2]
            yy = HEIGHT // 2 + int(size * (0.55 - pz)) + bob
            r = max(1, size // 16)
            pyxel.circ(sx, yy, r + 1, 0)
            pyxel.pset(sx, yy, obj_data[7])
            return

        if sp_type == "projectile":
            yy = HEIGHT // 2 + bob

            r = max(2, size // 13)
            color = 12 if obj_data.get("type") == "player" else 10

            pyxel.line(sx, yy + r + 2, sx, yy + r + 6, 7)
            if r >= 3:
                pyxel.pset(sx - 1, yy + r + 5, 9)
                pyxel.pset(sx + 1, yy + r + 5, 9)

            pyxel.line(sx - r, yy + r - 1, sx - r - 2, yy + r + 3, color)
            pyxel.line(sx + r, yy + r - 1, sx + r + 2, yy + r + 3, color)

            body_h = max(4, r * 3)
            pyxel.rect(sx - max(1, r // 2), yy - r, max(2, r), body_h, color)

            pyxel.tri(
                sx, yy - r - 4,
                sx - max(1, r // 2), yy - r,
                sx + max(1, r // 2), yy - r,
                7
            )

            pyxel.line(sx, yy - r + 1, sx, yy + r, 7)
            return

        enemy_bob = int(math.sin(t * 0.18 + dist) * max(1, size // 12)) + bob

        if sp_type == "final_boss":
            w, h = max(16, int(size * 1.8)), max(20, int(size * 2.1))
            
            yy_offset = 0
            if self.state == "BOSS_DEATH" and obj_data.get("hp", 1) <= 0:
                progress = min(1.0, self.boss_death_timer / 300.0)
                collapse = progress ** 2.0
                death_squash = int(h * collapse * 0.9)
                h = max(2, h - death_squash)
                w = w + int(death_squash * 0.4)
                yy_offset = int(death_squash * 0.5) 
            
            yy = HEIGHT // 2 - h // 4 + enemy_bob + yy_offset
            
            pyxel.rect(sx - w // 2 - 2, yy - h // 2 - 2, w + 4, h + 4, 0)
            pyxel.rect(sx - w // 2, yy - h // 2, w, h, 2)
            pyxel.rectb(sx - w // 2, yy - h // 2, w, h, 8)
            
            inner_w, inner_h = w * 3 // 4, h * 3 // 4
            pyxel.rect(sx - inner_w // 2, yy - inner_h // 2, inner_w, inner_h, 0)
            pyxel.rectb(sx - inner_w // 2, yy - inner_h // 2, inner_w, inner_h, 10)
            
            if h > 10:
                core_col = 10 if t % 8 < 4 else 7
                pyxel.circ(sx, yy, max(3, w // 5), core_col)
                pyxel.circ(sx, yy, max(1, w // 10), 7)
                pyxel.line(sx - w // 3, yy - h // 3, sx + w // 3, yy - h // 3, 9)
                pyxel.line(sx - w // 3, yy + h // 3, sx + w // 3, yy + h // 3, 9)

            if self.state != "BOSS_DEATH":
                hp_ratio = max(0, obj_data["hp"]) / obj_data["max_hp"]
                pyxel.rect(sx - w // 2, yy - h // 2 - 8, w, 4, 1)
                pyxel.rect(sx - w // 2, yy - h // 2 - 8, max(1, int(w * hp_ratio)), 4, 8)

        elif sp_type.startswith("boss"):
            w, h = max(12, int(size * 1.4)), max(16, int(size * 1.6))
            yy = HEIGHT // 2 - h // 4 + enemy_bob
            
            pyxel.rect(sx - w // 2 - 1, yy - h // 2 - 1, w + 2, h + 2, 0)
            pyxel.rect(sx - w // 2, yy + h // 2 - 4, w, 4, 0)
            pyxel.rect(sx - w // 2, yy - h // 2, w, h, 8)
            pyxel.rectb(sx - w // 2, yy - h // 2, w, h, 2)
            
            if h > 8:
                pyxel.line(sx - w // 2 + 2, yy - h // 2 + 2, sx + w // 2 - 2, yy - h // 2 + 2, 10)
                pyxel.rect(sx - w // 4, yy - h // 4, w // 2, h // 2, 0)
                eye = 10 if t % 10 < 5 else 7
                pyxel.circ(sx, yy, max(2, w // 6), eye)
            
            hp_ratio = max(0, obj_data["hp"]) / obj_data["max_hp"]
            pyxel.rect(sx - w // 2, yy - h // 2 - 6, w, 3, 1)
            pyxel.rect(sx - w // 2, yy - h // 2 - 6, max(1, int(w * hp_ratio)), 3, 8)

        elif sp_type == "brute":
            w, h = max(6, size), max(8, int(size * 1.18))
            yy = HEIGHT // 2 - h // 4 + enemy_bob
            pyxel.rect(sx - w // 2 - 1, yy - h // 2 - 1, w + 2, h + 2, 0)
            pyxel.rect(sx - w // 2, yy + h // 2 - 3, w, 3, 0)
            pyxel.rect(sx - w // 2, yy - h // 2, w, h, 2)
            pyxel.rectb(sx - w // 2, yy - h // 2, w, h, 4)
            pyxel.rect(sx - w // 3, yy - h // 2 + 2, max(2, w * 2 // 3), max(3, h // 3), 3)
            pyxel.line(sx - w // 2 + 2, yy, sx + w // 2 - 2, yy, 1)
            pyxel.line(sx - w // 3, yy + h // 4, sx + w // 3, yy + h // 4, 4)
            eye = 8 if t % 12 < 8 else 10
            pyxel.rect(sx - w // 4, yy - h // 4, max(2, w // 7), max(2, h // 10), eye)
            pyxel.rect(sx + w // 4 - max(2, w // 7), yy - h // 4, max(2, w // 7), max(2, h // 10), eye)
            hp_ratio = max(0, obj_data["hp"]) / obj_data["max_hp"]
            pyxel.rect(sx - w // 2, yy - h // 2 - 5, w, 2, 1)
            pyxel.rect(sx - w // 2, yy - h // 2 - 5, max(1, int(w * hp_ratio)), 2, 8)

        elif sp_type == "soldier":
            w, h = max(5, size // 2), max(8, size)
            yy = HEIGHT // 2 + enemy_bob
            pyxel.rect(sx - w // 2 - 1, yy - h // 2 - 1, w + 2, h + 2, 0)
            pyxel.rect(sx - w // 2, yy - h // 2, w, h, 3)
            pyxel.rect(sx - w // 3, yy - h // 5, max(2, w * 2 // 3), max(3, h // 3), 4)
            pyxel.rectb(sx - w // 3, yy - h // 5, max(2, w * 2 // 3), max(3, h // 3), 5)
            pyxel.rect(sx - w // 2 + 1, yy - h // 3, max(2, w - 2), max(2, h // 8), 0)
            pyxel.line(sx - w // 3, yy - h // 3, sx + w // 3, yy - h // 3, 11)
            pyxel.rect(sx + w // 3, yy - 1, max(3, w // 2), max(2, h // 7), 1)
            pyxel.rect(sx + w // 3, yy - 2, max(2, w // 3), 1, 7)
            pyxel.line(sx - w // 4, yy + h // 3, sx - w // 4, yy + h // 2, 5)
            pyxel.line(sx + w // 4, yy + h // 3, sx + w // 4, yy + h // 2, 5)

        elif sp_type == "drone":
            w = max(6, int(size * 0.62))
            yy = HEIGHT // 2 - size // 2 + enemy_bob
            if t % 8 < 4:
                pyxel.line(sx - w // 2, yy + w // 2, sx - w // 2 - 2, yy + w // 2 + 4, 7)
                pyxel.line(sx + w // 2, yy + w // 2, sx + w // 2 + 2, yy + w // 2 + 4, 7)
            pyxel.circ(sx, yy, w // 2 + 3, 0)
            pyxel.circ(sx, yy, w // 2, 13)
            pyxel.circb(sx, yy, w // 2, 12)
            pyxel.line(sx - w // 2, yy, sx + w // 2, yy, 12)
            pyxel.line(sx, yy - w // 2, sx, yy + w // 2, 12)
            core = 7 if t % 10 < 5 else 10
            pyxel.circ(sx, yy, max(2, w // 4), 1)
            pyxel.circ(sx, yy, max(1, w // 5), core)
            hp_ratio = max(0, obj_data["hp"]) / obj_data["max_hp"]
            pyxel.rect(sx - w // 2, yy - w // 2 - 5, w, 2, 1)
            pyxel.rect(sx - w // 2, yy - w // 2 - 5, max(1, int(w * hp_ratio)), 2, 10)

    def draw_ui(self):
        t = pyxel.frame_count

        pyxel.rect(0, 0, WIDTH, 39, 0)
        pyxel.line(0, 38, WIDTH - 1, 38, 5)
        pyxel.line(0, 39, WIDTH - 1, 39, 1)

        hp_col = 8 if self.hp < 30 else (10 if self.hp < 60 else 11)
        self._jtext(7, 3, "体力", 7)
        pyxel.rect(7, 16, 78, 7, 1)
        pyxel.rectb(7, 16, 78, 7, 5)
        hpw = int(74 * max(0, min(100, self.hp)) / 100)
        if hpw: pyxel.rect(9, 18, hpw, 3, hp_col)
        self._jtext(89, 16, f"{max(0, self.hp):03d}", hp_col)

        self._jtext(7, 26, f"波状戦 {self.wave:02d}/{self.max_wave:02d}", 10)
        alive = sum(1 for en in self.enemies if en["alive"])
        self._jtext(90, 26, f"敵残数 {alive:02d}", 8 if alive else 11)

        if self.invincible:
            pyxel.rect(174, 23, 73, 15, 3)
            pyxel.rectb(174, 23, 73, 15, 7)
            self._jtext(182, 26, "無敵状態", 7)

        s = 2
        mw, mh = self.map_w * s, self.map_h * s
        mox, moy = WIDTH - mw - 5, 44
        pyxel.rect(mox - 3, moy - 3, mw + 6, mh + 6, 0)
        pyxel.rectb(mox - 3, moy - 3, mw + 6, mh + 6, 5)

        pyxel.clip(mox, moy, mox + mw, moy + mh)

        for y, row in enumerate(self.map):
            for x, v in enumerate(row):
                if v > 0: pyxel.rect(mox + x * s, moy + y * s, s, s, 5)

        for item in self.health_items:
            if item["alive"]:
                ix, iy = int(mox + item["x"] * s), int(moy + item["y"] * s)
                pyxel.pset(ix, iy, 7)
                pyxel.pset(ix - 1, iy, 11)
                pyxel.pset(ix + 1, iy, 11)
                pyxel.pset(ix, iy - 1, 11)
                pyxel.pset(ix, iy + 1, 11)

        for en in self.enemies:
            if en["alive"]:
                if en["type"] == "final_boss": 
                    c = 8 if (t // 8) % 2 == 0 else 10  # 赤(8)と黄色(10)の点滅
                elif en["type"].startswith("boss"): c = 8
                elif en["type"] == "brute": c = 9
                elif en["type"] == "soldier": c = 11
                else: c = 10
                ex, ey = int(mox + en["x"] * s), int(moy + en["y"] * s)
                pyxel.rect(ex - 1, ey - 1, 3, 3, c)

        pxm, pym = mox + self.px * s, moy + self.py * s
        pyxel.circ(int(pxm), int(pym), 2, 9)
        pyxel.line(int(pxm), int(pym),
                   int(pxm + math.cos(self.pa) * 6),
                   int(pym + math.sin(self.pa) * 6), 7)

        pyxel.clip()

        cx, cy = WIDTH // 2, HEIGHT // 2
        cross = 10 if self.flash_timer else 7
        gap = 5 if self.flash_timer else 4
        pyxel.rect(cx - 1, cy - 1, 3, 3, cross)
        pyxel.line(cx - 12, cy, cx - gap, cy, cross)
        pyxel.line(cx + gap, cy, cx + 12, cy, cross)
        pyxel.line(cx, cy - 12, cx, cy - gap, cross)
        pyxel.line(cx, cy + gap, cx, cy + 12, cross)

        bob_x = math.sin(self.head_bob) * 4
        bob_y = abs(math.cos(self.head_bob)) * 3
        recoil = 18 if self.flash_timer > 6 else (8 if self.flash_timer > 0 else 0)
        
        gx = int(WIDTH // 2 + bob_x)
        gy = int(HEIGHT - 18 + bob_y + recoil)

        pyxel.rect(gx - 27, gy + 2, 18, 14, 3)
        pyxel.rect(gx + 8, gy + 2, 18, 14, 3)
        pyxel.line(gx - 26, gy + 3, gx - 10, gy + 3, 5)
        pyxel.line(gx + 10, gy + 3, gx + 25, gy + 3, 5)

        pyxel.rect(gx - 12, gy - 4, 24, 27, 0)
        pyxel.rectb(gx - 12, gy - 4, 24, 27, 5)
        pyxel.rect(gx - 8, gy - 18, 16, 15, 1)
        pyxel.rect(gx - 4, gy - 27, 8, 10, 5)
        pyxel.rect(gx - 2, gy - 33, 4, 8, 6)
        
        if self.flash_timer > 6:
            pyxel.rect(gx - 5, gy - 16, 10, 4, 0)
            
        pyxel.rect(gx - 8, gy + 3, 16, 5, 12 if not self.flash_timer else 7)
        pyxel.line(gx - 7, gy + 4, gx + 7, gy + 4, 7)
        pyxel.rect(gx - 5, gy + 9, 10, 7, 4)

        if self.flash_timer > 8:
            r = 6 + (self.flash_timer % 3) * 2
            my_y = gy - 36
            pyxel.circ(gx, my_y, r + 3, 0)
            pyxel.circ(gx, my_y, r, 9)
            pyxel.circ(gx, my_y, max(2, r - 2), 10)
            pyxel.circ(gx, my_y, max(1, r // 2), 7)
            for i in range(6):
                ang = (i / 6) * math.pi * 2 + t * 0.1
                ln = random.randint(5, 12)
                pyxel.line(gx, my_y,
                           gx + int(math.cos(ang) * ln),
                           my_y + int(math.sin(ang) * ln),
                           random.choice([10, 9]))

        if self.ai_mode:
            pyxel.rect(115, 5, 60, 16, 12)
            pyxel.rectb(115, 5, 60, 16, 7)
            self._jtext(121, 8, "自動操縦", 0)

App()

