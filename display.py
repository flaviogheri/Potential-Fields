import pygame as pg
import json

with open('obs.json') as f:
    obs = json.load(f)

# print(data)
    
def parse_color(color_str):
    print(color_str)
    if color_str == "red":
        return (255, 0, 0)
    elif color_str == "green":
        return (0, 255, 0)
    elif color_str == "blue":
        return (0, 0, 255)
    elif color_str == "yellow":
        return (255, 255, 0)
    elif color_str == "purple":
        return (128, 0, 128)
    elif color_str == "orange":
        return (255, 165, 0)
    elif color_str == "pink":
        return (255, 192, 203)
    elif color_str == "black":
        return (0, 0, 0)
    elif color_str == "white":
        return (255, 255, 255)
    else:
        return (0, 0, 0)


    


def main():
    pg.init()

    disp_w = 800 
    disp_h = 600
    disp = pg.display.set_mode((disp_w,disp_h))
    pg.display.set_caption("Display Circle")

    pos = (int(obs['position']['x']), int(obs['position']['y']))
    radius = int(obs['length'])  # Assuming length represents the radius

    color = parse_color(obs['color'])
    #color = #parse_color(obs['color'])	

        # Main loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Clear the screen
        disp.fill(parse_color("white"))

        # Draw the circle
        pg.draw.circle(disp, color, pos, radius)

        # Update the display
        pg.display.flip()




    pg.quit()
if __name__ =="__main__":
    main()