import pygame
import sys
import random
import time
from pygame.locals import *
import platform

# ゲームの初期化
pygame.init()
pygame.mixer.init()  # サウンド用

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ゾンビから逃げろ！")

# 時間管理
clock = pygame.time.Clock()
FPS = 60

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 日本語フォントの設定
japanese_font_name = None

# macOSの場合はヒラギノフォントを優先
if platform.system() == 'Darwin':
    possible_fonts = ['ヒラギノ角コシックw8', 'Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'ヒラギノ角ゴシック']
    for font in possible_fonts:
        if font in pygame.font.get_fonts():
            japanese_font_name = font
            print(f"日本語フォント候補: {font}")
            break

# Windowsの場合はMSゴシックを優先
elif platform.system() == 'Windows':
    possible_fonts = ['MS Gothic', 'Yu Gothic', 'Meiryo']
    for font in possible_fonts:
        if font in pygame.font.get_fonts():
            japanese_font_name = font
            break

# 日本語フォントが見つからない場合はシステムデフォルトを使用
if not japanese_font_name:
    japanese_font_name = pygame.font.get_default_font()

# ゲーム変数
score = 0
game_over = False
start_time = 0
game_started = False  # ゲーム開始フラグ

# アイテムの種類
ITEM_SPEED = 0
ITEM_INVINCIBLE = 1
ITEM_FREEZE = 2

# プレイヤークラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # プレイヤー画像の読み込み
        self.original_image = pygame.image.load('assets/images/Player.png').convert_alpha()
        # 画像サイズの調整（元のサイズが1024x1024と大きいため）
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.base_speed = 5  # 基本速度
        # マスク衝突判定用のマスクを作成
        self.mask = pygame.mask.from_surface(self.image)
        # パワーアップ状態
        self.is_speed_up = False
        self.is_invincible = False
        self.power_up_timer = 0
        self.power_up_duration = 5000  # 5秒間

    def update(self):
        # キー入力による移動
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        
        # パワーアップの効果時間管理
        now = pygame.time.get_ticks()
        if (self.is_speed_up or self.is_invincible) and now - self.power_up_timer > self.power_up_duration:
            self.reset_power_ups()
    
    def apply_power_up(self, power_up_type):
        self.power_up_timer = pygame.time.get_ticks()
        
        if power_up_type == ITEM_SPEED:
            self.is_speed_up = True
            self.speed = self.base_speed * 1.5
            print("スピードアップ！")
        elif power_up_type == ITEM_INVINCIBLE:
            self.is_invincible = True
            # 無敵状態の視覚的効果（半透明）
            self.image.set_alpha(150)
            print("無敵状態！")
    
    def reset_power_ups(self):
        self.is_speed_up = False
        self.is_invincible = False
        self.speed = self.base_speed
        self.image.set_alpha(255)  # 透明度をリセット
        print("パワーアップ効果が切れました")

# アイテムクラス
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        
        # アイテムタイプに応じた色を設定
        if item_type == ITEM_SPEED:
            color = (0, 255, 0)  # 緑：スピードアップ
        elif item_type == ITEM_INVINCIBLE:
            color = (255, 255, 0)  # 黄：無敵
        elif item_type == ITEM_FREEZE:
            color = (0, 255, 255)  # 水色：ゾンビ凍結
        
        # アイテム画像を作成（後で実際の画像に置き換えることができます）
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (10, 10), 10)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

# 障害物クラス
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 50, 50))  # 茶色の壁
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

# ゾンビクラス
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # ゾンビ画像の読み込み
        self.image_left = pygame.image.load('assets/images/Zombie-left.png').convert_alpha()
        # 画像サイズの調整（元のサイズが1024x1024と大きいため）
        self.image_left = pygame.transform.scale(self.image_left, (50, 50))
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_left
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # ゾンビの初期速度を遅くする
        self.speed = 1.0
        # マスク衝突判定用のマスクを作成
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, player, game_time):
        # プレイヤーを追いかける
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
            self.image = self.image_right
            # 画像が変わったらマスクも更新
            self.mask = pygame.mask.from_surface(self.image)
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed
            self.image = self.image_left
            # 画像が変わったらマスクも更新
            self.mask = pygame.mask.from_surface(self.image)
        
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed

