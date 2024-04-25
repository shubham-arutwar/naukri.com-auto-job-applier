import pygame

def bruh():
    pygame.init()
    pygame.mixer.music.load('./assets/bruh-sound-effect-2-37927.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()