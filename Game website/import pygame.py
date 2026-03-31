import pygame
import time
import random 
pygame.font.init()

# Initialize pygame
pygame.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

# Load background
BG = pygame.image.load("dbget.im.jpg")

# Player constants
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5  # Falling star speed

# Fonts
FONT = pygame.font.SysFont("comicsans", 30)          # Elapsed time
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 60) # "GAME OVER"
RESTART_FONT = pygame.font.SysFont("comicsans", 40)   # Restart instruction

# Draw everything on the screen
def draw(player, elapsed_time, stars, hit):
    WIN.blit(BG, (0, 0))  # Draw background

    # Draw elapsed time
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", True, "white")
    WIN.blit(time_text, (10, 10))

    # Draw player if not hit
    if not hit:
        pygame.draw.rect(WIN, "red", player)

    # Draw stars
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    # Draw Game Over and restart instructions if hit
    if hit:
        over_text = GAME_OVER_FONT.render("GAME OVER", True, "yellow")
        WIN.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 100))

        restart_text = RESTART_FONT.render("Click Anywhere to Restart", True, "white")
        WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

    pygame.display.update()  # Update display

# Main game function
def main():
    run = True
    clock = pygame.time.Clock()  # Control frame rate

    while run:  # Outer loop allows restarting
        # Reset game variables
        player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
        stars = []
        hit = False
        star_add_increment = 2000
        star_count = 0
        start_time = time.time()
        elapsed_time = 0

        game_running = True
        while game_running:  # Inner loop runs actual game
            dt = clock.tick(60)
            star_count += dt
            elapsed_time = time.time() - start_time

            # Spawn new stars
            if star_count > star_add_increment:
                for _ in range(10):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)
                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_running = False
                elif hit and event.type == pygame.MOUSEBUTTONDOWN:
                    # Restart game on any mouse click
                    game_running = False

            # Player movement (only if not hit)
            keys = pygame.key.get_pressed()
            if not hit:
                if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                    player.x -= PLAYER_VEL
                if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
                    player.x += PLAYER_VEL

            # Update stars and check collisions
            for star in stars[:]:
                star.y += STAR_VEL
                if star.y > HEIGHT:
                    stars.remove(star)
                elif star.y + star.height >= player.y and star.colliderect(player):
                    hit = True
                    break

            # Draw everything
            draw(player, elapsed_time, stars, hit)

    pygame.quit()

if __name__ == "__main__":
    main()