# スプライトグループの作成
all_sprites = pygame.sprite.Group()
zombies = pygame.sprite.Group()
items = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# 背景画像の読み込み
background = pygame.image.load('assets/images/ground.png').convert()

# 障害物の生成
def create_obstacles():
    # 画面の四隅に障害物を配置
    obstacle_size = 100
    
    # 左上の障害物
    obstacle1 = Obstacle(50, 50, obstacle_size, obstacle_size)
    obstacles.add(obstacle1)
    all_sprites.add(obstacle1)
    
    # 右上の障害物
    obstacle2 = Obstacle(SCREEN_WIDTH - 150, 50, obstacle_size, obstacle_size)
    obstacles.add(obstacle2)
    all_sprites.add(obstacle2)
    
    # 左下の障害物
    obstacle3 = Obstacle(50, SCREEN_HEIGHT - 150, obstacle_size, obstacle_size)
    obstacles.add(obstacle3)
    all_sprites.add(obstacle3)
    
    # 右下の障害物
    obstacle4 = Obstacle(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150, obstacle_size, obstacle_size)
    obstacles.add(obstacle4)
    all_sprites.add(obstacle4)
    
    # 中央の障害物
    obstacle5 = Obstacle(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, obstacle_size, obstacle_size)
    obstacles.add(obstacle5)
    all_sprites.add(obstacle5)

# アイテムの生成
def spawn_item():
    item_type = random.randint(0, 2)  # ランダムなアイテムタイプ
    
    # 画面内のランダムな位置（障害物と重ならないように）
    while True:
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        
        # 仮の矩形を作成して衝突チェック
        temp_rect = pygame.Rect(x, y, 20, 20)
        collision = False
        
        # 障害物との衝突チェック
        for obstacle in obstacles:
            if temp_rect.colliderect(obstacle.rect):
                collision = True
                break
        
        if not collision:
            break
    
    item = Item(x, y, item_type)
    items.add(item)
    all_sprites.add(item)

