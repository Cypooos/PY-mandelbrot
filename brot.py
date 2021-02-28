
import pygame

# Constantes
base_qualite = int(input("qualité ? => "))
MAX_ITERATION = base_qualite*2 # nombre d'itérations maximales avant de considérer que la suite converge
XMIN, XMAX, YMIN, YMAX = -2, +0.5, -1.25, +1.25# bornes du repère BASE : -2, +0.5, -1.25, +1.25

LARGEUR, HAUTEUR = 400, 400 # taille de la fenêtre en pixels
zoom = 1.0 # BASE: 1
# Initialisation et création d'une fenêtre aux dimensions spécifiéés munie d'un titre

def get_boundaries(min_x, max_x, min_y, max_y, zoom,center):

    if zoom == 1:
        zoom_padding = 1.5
    else:
        zoom_padding = 1/zoom

    min_x = center[0] - zoom_padding
    max_x = center[0] + zoom_padding
    min_y = center[1] - zoom_padding
    max_y = center[1] + zoom_padding

    return min_x, max_x, min_y, max_y
pygame.init()
screen = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption("Fractale de Mandelbrot")
def update():
  count = 0
  for y in range(HAUTEUR):
    for x in range(LARGEUR):
      # Les deux lignes suivantes permettent d'associer à chaque pixel de l'écran de coordonnées (x;y)
      # un point C du plan de coordonnées (cx;cy) dans le repère défini par XMIN:XMAX et YMIN:YMAX
      cx = (x * (XMAX - XMIN) / LARGEUR + XMIN)
      cy = (y * (YMIN - YMAX) / HAUTEUR + YMAX)
      xn = 0
      yn = 0
      n = 0
      while (xn * xn + yn * yn) < 4 and n < MAX_ITERATION: # on teste que le carré de la distance est inférieur à 4 -> permet d'économiser un calcul de racine carrée coûteux en terme de performances
        # Calcul des coordonnes de Mn
        tmp_x = xn
        tmp_y = yn
        xn = tmp_x * tmp_x - tmp_y * tmp_y + cx
        yn = 2 * tmp_x * tmp_y + cy
        n = n + 1
      if n == MAX_ITERATION:
        screen.set_at((x, y), (0, 0, 0))
      else:
        screen.set_at((x, y), ((3 * n) % 256, (1 * n) % 256, (10 * n) % 256))
    count +=1
    if count == 10:pygame.display.flip();count = 0
update()

loop = True
while loop:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: # Pour quitter l'application en fermant la fenêtre
      loop = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      p = pygame.mouse.get_pos()
      px = (p[0] * (XMAX - XMIN) / LARGEUR + XMIN)
      py = (p[1] * (YMIN - YMAX) / HAUTEUR + YMAX)
      print("({};{};{})".format(px,py,zoom))
      zoom *=32
      MAX_ITERATION +=base_qualite
      XMIN, XMAX, YMIN, YMAX = get_boundaries(XMIN, XMAX, YMIN, YMAX, zoom, (px,py))
      update()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        p = pygame.mouse.get_pos()
        px = (p[0] * (XMAX - XMIN) / LARGEUR + XMIN)
        py = (p[1] * (YMIN - YMAX) / HAUTEUR + YMAX)
        print("({};{};{})".format(px,py,zoom))
        MAX_ITERATION -=(base_qualite/2)
        XMIN, XMAX, YMIN, YMAX = get_boundaries(XMIN, XMAX, YMIN, YMAX, zoom, (px,py))
        update()
      elif event.key == pygame.K_q:
        pygame.quit()
        exit()
      else:
        p = pygame.mouse.get_pos()
        px = (p[0] * (XMAX - XMIN) / LARGEUR + XMIN)
        py = (p[1] * (YMIN - YMAX) / HAUTEUR + YMAX)
        print("({};{};{};{})".format(XMIN, XMAX, YMIN, YMAX))
        zoom /=16
        MAX_ITERATION -=base_qualite
        XMIN, XMAX, YMIN, YMAX = get_boundaries(XMIN, XMAX, YMIN, YMAX, zoom, (px,py))
        update()
pygame.quit()
