import pygame
import sys

# Function to initialize Pygame and the menu
def main_menu():
    pygame.init()
    
    # Screen settings
    SCREEN_WIDTH = 450
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Solver")
    
    # Load background for menu
    background = pygame.image.load("game_background.png")  # Background image for menu
    icon = pygame.image.load("game.png")  # Photo for the game
    pygame.display.set_icon(icon)  # Game icon
    pygame.mixer.music.load("background music.mp3")  # Background music file
    pygame.mixer.music.set_volume(0.3)  # Set the music volume
    pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely
    button_sound = pygame.mixer.Sound("correct.mp3")  # Sound effect for button clicks
    
    # Colors
    WHITE = (255, 255, 255)
    GREY = (30, 30, 30)
    PURPLE = (100, 0, 100)
    
    # Fonts
    font = pygame.font.Font(None, 40)
    largefont = pygame.font.Font(None, 75)
    
    # Define button dimensions
    button_width = 200
    button_height = 50
    
    # Create button rectangles dynamically centered
    start_button = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 200, button_width, button_height)
    menu_button = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 300, button_width, button_height)
    exit_button = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 400, button_width, button_height)

    # Main loop
    while True:
        screen.blit(background, (0, 0))  # Draw background image
        pygame.draw.rect(screen, PURPLE, start_button)
        pygame.draw.rect(screen, PURPLE, menu_button)
        pygame.draw.rect(screen, PURPLE, exit_button)

        # Render button texts, centering them within the buttons
        screen.blit(font.render("Start", True, WHITE), (start_button.x + (button_width - font.size("Start")[0]) // 2, start_button.y + (button_height - font.get_height()) // 2))
        screen.blit(font.render("Menu", True, WHITE), (menu_button.x + (button_width - font.size("Menu")[0]) // 2, menu_button.y + (button_height - font.get_height()) // 2))
        screen.blit(font.render("Exit", True, WHITE), (exit_button.x + (button_width - font.size("Exit")[0]) // 2, exit_button.y + (button_height - font.get_height()) // 2))

        # Center the "Main Menu" text
        menu_title = largefont.render("Maze Solver", True, WHITE)
        title_rect = menu_title.get_rect(center=(SCREEN_WIDTH // 2, 100))  # Center horizontally at 100 pixels from the top
        screen.blit(menu_title, title_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Play the button sound when a button is clicked
                if start_button.collidepoint(event.pos):
                    button_sound.play()  # Play sound effect for button press
                    import the_game  # Import the game module
                    the_game.run_game()  # Start the game using the function defined in main_game.py
                elif exit_button.collidepoint(event.pos):
                    button_sound.play()  # Play sound effect for button press
                    pygame.quit()
                    sys.exit()  # Exit the game

if __name__ == "__main__":
    main_menu()