import pygame
import sounddevice as sd
import numpy as np
import sys
import random
# -- Cấu hình cơ bản --
WIDTH, HEIGHT = 800, 600
BLOW_THRESHOLD = 0.03  # Ngưỡng âm thanh
FPS = 60
# -- Định nghĩa màu sắc --
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CAKE_COLOR = (255, 182, 193)
ICING_COLOR = (255, 105, 180)
PLATE_COLOR = (220, 220, 220)
CANDLE_COLOR = (173, 216, 230)
FLAME_COLORS = [(255, 140, 0), (255, 215, 0), (255, 69, 0)]
TEXT_COLOR = (255, 50, 50)
is_blown = False
def audio_callback(indata, frames, time, status):
    global is_blown
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > BLOW_THRESHOLD * 100:
        is_blown = True
def draw_cake(screen):
    plate_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 100, 400, 40)
    pygame.draw.ellipse(screen, PLATE_COLOR, plate_rect)
    cake_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 300, 120)
    pygame.draw.rect(screen, CAKE_COLOR, cake_rect, border_radius=10)
    icing_rect = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 - 10, 320, 40)
    pygame.draw.rect(screen, ICING_COLOR, icing_rect, border_radius=20)
    for i in range(5):
        drop_x = WIDTH//2 - 140 + i * 70
        pygame.draw.circle(screen, ICING_COLOR, (drop_x, HEIGHT//2 + 25), 15)
def draw_candles(screen, num_candles, is_blown):
    if num_candles <= 0: return
    start_x = WIDTH // 2 - 120
    end_x = WIDTH // 2 + 120
    if num_candles == 1:
        step = 0
        start_x = WIDTH // 2
    else:
        step = (end_x - start_x) / (num_candles - 1)
        
    for i in range(num_candles):
        x = start_x + i * step
        y = HEIGHT // 2 - 60
        candle_rect = pygame.Rect(x - 6, y, 12, 50)
        pygame.draw.rect(screen, CANDLE_COLOR, candle_rect, border_radius=3)
        pygame.draw.line(screen, BLACK, (x, y), (x, y - 5), 2)
        if not is_blown:
            flame_color = random.choice(FLAME_COLORS)
            offset_y = random.randint(-2, 2)
            pygame.draw.ellipse(screen, flame_color, (x - 8, y - 25 + offset_y, 16, 25))
def main():
    global is_blown
    
    print("\n" + "="*40)
    print("🎂 CHƯƠNG TRÌNH BÁNH SINH NHẬT BẰNG PYTHON 🎂")
    print("="*40)
    
    try:
        age_input = input(">> Nhập số tuổi của bạn (tương ứng số nến): ")
        age = int(age_input)
    except ValueError:
        print(">> Lỗi: Số tuổi phải là số! Mình sẽ để mặc định là 1 nến nhé.")
        age = 1
        
    name = input(">> Nhập tên của bạn (hoặc người nhận): ")
    
    print("\n" + "="*40)
    print(">> Đang mở cửa sổ bánh kem...")
    print(">> HƯỚNG DẪN: Hãy đưa miệng gần micro của máy tính và THỔI MẠNH để tắt nến nhé!")
    print("="*40 + "\n")
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Happy Birthday Cake")
    clock = pygame.time.Clock()
    
    try:
        font = pygame.font.SysFont("comicsansms", 64, bold=True)
    except:
        font = pygame.font.Font(None, 64)
    
    try:
        stream = sd.InputStream(channels=1, callback=audio_callback)
        stream.start()
    except Exception as e:
        print(f"Không thể mở Microphone: {e}")
        stream = None
    
    start_ticks = pygame.time.get_ticks()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        if stream is None and not is_blown:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds > 5:
                is_blown = True
                
        screen.fill(WHITE)
        draw_cake(screen)
        draw_candles(screen, age, is_blown)
        
        if is_blown:
            text_str = f"Happy Birthday {name}!"
            text_surface = font.render(text_str, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//4))
            screen.blit(text_surface, text_rect)
            
        pygame.display.flip()
        clock.tick(FPS)
        
    if stream is not None:
        stream.stop()
        stream.close()
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
