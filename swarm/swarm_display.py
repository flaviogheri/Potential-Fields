import pygame as pg
import json
from agentinswarm import swarm_agent
import numpy as np
import time

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
    pg.display.set_caption("Swarm Simulation")

    # Load agent data from JSON
    with open('agents.json') as f:
        agents_data = json.load(f)

    # Create a list to hold swarm agents
    swarm_agents = []

    # Create swarm agents from the data
    for agent_data in agents_data:
        position = (agent_data['position']['x'], agent_data['position']['y'])
        center_position = (agent_data['center_position']['x'], agent_data['center_position']['y'])
        agent_color = agent_data['color']
        agent_radius = agent_data['length']
        alpha_avoid = agent_data['alpha_avoid']
        Rta_ratio = agent_data['Rta_ratio']

        agent = swarm_agent(center_position=center_position, position=position, color=agent_color, alpha_avoid=alpha_avoid, Rta_ratio=Rta_ratio, radius=agent_radius, max_speed=0.8)
        swarm_agents.append(agent)

    # Set clock for framerate
    clock = pg.time.Clock()
    fps = 60  # Adjust this value to change the framerate (lower value slows down the simulation)

    # Main loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Limit framerate
        dt = clock.tick(fps) / 1000  # Convert milliseconds to seconds for calculations
        # Clear the screen
        disp.fill(parse_color("white"))

        for agent in swarm_agents:

            obstacle_positions = [other_agent.p for other_agent in swarm_agents if other_agent != agent]
            agent.obstacles_p = obstacle_positions
        
        x, y = swarm_agents[0].center_position
        y += dt * -10 # Adjust the multiplier to change the speed of movement
        new_pos = (int(x), int(y))
        print("new_pos: ", new_pos)
        pg.draw.circle(disp, (0, 0, 0), new_pos, agent.r)




        # Move each swarm agent
        print("swarm agents:", swarm_agents)
        for agent in swarm_agents:
            agent.dt = dt
            # agent.swarm_field.center = new_pos
            # agent.swarm_field.pos = agent.p
            print("swarm center according to agent: ", agent.swarm_field.center)
            agent.center_position = new_pos
            agent.move()
            time.sleep(0.1)

        # Draw each swarm agent
        for agent in swarm_agents:
            pg.draw.circle(disp, agent.color, agent.p.astype(int), agent.r)

        if obs:
            obs_pos = (int(obs['position']['x']), int(obs['position']['y']))
            obs_radius = int(obs['length'])
            obs_color = parse_color(obs['color'])
            pg.draw.circle(disp, obs_color, obs_pos, obs_radius)


        # Update the display
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()

