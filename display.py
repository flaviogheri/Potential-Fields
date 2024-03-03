import pygame as pg
import json
from agent import Agent
import numpy as np

with open('obs.json') as f:
    obs = json.load(f)

    
def parse_color(color_str):
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


    with open('agent.json') as f:
        agent_data = json.load(f)


    # Extract x and y coordinates from the position dictionary
    position = (agent_data['position']['x'], agent_data['position']['y'])


    # Create agent object
    agent = Agent(position=position, color=agent_data['color'], radius=agent_data['length'], max_speed=0.5)

    agent.obstacles_p = (int(obs['position']['x']), int(obs['position']['y']))


    # Main loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        agent.move()


        # Clear the screen
        disp.fill(parse_color("white"))

        # Draw the agent
        pg.draw.circle(disp, agent.color, agent.p.astype(int), agent.r)\
        
        
        # Draw obstacles (assuming there's only one for now)
        obs_pos = (int(obs['position']['x']), int(obs['position']['y']))
        obs_radius = int(obs['length'])
        obs_color = parse_color(obs['color'])
        pg.draw.circle(disp, obs_color, obs_pos, obs_radius)

        # Update the display
        pg.display.flip()
    pg.quit()
if __name__ =="__main__":
    main()