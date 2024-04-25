import pygame

def notification_play():
    pygame.init()
    pygame.mixer.music.load('./assets/sound-1.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()