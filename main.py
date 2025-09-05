# main.py
import pygame
import cv2
import time
from hand_tracker import HandTracker
from game_logic import RPSGame

# --- Constants and Initialization ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 920
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Modular Rock Paper Scissors")
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 48)

def draw_ui(game, frame):
    """Handles all the drawing onto the Pygame screen."""
    screen.fill(BLACK)
    
    # Convert and draw the OpenCV frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (640, 480))
    pygame_frame = pygame.surfarray.make_surface(frame_resized.swapaxes(0, 1))
    screen.blit(pygame_frame, (SCREEN_WIDTH // 2 - 320, 50))

    # Draw scores
    player_score_text = small_font.render(f"Player: {game.player_score}", True, WHITE)
    screen.blit(player_score_text, (50, 50))
    comp_score_text = small_font.render(f"Computer: {game.computer_score}", True, WHITE)
    screen.blit(comp_score_text, (SCREEN_WIDTH - 250, 50))

    # Draw game state text
    if game.winner: # Result phase
        player_text = small_font.render(f"You: {game.player_choice}", True, BLUE)
        screen.blit(player_text, (100, SCREEN_HEIGHT - 150))
        comp_text = small_font.render(f"Comp: {game.computer_choice}", True, RED)
        screen.blit(comp_text, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 150))

        winner_color = GREEN if "You" in game.winner else RED if "Computer" in game.winner else WHITE
        winner_text = font.render(game.winner, True, winner_color)
        text_rect = winner_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 75))
        screen.blit(winner_text, text_rect)
    else: # Play phase
        prompt_text = font.render("Show your hand!", True, GRAY)
        text_rect = prompt_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 75))
        screen.blit(prompt_text, text_rect)
        if game.player_choice:
            detected_text = small_font.render(f"Detected: {game.player_choice}", True, GREEN)
            text_rect = detected_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 150))
            screen.blit(detected_text, text_rect)

    pygame.display.flip()

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    game = RPSGame()

    # Game state and timing variables
    game_state = "PLAY" # PLAY, RESULT
    last_gesture_time = time.time()
    gesture_lock_delay = 1.0
    result_display_time = 2.0
    last_result_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        success, frame = cap.read()
        if not success:
            continue
        
        frame = cv2.flip(frame, 1) # Mirror the frame
        
        # We find the gesture regardless of the state to show live tracking
        current_gesture, processed_frame = tracker.find_gesture(frame)

        if game_state == "PLAY":
            if current_gesture:
                game.player_choice = current_gesture
                if time.time() - last_gesture_time > gesture_lock_delay:
                    game.make_computer_choice()
                    game.determine_winner()
                    game_state = "RESULT"
                    last_result_time = time.time()
            else:
                # If no gesture is detected, reset the timer and choice
                last_gesture_time = time.time()
                game.player_choice = None

        elif game_state == "RESULT":
            if time.time() - last_result_time > result_display_time:
                game.reset_round()
                game_state = "PLAY"
                last_gesture_time = time.time()

        draw_ui(game, processed_frame)

    cap.release()
    pygame.quit()

if __name__ == '__main__':
    main()