# ゾンビの生成
def spawn_zombie():
    # 画面外からゾンビを生成
    side = random.randint(1, 4)
    if side == 1:  # 上
        x = random.randint(0, SCREEN_WIDTH)
        y = -50
    elif side == 2:  # 右
        x = SCREEN_WIDTH + 50
        y = random.randint(0, SCREEN_HEIGHT)
    elif side == 3:  # 下
        x = random.randint(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT + 50
    else:  # 左
        x = -50
        y = random.randint(0, SCREEN_HEIGHT)
    
    zombie = Zombie(x, y)
    zombies.add(zombie)
    all_sprites.add(zombie)

# テキスト描画関数
def draw_text(text, size, x, y, color=(255, 255, 255)):
    try:
        # 日本語フォントを使用
        font = pygame.font.SysFont(japanese_font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)
    except Exception as e:
        # フォントエラーの場合は英語で表示
        print(f"フォントエラー: {e}")
        font = pygame.font.SysFont('Arial', size)
        # 日本語が表示できない場合は英語に変換
        if any(ord(c) > 127 for c in text):
            text = "Zombie Game"
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# スタート画面の表示
def show_start_screen():
    # 背景を敷き詰める
    for y in range(0, SCREEN_HEIGHT, background.get_height()):
        for x in range(0, SCREEN_WIDTH, background.get_width()):
            screen.blit(background, (x, y))
    
    # タイトル
    draw_text("ゾンビから逃げろ！", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    
    # ゲーム説明
    draw_text("矢印キーで移動", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("アイテムを取ってゾンビから逃げよう", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
    draw_text("緑：スピードアップ  黄：無敵  水色：ゾンビ凍結", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
    
    # 開始方法
    draw_text("Enterキーを押してスタート", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3/4)
    draw_text("ESCキーで終了", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3/4 + 50)
    
    # 画面更新
    pygame.display.flip()
    
    # キー入力待機
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    waiting = False
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# ゲームオーバー画面の表示
def show_game_over_screen():
    screen.fill(BLACK)
    draw_text("ゲームオーバー！", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text(f"スコア: {score}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Rキーでリスタート", 22, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3/4)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    waiting = False

# ゲームのメインループ
def main():
    global score, game_over, start_time, game_started
    
    # スタート画面表示（ゲーム開始前）
    if not game_started:
        show_start_screen()
        game_started = True
    
    # ゲーム変数の初期化
    score = 0
    game_over = False
    start_time = time.time()
    
    # スプライトグループのリセット
    all_sprites.empty()
    zombies.empty()
    items.empty()
    obstacles.empty()
    
    # プレイヤーの作成
    player = Player()
    all_sprites.add(player)
    
    # 障害物の生成
    create_obstacles()
    
    # 最初のゾンビを生成
    spawn_zombie()
    
    # ゾンビ生成タイマー
    zombie_spawn_time = 3000  # 3秒ごとに生成
    last_spawn = pygame.time.get_ticks()
    
    # ゾンビ速度増加タイマー
    zombie_speed_increase_time = 30000  # 30秒ごとに速度増加
    last_speed_increase = pygame.time.get_ticks()
    zombie_speed_increase = 0.1  # 増加量
    max_zombie_speed = 3.0  # 最大速度
    
    # アイテム生成タイマー
    item_spawn_time = 10000  # 10秒ごとに生成
    last_item_spawn = pygame.time.get_ticks()
    
    # ハイスコア
    high_score = 0
    
    # メインゲームループ
    running = True
    while running:
        clock.tick(FPS)
        
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
        # ゲームオーバーでなければ更新
        if not game_over:
            # スコア更新（生存時間）
            current_time = time.time()
            score = int(current_time - start_time)
            game_time = score  # ゲーム時間をスコアとして使用
            
            # ハイスコア更新
            high_score = max(high_score, score)
            
            # ゾンビ生成タイマー
            now = pygame.time.get_ticks()
            if now - last_spawn > zombie_spawn_time:
                spawn_zombie()
                last_spawn = now
                # ゲームが進むにつれてゾンビの生成間隔を短くする
                zombie_spawn_time = max(1000, zombie_spawn_time - 100)
            
            # ゾンビ速度増加タイマー
            if now - last_speed_increase > zombie_speed_increase_time:
                for zombie in zombies:
                    zombie.speed = min(max_zombie_speed, zombie.speed + zombie_speed_increase)
                last_speed_increase = now
                print(f"ゾンビの速度が上昇: {zombies.sprites()[0].speed if zombies else 0}")
            
            # アイテム生成タイマー
            if now - last_item_spawn > item_spawn_time:
                spawn_item()
                last_item_spawn = now
                print("アイテムが出現しました")
            
            # プレイヤーの更新
            player.update()
            
            # ゾンビの更新
            for zombie in zombies:
                zombie.update(player, game_time)
                
                # 障害物との衝突チェック
                zombie_hits_obstacle = pygame.sprite.spritecollide(zombie, obstacles, False, pygame.sprite.collide_mask)
                if zombie_hits_obstacle:
                    # 障害物に当たったら少し押し戻す
                    if zombie.rect.x < zombie_hits_obstacle[0].rect.x:
                        zombie.rect.x -= zombie.speed
                    elif zombie.rect.x > zombie_hits_obstacle[0].rect.x:
                        zombie.rect.x += zombie.speed
                    if zombie.rect.y < zombie_hits_obstacle[0].rect.y:
                        zombie.rect.y -= zombie.speed
                    elif zombie.rect.y > zombie_hits_obstacle[0].rect.y:
                        zombie.rect.y += zombie.speed
            
            # プレイヤーと障害物の衝突チェック
            player_hits_obstacle = pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_mask)
            if player_hits_obstacle:
                # 障害物に当たったら少し押し戻す
                if player.rect.x < player_hits_obstacle[0].rect.x:
                    player.rect.x -= player.speed
                elif player.rect.x > player_hits_obstacle[0].rect.x:
                    player.rect.x += player.speed
                if player.rect.y < player_hits_obstacle[0].rect.y:
                    player.rect.y -= player.speed
                elif player.rect.y > player_hits_obstacle[0].rect.y:
                    player.rect.y += player.speed
            
            # プレイヤーとアイテムの衝突チェック
            item_hits = pygame.sprite.spritecollide(player, items, True, pygame.sprite.collide_mask)
            for item in item_hits:
                if item.item_type == ITEM_FREEZE:
                    # すべてのゾンビを一時的に凍結
                    for zombie in zombies:
                        zombie.speed = 0
                    # 3秒後に元の速度に戻すタイマーをセット
                    pygame.time.set_timer(pygame.USEREVENT, 3000)
                    print("ゾンビが凍結しました！")
                else:
                    # その他のパワーアップをプレイヤーに適用
                    player.apply_power_up(item.item_type)
            
            # 衝突判定（マスク衝突判定を使用）
            if not player.is_invincible:  # 無敵状態でなければ衝突判定
                for zombie in zombies:
                    if pygame.sprite.collide_mask(player, zombie):
                        game_over = True
                        break
        
        # 描画
        # 背景を敷き詰める
        for y in range(0, SCREEN_HEIGHT, background.get_height()):
            for x in range(0, SCREEN_WIDTH, background.get_width()):
                screen.blit(background, (x, y))
        
        # スプライトの描画
        all_sprites.draw(screen)
        
        # スコア表示
        draw_text(f"スコア: {score}", 36, SCREEN_WIDTH // 2, 10)
        draw_text(f"ハイスコア: {high_score}", 24, SCREEN_WIDTH // 2, 50)
        
        # パワーアップ状態の表示
        if player.is_speed_up:
            draw_text("スピードアップ中！", 24, SCREEN_WIDTH // 2, 80)
        if player.is_invincible:
            draw_text("無敵状態！", 24, SCREEN_WIDTH // 2, 110)
        
        # 画面更新
        pygame.display.flip()
        
        # ゲームオーバー処理
        if game_over:
            show_game_over_screen()
            main()  # リスタート
    
    pygame.quit()

# メイン処理
if __name__ == "__main__":
    # Pygameの初期化
    pygame.init()
    pygame.mixer.init()  # サウンド用
    
    # 画面設定
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ゾンビから逃げろ！")
    
    # 時間管理
    clock = pygame.time.Clock()
    FPS = 60
    
    # 日本語フォントの設定
    japanese_font_name = None
    
    # macOSの場合はヒラギノフォントを優先
    if platform.system() == 'Darwin':
        possible_fonts = ['ヒラギノ角コシックw8', 'Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'ヒラギノ角ゴシック']
        for font in possible_fonts:
            if font in pygame.font.get_fonts():
                japanese_font_name = font
                print(f"日本語フォント候補: {font}")
                break
    
    # Windowsの場合はMSゴシックを優先
    elif platform.system() == 'Windows':
        possible_fonts = ['MS Gothic', 'Yu Gothic', 'Meiryo']
        for font in possible_fonts:
            if font in pygame.font.get_fonts():
                japanese_font_name = font
                break
    
    # 日本語フォントが見つからない場合はシステムデフォルトを使用
    if not japanese_font_name:
        japanese_font_name = pygame.font.get_default_font()
    
    # スプライトグループの作成
    all_sprites = pygame.sprite.Group()
    zombies = pygame.sprite.Group()
    items = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    
    # 背景画像の読み込み
    background = pygame.image.load('assets/images/ground.png').convert()
    
    # ゲーム開始フラグ
    game_started = False
    
    # ゲーム開始
    main()
    
    # 終了処理
    pygame.quit()