import pygame, time, os, random, sys


# --- 初始化 ---
def play_game(screen:pygame.Surface):
    # pygame.init()
    WIDTH, HEIGHT = 900, 400
    # screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # pygame.display.set_caption("塔防簡單版")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    # --- 顏色 ---
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BROWN = (150, 75, 0)
    YELLOW = (255, 255, 0)

    # --- 遊戲參數 ---
    player_money = 0
    last_income_time = time.time()
    BASE_HP = 200


    # --- 圖片路徑 ---
    MELEE_IMAGE_PATH = "assets/bird/S__2269203_0.png"
    RANGE_IMAGE_PATH = "archer.png"
    ENEMY_IMAGE_PATH = "mushrooms/香菇1_20250429134900.png"

    def load_image(path, size=(30,30), color=BLUE):
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        else:
            surf = pygame.Surface(size)
            surf.fill(color)
            return surf

    melee_image = load_image(MELEE_IMAGE_PATH, (30,30), BLUE)
    range_image = load_image(RANGE_IMAGE_PATH, (30,30), GREEN)
    enemy_image = load_image(ENEMY_IMAGE_PATH, (30,30), RED)

    # --- 背景 ---
    background = pygame.image.load("misks/Void.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # --- 群組 ---
    allies = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    arrows = pygame.sprite.Group()
    towers = pygame.sprite.Group()
    hit_effects = pygame.sprite.Group()

    # ---------- 類別 ----------
    class HitEffect(pygame.sprite.Sprite):
        def __init__(self, pos, duration=0.1):
            super().__init__()
            self.pos = pos
            self.start_time = time.time()
            self.duration = duration
        def update(self):
            if time.time() - self.start_time > self.duration:
                self.kill()
        def draw(self, surface):
            pygame.draw.circle(surface, YELLOW, self.pos, 10)

    class Arrow(pygame.sprite.Sprite):
        def __init__(self, x, y, target, damage, speed=4):
            super().__init__()
            self.image = pygame.Surface((15,5))
            self.image.fill(BLUE)
            self.rect = self.image.get_rect(center=(x,y))
            self.target = target
            self.damage = damage
            self.speed = speed

        def update(self):
            if self.target and getattr(self.target,'hp',0) > 0:
                dx = self.target.rect.centerx - self.rect.centerx
                dy = self.target.rect.centery - self.rect.centery
                dist = max(1,(dx**2 + dy**2)**0.5)
                self.rect.x += self.speed * dx / dist
                self.rect.y += self.speed * dy / dist
                if self.rect.colliderect(self.target.rect):
                    self.target.hp -= self.damage if not isinstance(self.target, Tower) else 0
                    if isinstance(self.target, Tower):
                        self.target.take_damage(self.damage)
                    hit_effects.add(HitEffect(self.target.rect.center))
                    self.kill()
            else:
                self.kill()

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    class Unit(pygame.sprite.Sprite):
        def __init__(self, x, y, images_walk, images_attack, attack, attack_speed, hp, range_type, move_speed=1.0, attack_range=None):
            super().__init__()
            self.images_walk = images_walk      # 走路動畫圖片列表
            self.images_attack = images_attack  # 攻擊動畫圖片列表
            self.image_index = 0
            self.image = self.images_walk[self.image_index]
            self.image=pygame.transform.scale(self.image,(50,50))
            self.image=pygame.transform.flip(self.image,1,0)
            self.rect = self.image.get_rect(midleft=(x,y))
            self.attack = attack
            self.attack_speed = attack_speed
            self.hp = hp
            self.range_type = range_type
            self.last_attack_time = time.time()
            self.target = None
            self.speed = move_speed
            self.attack_range = attack_range if attack_range else (40 if range_type=="melee" else 150)
            self.last_frame_time = time.time()
            self.frame_interval = 0.2  # 每0.2秒換一張圖片
            self.state = "walk"  # "walk" 或 "attack”

        def update_animation(self):
            now = time.time()
            if now - self.last_frame_time > self.frame_interval:
                self.image_index = (self.image_index + 1) % (len(self.images_walk) if self.state=="walk" else len(self.images_attack))
                self.image = self.images_walk[self.image_index] if self.state=="walk" else self.images_attack[self.image_index]
                self.image=pygame.transform.scale(self.image,(50,50))  
                self.image=pygame.transform.flip(self.image,1,0)
                self.last_frame_time = now
            
        def update(self, enemies):
            now = time.time()
            # 找目標：先敵人，再塔
            if not self.target or getattr(self.target,'hp',0)<=0:
                self.target=None
                for e in enemies:
                    distance = e.rect.x - self.rect.x
                    if 0 < distance <= self.attack_range:
                        self.target = e
                        break
                if self.target is None:
                    for t in towers:
                        distance = t.rect.x - self.rect.x
                        if 0 < distance <= self.attack_range:
                            self.target = t
                            break

            # 攻擊
            if self.target and now - self.last_attack_time >= self.attack_speed:
                if self.range_type == "ranged":
                    arrows.add(Arrow(self.rect.centerx+10, self.rect.centery, self.target, self.attack))
                else:
                    if isinstance(self.target, Tower):
                        self.target.take_damage(self.attack)
                    else:
                        self.target.hp -= self.attack
                self.last_attack_time = now

            # 移動
            if self.target:
                distance = self.target.rect.x - self.rect.x
                if distance > self.attack_range:
                    self.rect.x += min(self.speed, distance - self.attack_range)
            else:
                self.rect.x += self.speed

            if self.hp <= 0:
                self.kill()
            # --- 動畫 ---
            if self.target:
                self.state = "attack"
            else:
                self.state = "walk"
            self.update_animation()
    


        def draw_health(self, surface):
            bar_width = self.rect.width
            bar_height = 4
            ratio = max(self.hp / 40, 0) if self.range_type=="melee" else max(self.hp / 25, 0)
            pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 6, bar_width, bar_height))
            pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 6, bar_width*ratio, bar_height))

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, hp=30, attack=3):
            super().__init__()
            self.image = enemy_image
            self.rect = self.image.get_rect(midright=(x,y))
            self.hp = hp
            self.attack = attack
            self.last_attack_time = time.time()

        def update(self, allies):
            now = time.time()
            target = None
            for a in allies:
                if self.rect.colliderect(a.rect):
                    target = a
                    break
            if target:
                if now - self.last_attack_time >= 1:
                    target.hp -= self.attack
                    self.last_attack_time = now
            else:
                self.rect.x -= 1
            if self.hp <=0:
                self.kill()

        def draw_health(self, surface):
            bar_width = self.rect.width
            bar_height = 4
            pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 6, bar_width, bar_height))
            pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 6, bar_width*max(self.hp/30,0), bar_height))

    class Tower(pygame.sprite.Sprite):
        def __init__(self,x,y,hp=100):
            super().__init__()
            self.image = pygame.image.load("misks/villiagehousestileset2.png").convert_alpha()
            self.image = pygame.transform.scale(self.image,(40,60))
            self.rect = self.image.get_rect(midbottom=(x,y))
            self.hp = hp

        def take_damage(self,dmg):
            self.hp -= dmg
            if self.hp <=0:
                self.kill()

        def draw_health(self,surface):
            bar_width, bar_height = self.rect.width, 6
            pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 8, bar_width, bar_height))
            pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 8, bar_width*max(self.hp/100,0), bar_height))

    # ---------- 初始敵人與塔 ----------
    # for i in range(3):
    #     enemies.add(Enemy(WIDTH - i*100, 300))
    towers.add(Tower(400, 300 + 20))
    towers.add(Tower(600, 300 + 20))
    towers.add(Tower(700, 300 + 20))


    # ---enemy spawning timer---
    enemy_spawn = pygame.event.custom_type()
    pygame.time.set_timer(enemy_spawn, 2000)

    # ---------- 主迴圈 ----------
    running = True
    while running:
        clock.tick(60)
        screen.blit(background, (0, 0))

        # 每秒加錢
        now = time.time()
        if now - last_income_time >= 1:
            player_money += 3
            last_income_time = now

        # 事件
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == enemy_spawn:   #enemy spawning
                for i in range(int(pygame.time.get_ticks()/30000)+1):
                    enemies.add(Enemy(WIDTH + (random.randint(1,5)*100), 300))
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if player_money >= 10:
                        walk_images = [pygame.image.load(f"birdani/kiwi_bird_{i}.png") for i in range(1,9)]
                        melee_attack_images = [pygame.image.load(f"birdani/kiwi_bird_attack_{i}.png") for i in range(1,5)]
                        allies.add(Unit(
                            x=50,
                            y=300,
                            images_walk=walk_images,
                            images_attack=melee_attack_images,
                            attack=5, 
                            attack_speed=0.8, 
                            hp=40,
                            range_type="melee", 
                            move_speed=1.0, 
                            attack_range=40
                        ))

                        player_money -=10
                elif event.key==pygame.K_m:
                    if player_money >= 15:
                        walk_images = [pygame.image.load(f"birdani/kiwi_bird_{i}.png") for i in range(1,9)]
                        ranged_attack_image = [pygame.image.load(f"birdani/kiwi_bird_jump_{i}.png") for i in range(1,8)]
                        allies.add(Unit(
                            x=50, 
                            y=300, 
                            images_walk= walk_images,
                            images_attack= ranged_attack_image,
                            attack=3, 
                            attack_speed=0.5, 
                            hp=25,
                            range_type="ranged", 
                            move_speed=1.2, 
                            attack_range=150))
                        player_money -=15

        # 更新
        allies.update(enemies)
        enemies.update(allies)
        arrows.update()
        hit_effects.update()

        # 檢查敵人攻擊基地
        for e in enemies:
            if e.rect.x <= 0:
                BASE_HP -= e.attack
                e.kill()

        # 遊戲結束判定
        if BASE_HP <=0:
            screen.fill((200,0,0))
            game_over_text = font.render("Lose", True, WHITE)
            screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        # 胜利判定
        if len(towers) == 0:
            screen.fill((0,200,0))
            win_text = font.render("Win", True, WHITE)
            screen.blit(win_text, (WIDTH//2 , HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        # 繪製
        towers.draw(screen)
        allies.draw(screen)
        enemies.draw(screen)
        for arrow in arrows:
            arrow.draw(screen)
        for effect in hit_effects:
            effect.draw(screen)

        # 顯示血條
        for ally in allies:
            ally.draw_health(screen)
        for e in enemies:
            e.draw_health(screen)
        for t in towers:
            t.draw_health(screen)

        # 顯示金錢和基地HP
        money_text = font.render(f"Money: {player_money}", True, YELLOW)
        screen.blit(money_text, (10,10))
        pygame.draw.rect(screen, RED, (WIDTH-220, 20, 200, 16))
        pygame.draw.rect(screen, GREEN, (WIDTH-220, 20, 200*(BASE_HP/200), 16))
        screen.blit(font.render("base", True, YELLOW), (WIDTH-270,20))

        pygame.display.flip()

    # pygame.quit()
    return