import sys, pygame

red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

window_width = 540
window_height = 540

def main():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode(size=(window_width, window_height), flags=pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption('Tic-Tac-Toe')
    clock = pygame.time.Clock()
    done = False

    screen.fill(black)

    while not done:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
