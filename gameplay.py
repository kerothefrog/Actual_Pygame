import pygame, time, os, random, sys, math
import g_var
from button import Interactive_button

def spawning_timer(enemy_group:pygame.sprite.Group, level_state:str, time):
    if level_state == 'gameplay1':
        temp = int(time/10 + 1)
        if len(enemy_group)>10: return 0
        if temp > 3:
            return 3
        else:
            return temp
    elif level_state == 'gameplay2':
        temp = int(time/10 + 1)
        if len(enemy_group)>15: return 0
        if temp > 5:
            return 5
        else:
            return temp
    elif level_state == 'gameplay3':
        temp = int(math.log10(time)+3)
        if len(enemy_group)>25 :return 0
        if temp > 7:
            return 7 
        else:
            return temp
    elif level_state == 'gameplay4':
        if time < 12.4:
            return 0
        else:
            return int(time/5)
    elif level_state == 'gameplay5':
        return int(math.pow(time/5,1.1))
    
def load_image(path, size=(30,30), color=(0,0,255)):
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        else:
            surf = pygame.Surface(size)
            surf.fill(color)


# --- 初始化 ---
def play_game(screen:pygame.Surface, level_state:str):
    # pygame.init()
    WIDTH, HEIGHT = 900, 400
    # screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # pygame.display.set_caption("塔防簡單版")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    font_bigger = pygame.font.SysFont(None,50)
    game_started_time = time.time()

    # --- 顏色 ---
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BROWN = (150, 75, 0)
    YELLOW = (255, 255, 0)

    # --- 遊戲參數 ---
    last_income_time = time.time()
    BASE_HP = 100
    g_var.paused = False
    g_var.player_money = 0
    g_var.score = 0


    # --- 圖片路徑 ---
    # MELEE_IMAGE_PATH = "birdani/kiwi_bird_1.png"
    # RANGE_IMAGE_PATH = "birdani/kiwi_bird_attack_1.png"
    # ENEMY_IMAGE_PATH = "mushrooms/香菇1_20250429134900.png"

    

    # melee_image = load_image(MELEE_IMAGE_PATH, (30,30), BLUE)
    # range_image = load_image(RANGE_IMAGE_PATH, (30,30), GREEN)
    # enemy_image = load_image(ENEMY_IMAGE_PATH, (30,30), RED)

    # --- 背景 ---
    background = pygame.image.load("misks/background.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    pause_menu = pygame.image.load("UI/paused_menu.png").convert_alpha()
    pause_menu = pygame.transform.scale(pause_menu, (560, 340))

    pause_button = pygame.sprite.GroupSingle(Interactive_button(
        location = (150,50),
        font=font,
        button_surf=load_image("UI/pause_button.png", size=(50,50)),
        hover_button_surf=load_image("UI/pause_button.png", size=(50,50)),
        size=(50,50)
    ))
    pause_menu_back_button = pygame.sprite.GroupSingle(Interactive_button(
        location=(620,120),
        font=font,
        button_surf=load_image("UI/backb.png", size=(75,75)),
        hover_button_surf=load_image("UI/backb.png", size=(75,75)),
        size=(75,75)
    ))
    pause_menu_quit_button = pygame.sprite.GroupSingle(Interactive_button(
        location=(300,230),
        font=font,
        button_surf=load_image("UI/quit_button.png", size=(150,75)),
        hover_button_surf=load_image("UI/quit_button.png", size=(150,75)),
        size=(150,75)
    ))


    # --- 群組 ---
    allies = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    arrows = pygame.sprite.Group()
    towers = pygame.sprite.Group()
    hit_effects = pygame.sprite.Group()
    character_select_boxes = pygame.sprite.Group()

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
            self.image = load_image("birdani/melee_kiwi.png",(20,20))
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
        def __init__(self, x, y, images_walk, images_attack, attack, attack_speed, hp, range_type, move_speed=1.0, attack_range=None, frame_interval=0.2):
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
            self.full_hp = hp
            self.range_type = range_type
            self.last_attack_time = time.time()
            self.target = None
            self.speed = move_speed
            self.attack_range = attack_range if attack_range else (40 if range_type=="melee" else 150)
            self.last_frame_time = time.time()
            self.frame_interval = frame_interval  # 每0.2秒換一張圖片
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
            ratio = max(self.hp / self.full_hp, 0)
            pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 6, bar_width, bar_height))
            pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 6, bar_width*ratio, bar_height))

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y,images_walk, images_attack, score_when_killed, money_when_killed, hp=30, attack=3, frame_interval=0.2):
            super().__init__()
            self.images_walk = images_walk      # 走路動畫圖片列表
            self.images_attack = images_attack  # 攻擊動畫圖片列表
            self.image_index = 0
            self.image = self.images_walk[self.image_index]
            self.image=pygame.transform.scale(self.image,(50,50))
            self.image=pygame.transform.flip(self.image,1,0)
            self.rect = self.image.get_rect(midright=(x,y))
            self.hp = hp

            self.hp_full=hp
            self.attack = attack
            self.last_attack_time = time.time()
            self.last_frame_time = time.time()
            self.frame_interval = frame_interval  # 每0.2秒換一張圖片//
            self.state = "walk"  # "walk" 或 "attack”
            self.score_when_killed = score_when_killed
            self.money_when_killed = money_when_killed
            

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
                g_var.score += self.score_when_killed
                g_var.player_money += self.money_when_killed
                self.kill()

            if target:
                self.state = "attack"
            else:
                self.state = "walk"
            self.update_animation()
    

        def draw_health(self, surface):
            bar_width = self.rect.width
            bar_height = 4
            pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 6, bar_width, bar_height))
            pygame.draw.rect(surface, "#8EFF8EB2", (self.rect.x, self.rect.y - 6, bar_width*max(self.hp/self.hp_full,0), bar_height))

        def update_animation(self):
            now = time.time()
            if now - self.last_frame_time > self.frame_interval:
                self.image_index = (self.image_index + 1) % (len(self.images_walk) if self.state=="walk" else len(self.images_attack))
                self.image = self.images_walk[self.image_index] if self.state=="walk" else self.images_attack[self.image_index]
                self.image=pygame.transform.scale(self.image,(50,50))  
                self.image=pygame.transform.flip(self.image,1,0)
                self.last_frame_time = now




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
                g_var.score += 200
                self.kill()

        def draw_health(self,surface):
            bar_width, bar_height = self.rect.width, 6
            pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 8, bar_width, bar_height))
            pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 8, bar_width*max(self.hp/100,0), bar_height))

    class Character_select_box(pygame.sprite.Sprite):
        def __init__(self, default_image:str, hover_image:str, center_location:tuple, size:tuple, spawning_event:int):
            super().__init__()
            self.location = center_location
            self.size = size
            self.default_image = pygame.image.load(default_image).convert_alpha()
            self.default_image = pygame.transform.scale(self.default_image, self.size)
            self.hover_image = pygame.image.load(hover_image).convert_alpha()
            self.hover_image = pygame.transform.scale(self.hover_image, self.size)

            self.spawning_event = pygame.event.Event(spawning_event)
            

            self.image = None
            self.rect = None

            self.set_image_and_rect()

        def set_image_and_rect(self):
            self.image = self.default_image
            self.rect = self.image.get_rect(center=self.location)

        def is_hovered(self):
            return pygame.Rect.collidepoint(self.rect, pygame.mouse.get_pos())
        
        def is_clicked(self):
            return pygame.Rect.collidepoint(self.rect, pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
        
        def update(self):
            if self.is_hovered():
                self.image = self.hover_image
            else:
                self.image = self.default_image


    # ---------- 初始敵人與塔 ----------
    # for i in range(3):
    #     enemies.add(Enemy(WIDTH - i*100, 300))
    towers.add(Tower(400, 300 + 20))
    towers.add(Tower(600, 300 + 20))
    towers.add(Tower(700, 300 + 20))

    # ---character select boxes---
    warrior_spawn = pygame.event.custom_type()
    archer_spawn = pygame.event.custom_type()
    kiwi_boss_spawn = pygame.event.custom_type()

    character_select_boxes.add(Character_select_box(
        default_image="UI/archer_select_box_1.png",
        hover_image="UI/archer_select_box_2.png",
        center_location=(400,80),
        size=(80,80),
        spawning_event=archer_spawn
    ))
    character_select_boxes.add(Character_select_box(
        default_image="UI/warrior_select_box_1.png",
        hover_image="UI/warrior_select_box_2.png",
        center_location=(500,80),
        size=(80,80),
        spawning_event=warrior_spawn
    ))
    character_select_boxes.add(Character_select_box(
        default_image="UI/kiwi_boss_select_1.png",
        hover_image="UI/kiwi_boss_select_2.png",
        center_location=(600,80),
        size=(80,80),
        spawning_event=kiwi_boss_spawn
    ))

    # ---enemy spawning timer---
    enemy_spawn = pygame.event.custom_type()
    pygame.time.set_timer(enemy_spawn, 2000)

    # ---------- 主迴圈 ----------
    running = True
    while running:
        clock.tick(60)
        mouse_button_down_event = False

        current_tick_screen = screen.copy()

        if g_var.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if pause_menu_back_button.sprite.is_pressed():
                g_var.paused = False
            if pause_menu_quit_button.sprite.is_pressed():
                return
            
            screen.blit(current_tick_screen,(0,0))
            screen.blit(pause_menu,(200,50))
            pause_menu_back_button.draw(screen)
            pause_menu_back_button.update(screen)
            pause_menu_quit_button.draw(screen)
            pause_menu_quit_button.update(screen)

        else:
            # 每秒加錢
            now = time.time()
            if now - last_income_time >= 1:
                g_var.player_money += 3
                last_income_time = now

            # 事件
            for event in pygame.event.get():

                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == enemy_spawn:   #enemy spawning
                    for i in range(spawning_timer(enemy_group=enemies, level_state=level_state, time=now-game_started_time)):
                        temp = random.randint(0,3)
                        if temp==0:

                            enemies.add(Enemy(
                                x=WIDTH + (random.randint(50,300)), 
                                y=300,
                                images_walk = [pygame.image.load(f"mushrooms/mushroom_walk_{i}.png") for i in range(1,4)],
                                images_attack = [pygame.image.load(f"mushrooms/mushroom_walk_{i}.png") for i in range(1,4)],
                                hp=10,
                                score_when_killed=20,
                                money_when_killed=1
                            ))

                        elif temp ==1:

                            enemies.add(Enemy(
                                x=WIDTH + (random.randint(50,300)), 
                                y=300,
                                images_walk = [pygame.image.load(f"mushrooms/mushroom2_walk_{i}.png") for i in range(1,4)],
                                images_attack = [pygame.image.load(f"mushrooms/mushroom2_walk_{i}.png") for i in range(1,4)],
                                hp=25,
                                score_when_killed=50,
                                money_when_killed=3
                            ))

                        elif temp ==2:

                            enemies.add(Enemy(
                                x=WIDTH + (random.randint(50,300)), 
                                y=300,
                                images_walk = [pygame.image.load(f"mushrooms/mushroom3_walk_{i}.png") for i in range(1,8)],
                                images_attack = [pygame.image.load(f"mushrooms/mushroom3_walk_{i}.png") for i in range(1,8)],
                                hp=40,
                                score_when_killed=80,
                                money_when_killed=3
                            ))

                        else:

                            enemies.add(Enemy(
                                x=WIDTH + (random.randint(50,300)), 
                                y=300,
                                images_walk = [pygame.image.load(f"mushrooms/mushroom4_walk_{i}.png") for i in range(1,7)],
                                images_attack = [pygame.image.load(f"mushrooms/mushroom4_walk_{i}.png") for i in range(1,7)],
                                hp=15,
                                score_when_killed=30,
                                money_when_killed=1
                            ))

                if event.type==pygame.KEYDOWN:
                    pass

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_button_down_event = True

                #spawning_warriors
                if event.type == warrior_spawn: 
                    if g_var.player_money >= 10:
                        walk_images = [pygame.image.load(f"birdani/kiwi_bird_{i}.png") for i in range(1,9)]
                        attack_images = [pygame.image.load(f"birdani/kiwi_bird_jump_{i}.png") for i in range(1,8)]
                        allies.add(Unit(
                            x=50,
                            y=300,
                            images_walk=walk_images,
                            images_attack=attack_images,
                            attack=5, 
                            attack_speed=0.8, 
                            hp=40,
                            range_type="melee", 
                            move_speed=2.0, 
                            attack_range=40
                        ))
                        g_var.player_money -=10

                if event.type == archer_spawn:
                    if g_var.player_money >= 15:
                        walk_images = [pygame.image.load(f"birdani/kiwi_bird_{i}.png") for i in range(1,9)]
                        attack_images = [pygame.image.load(f"birdani/kiwi_bird_attack_{i}.png") for i in range(1,5)]
                        allies.add(Unit(
                            x=50, 
                            y=300, 
                            images_walk= walk_images,
                            images_attack= attack_images,
                            attack=8, 
                            attack_speed=0.5, 
                            hp=25,
                            range_type="ranged", 
                            move_speed=1, 
                            attack_range=150))
                        g_var.player_money -=15

                if event.type == kiwi_boss_spawn:
                    if g_var.player_money >= 40:
                        walk_images = [pygame.image.load(f"birdani/kiwi_bird_{i}.png") for i in range(1,9)]
                        attack_images = [pygame.image.load(f"birdani/kiwi_boss_{i}.png") for i in range(1,11)]
                        allies.add(Unit(
                            x=50, 
                            y=300, 
                            images_walk= walk_images,
                            images_attack= attack_images,
                            attack=30, 
                            attack_speed=0.5, 
                            hp=150,
                            range_type="melee", 
                            move_speed=1, 
                            attack_range=40,
                            frame_interval=0.1))
                        g_var.player_money -=40

            # 更新
            allies.update(enemies)
            enemies.update(allies)
            arrows.update()
            hit_effects.update()
            character_select_boxes.update()
            for character in character_select_boxes:
                if character.is_clicked() and mouse_button_down_event: pygame.event.post(character.spawning_event)

            # 檢查敵人攻擊基地
            for e in enemies:
                if e.rect.x <= 0:
                    BASE_HP -= e.attack
                    e.kill()

            # 遊戲結束判定
            if BASE_HP <=0:
                screen.fill((200,0,0))
                game_over_text = font_bigger.render("Lose", True, WHITE)
                game_over_score_text = font_bigger.render(f"Your score: {g_var.score}", True, WHITE)
                screen.blit(game_over_text, (150,100))
                screen.blit(game_over_score_text,(150,150))
                pygame.display.flip()
                pygame.time.wait(1000)
                running = False

            # 胜利判定
            if len(towers) == 0:
                screen.fill((0,200,0))
                win_text = font_bigger.render("Win", True, WHITE)
                game_over_score_text = font_bigger.render(f"Your score: {g_var.score}", True, WHITE)
                screen.blit(win_text, (150,100))
                screen.blit(game_over_score_text,(150,150))
                pygame.display.flip()
                pygame.time.wait(1000)
                running = False

            # 繪製
            screen.blit(background, (0, 0))
            towers.draw(screen)
            allies.draw(screen)
            enemies.draw(screen)
            character_select_boxes.draw(screen)
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

            # 顯示金錢
            money_text = font.render(f"Money: {g_var.player_money}", True, YELLOW)
            screen.blit(money_text, (10,10))

            # draw base hp box
            pygame.draw.rect(screen, RED, (WIDTH-220, 20, 200, 16))
            pygame.draw.rect(screen, GREEN, (WIDTH-220, 20, 200*(BASE_HP/100), 16))
            screen.blit(font.render("base", True, YELLOW), (WIDTH-270,20))

            # draw score text
            score_text = font.render(f"Score: {g_var.score}", True, YELLOW)
            screen.blit(score_text, (10,30))

            #draw pause button
            pause_button.draw(screen)
            pause_button.update(screen)

            #detect if paused
            if pause_button.sprite.is_pressed():
                g_var.paused = True

        pygame.display.flip()

    return