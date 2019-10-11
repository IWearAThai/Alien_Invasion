import pygame


class Beam(pygame.sprite.Sprite):
    """Manages beams fired from aliens"""
    def __init__(self, ai_settings, screen, alien):
        super().__init__()
        self.screen = screen

        # Initialize beam image and related variables
        self.image = pygame.image.load('images/alien_beam_resized.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        # Y position and speed factor
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.beam_speed_factor

    def update(self):
        """Move the beam down the screen"""
        self.y += self.speed_factor
        self.rect.y = self.y

    def blitme(self):
        """Draw the beam on the screen"""
        self.screen.blit(self.image, self.rect)
