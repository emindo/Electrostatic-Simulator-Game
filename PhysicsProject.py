from turtle import mode
import pygame as py
import sys
import math

#initialise pygame
py.init()

#Screen Settings
WIDTH, HEIGHT = 800,600
screen = py.display.set_mode((WIDTH,HEIGHT))
py.display.set_caption("Charge!")


#Colors
posColor = (255,0,0)
negColor = (0,0,255)
neuColor = (169,169,169)
targetneuColor = (200,200,200)
targetposColor = (255,182,193)
targetnegColor = (173,216,230)
fontColor = (0,0,0)
screenColor = (255,255,255)
goalColor = (255,165,0)

#physics related constants
k_constant = 1 #Represents k electric constant
MIN_DISTANCE = 10  #Minimum Distance between center of charges
MAX_VELOCITY = 100 #Escape Velocity

#game settings
GOAL_WIDTH, GOAL_HEIGHT = 100, 100
GOAL_SIZE = 100
SIZE_SCALING = 5 #amount increase in size when combining charges
font = py.font.SysFont(None, 25)
hfont = py.font.SysFont(None, 20)
level = 0
fixed_mode = False
title_font = py.font.SysFont(None, 60)
button_font = py.font.SysFont(None, 30)
game_won = False
clock = py.time.Clock()

#Make Levels

LEVEL_DATA = [
    #Level 1
    {
        "target_position":(WIDTH // 2, 100),
        "target_charge": 1,
        "goal_position":(WIDTH // 2 - GOAL_SIZE//2, HEIGHT // 2 - GOAL_SIZE//2 + 100),
        "obstacles": [
            ],
        "max_charges": 3,
        "text": ["Tutorial: right click to place a neg charge->", "Negative charge will attract the target positive charge", "You can click more than once to increase its magnitude"],
        "text_position": [(10,500), (WIDTH // 2 - 200,50),(0,550)]
        },

    
    #Level 2
    {
        "target_position":(WIDTH // 2, 300),
        "target_charge": 1,
        "goal_position":(WIDTH // 2 - GOAL_SIZE//2, HEIGHT // 2 - GOAL_SIZE//2 + 200),
        "obstacles": [
            ],
        "max_charges": 3,     
        "text":["Tutorial: left click to place a pos charge->", "The pos charge will repel the target positive charge"],
        "text_position": [(10,135), (WIDTH // 2 - 200,50)]
         },
    #Level 3
    {
        "target_position":(WIDTH // 2 - 250, HEIGHT // 2),
        "target_charge": -1,
        "goal_position":(WIDTH // 2 - GOAL_SIZE//2 + 300, HEIGHT // 2 - GOAL_SIZE//2),
        "obstacles": [
            {"position": (WIDTH // 2, HEIGHT // 2), "charge": -1, "fixed": True},
            ],
        "max_charges": 3,     
        "text":["Tutorial: Make this charge positive by adding positive charge to it"],
        "text_position": [(30,275)]
         },
    #Level 4
    {
        "target_position":(WIDTH // 2 - 250, HEIGHT // 2),
        "target_charge": -1,
        "goal_position":(WIDTH // 2 - GOAL_SIZE//2, HEIGHT // 2 - GOAL_SIZE//2 + 200),
        "obstacles": [
            {"position": (WIDTH // 2, HEIGHT // 2), "charge": -1, "fixed": True},
            ],
        "max_charges": 3,     
        "text":["No more tutorial :("],
        "text_position": [(300,100)]
         },
    #Level 5
    {
        "target_position":(WIDTH // 2 - 250, HEIGHT // 2 - 250),
        "target_charge": -1,
        "goal_position":(WIDTH // 2 - GOAL_SIZE//2 + 200, HEIGHT // 2 - GOAL_SIZE//2 + 200),
        "obstacles": [
            {"position": (400, 500), "charge": 1, "fixed": True},
            {"position": (500, 350), "charge": 1, "fixed": True}
            ],
        "max_charges": 3,     
        "text":["No more tutorial :("],
        "text_position": [(300,100)]
         },
    #Level 6
    {
        "target_position":(WIDTH // 2 + 250, HEIGHT // 2 - 250),
        "target_charge": -1,
        "goal_position":(WIDTH // 2 - GOAL_SIZE//2 - 200, HEIGHT // 2 - GOAL_SIZE//2 + 200),
        "obstacles": [
            {"position": (270, 400), "charge": 1, "fixed": True},
            {"position": (400, 350), "charge": -1, "fixed": True},
            {"position": (100, 300), "charge": 1, "fixed": True}
            ],
        "max_charges": 3,     
        "text":["No more tutorial :("],
        "text_position": [(300,100)]
         },     
    #Level 7
    {
        "target_position":(WIDTH // 2 - 250, HEIGHT // 2),
        "target_charge": -1,
        "goal_position":(WIDTH // 2 - GOAL_SIZE//2 + 200, HEIGHT // 2 - GOAL_SIZE//2),
        "obstacles": [
            {"position": (200, 200), "charge": 1, "fixed": True},
            {"position": (400, 400), "charge": -1, "fixed": True},
            {"position": (200, 400), "charge": 1, "fixed": True},
            {"position": (400, 200), "charge": -1, "fixed": True}
            ],
        "max_charges": 3,     
        "text":["Good Luck!"],
        "text_position": [(300,100)]
         },
    #Level 8
    {
        "target_position":(WIDTH // 2, HEIGHT // 2 + 250),
        "target_charge": 1,
        "goal_position":(WIDTH // 2 - GOAL_SIZE//2 , HEIGHT // 2 - GOAL_SIZE//2 - 200),
        "obstacles": [
            {"position": (WIDTH//2 + WIDTH//8, 200), "charge": -1, "fixed": True},
            {"position": (WIDTH//2 + WIDTH//4, 400), "charge": -1, "fixed": True},
            {"position": (WIDTH // 2, 100), "charge": 2, "fixed": True},
            {"position": (WIDTH//2 - WIDTH//8, 200), "charge": -1, "fixed": True},
            {"position": (WIDTH//2 - WIDTH//4, 400), "charge": -1, "fixed": True}
            ],
        "max_charges": 3,     
        "text":[" "],
        "text_position": [(WIDTH // 2, 50)]
         },
     #Level 9
    {
        "target_position":(WIDTH // 2 - 100, HEIGHT // 2 - 200),
        "target_charge": 0,
        "goal_position":(WIDTH // 2 - GOAL_SIZE//2 + 200, HEIGHT // 2 - GOAL_SIZE//2+200),
        "obstacles": [
            {"position": (200, 200), "charge": 1, "fixed": True},
            {"position": (300, 300), "charge": -1, "fixed": True},
            {"position": (400, 400), "charge": 1, "fixed": True},
            {"position": (500, 200), "charge": -1, "fixed": True},
            {"position": (600, 300), "charge": 1, "fixed": True},
            {"position": (700, 400), "charge": -1, "fixed": True}
            ],
        "max_charges": 3,     
        "text":["Almost there!"],
        "text_position": [(300,100)]
         },
     #Level 10
    {
        "target_position":(WIDTH // 2, HEIGHT // 2),
        "target_charge": 1,
        "goal_position":(WIDTH // 2 - GOAL_SIZE//2, HEIGHT // 2 + GOAL_SIZE//2+200),
        "obstacles": [
            {"position": (200, HEIGHT // 2), "charge": 1, "fixed": True},
            {"position": (300, HEIGHT // 2), "charge": 1, "fixed": True},
            {"position": (400, HEIGHT // 2), "charge": 1, "fixed": True},
            {"position": (500, HEIGHT // 2), "charge": 1, "fixed": True},
            {"position": (600, HEIGHT // 2), "charge": 1, "fixed": True},
            {"position": (700, HEIGHT // 2), "charge": 1, "fixed": True},
            {"position": (700, HEIGHT // 2), "charge": 1, "fixed": True}
            ],
        "max_charges": 6,     
        "text":["Last Level!"],
        "text_position": [(300,100)]
         }
   ]


#Charge Class

class Charge:
    def __init__(self, position, color, q_charge, fixed, radius = 10, istarget = False, mass = 1):
        self.position = py.Vector2(position)
        self.color = color
        self.base = color
        self.q_charge = q_charge #- for neg charge and + for pos charge
        self.radius = radius
        self.velocity = py.Vector2(0,0)
        self.magnitude = abs(self.q_charge)
        self.fixed = fixed
        self.istarget = istarget
        self.mass = mass
        
        
    def draw(self, surface):
        py.draw.circle(surface, self.color, (int(self.position.x),int(self.position.y)), self.radius)
        
        
        charge_text = font.render(f"{self.q_charge}", True, fontColor)
        """
        text_circle = charge_text.get_circle()
        text_circle.center = (300, 300)
        screen.blit(text, text_rect)
        
        screen.blit(charge_text, (int(self.position.x) - self.radius/2,int(self.position.y)-self.radius/2))
        """
        text_surface = font.render(str(self.q_charge), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(int(self.position.x), int(self.position.y)))
        surface.blit(text_surface, text_rect)
        
        

    def apply_force(self, force):
        if not self.fixed or self.q_charge == 0:
            self.velocity += force / self.mass #Apply acceleration. a = force/mass
        
    def update_position(self):    
        if not self.fixed:
            self.position += self.velocity
            if self.velocity.length() > MAX_VELOCITY:
                self.velocity.scale_to_length(MAX_VELOCITY)
            
    def out_of_bounds(self, width, height):
        return (self.position.x - self.radius < 0 or
                self.position.x - self.radius > width or
                self.position.y - self.radius < 0 or
                self.position.y - self.radius > height)
    
    #update magnitude using the radius as representation. Update charge state using color
    def update_color_and_size(self):
        self.magnitude = abs(self.q_charge)
        
        self.radius = max(10, SIZE_SCALING * self.mass)
        if not self.istarget:
            if self.q_charge > 0:
                self.color = posColor
            elif self.q_charge < 0:
                self.color = negColor
            else:
                self.color = neuColor
        else:
            if self.q_charge > 0:
                self.color = targetposColor
            elif self.q_charge < 0:
                self.color = targetnegColor
            else:
                self.color = targetneuColor
        
    #check to see if charges are colliding          
    def check_collision(self, other_charge):
        distance = self.position.distance_to(other_charge.position)
        return distance < self.radius + other_charge.radius
    
    def handle_collision(self, other_charge):
        
        total_mass = self.mass + other_charge.mass
        if total_mass > 0:
            self.velocity = (self.velocity * self.mass + other_charge.velocity * other_charge.mass) / total_mass
        
        self.q_charge += other_charge.q_charge
        self.mass += other_charge.mass
        self.update_color_and_size()
        
   
            
    
#calculation of force between two chrages
def calculate_force(charge1, charge2):
    global k_constant
    direction = charge2.position - charge1.position #get direction vector and length
    distance = direction.length()
    if distance < MIN_DISTANCE:
        distance = MIN_DISTANCE
        
    #Magnitude of Force = k(q1q2)/r^2
    force_magnitude = abs(k_constant * charge1.q_charge * charge2.q_charge)/(distance ** 2) 
    force = py.Vector2(0,0)
    
    #Get Unit Vector and multiply by magnitude
    if not direction.length() == 0:
        if charge1.q_charge * charge2.q_charge > 0:
            force = -1 * direction.normalize() * force_magnitude
        else:
            force = 1 * direction.normalize() * force_magnitude
            
    return force

def setup_level(level_index):
    global target, goal_position, charges, game_won, charge_count, max_charges, custom_level_text, level_text_position
    
    level_data = LEVEL_DATA[level_index]
    target_pos = level_data["target_position"]
    target_charge = level_data["target_charge"]
    if target_charge > 0:
        target_color = targetposColor
    elif target_charge < 0:
        target_color = targetnegColor
    else:
        target_color = targetneuColor
    goal_position = py.Vector2(level_data["goal_position"])
    target = Charge(target_pos, target_color, target_charge, fixed = False, istarget=True)
    
    charges = [target]
    
    charge_count = 0
    max_charges = level_data["max_charges"]
    custom_level_text = level_data["text"]
    level_text_position = level_data["text_position"]

    for obstacle in level_data["obstacles"]:
        obstacle_color = posColor if obstacle["charge"] > 0 else negColor
        charges.append(Charge(obstacle["position"], obstacle_color, obstacle["charge"], obstacle["fixed"]))
    
# Function to calculate electric potential at a point
def calculate_potential(point, charges):
    total_potential = 0
    for charge in charges:
        r_vector = point - charge.position
        distance = r_vector.length()
        if distance > 0:  # Avoid division by zero
            total_potential += k_constant * charge.q_charge / distance
    return total_potential

def calculate_e_field(point):
        global charges
        e_field = py.Vector2(0, 0)
        for charge in charges:
            r = point - charge.position
            d = r.length()
            if d > 0:
                r_unit = r.normalize()
                field_contribution = k_constant * charge.q_charge / (d**2)
                e_field += r_unit * field_contribution
        return e_field

def main_menu():
    while True:
        screen.fill(screenColor)
        title_text = title_font.render("Electrostatics!", True, fontColor)
        play_text = button_font.render("Play", True, fontColor)
        how_to_play_text = button_font.render("How to Play", True, fontColor)
        simulation_text = button_font.render("Simulation", True, fontColor)
        
        #Display Title
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT// 4))
        
        #Create Play Button
        play_button = screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2))
        
        #Create Instruction Button
        how_to_play_button = screen.blit(how_to_play_text, (WIDTH // 2 - how_to_play_text.get_width() // 2, HEIGHT // 2 + 100))
        
        #Create Simulation Button
        simulation_button =  screen.blit(simulation_text, (WIDTH // 2 - simulation_text.get_width() // 2, HEIGHT // 2 + 200))
        
     
        py.display.flip()
        
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    setup_level(0)
                    game_loop(0)
                elif how_to_play_button.collidepoint(event.pos):
                    how_to_play_screen()
                elif simulation_button.collidepoint(event.pos):
                    simulation_mode()

def simulation_mode():
    global fixed_mode, start, k_constant, charges
    run = True
    fixed_mode = False
    charges = []
    start = False
    popup = False
    field_on = False
    potential_on = False
    clock.tick(60)
    
    input_box = py.Rect(30, 185, 40, 32)
    color_inactive = py.Color('Black')
    color_active = py.Color('Gray')
    color = color_inactive
    active = False
    text = '1'

    field_spacing = 50
    field_arrow = []
    
    
    
    while run:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            #Check if mouse is being clicked/outputted
            
            elif event.type == py.MOUSEBUTTONDOWN:
                #store position
                pos = py.mouse.get_pos()
                
                #if left click, positive char. if right click, negative charge
                if play_button.collidepoint(event.pos):
                    start = not start
                elif input_box.collidepoint(event.pos):
                    active = not active
                elif not input_box.collidepoint(event.pos) and active:
                    active = False
                elif popup_button.collidepoint(event.pos):
                    popup = True
                elif popup and close_button.collidepoint(event.pos):
                    popup = False
                elif button.collidepoint(event.pos):
                    field_on = not field_on
                elif button1.collidepoint(event.pos):
                    potential_on = not potential_on
                elif event.button == 1:
                    charges.append(Charge(pos, posColor, 1, fixed_mode))
                elif event.button == 3:
                    charges.append(Charge(pos, negColor, -1,fixed_mode))
                    
                color = color_active if active else color_inactive
                
                    
            #space to switch between fixed and non fixed charges
            #R to reset    
            elif event.type == py.KEYDOWN:
                if active:
                    if event.key == py.K_RETURN:
                        try:
                            number = int(text)
                            print("Entered number:", number)
                            k_constant = number
                            print(k_constant)
                            #text = ''
                        except ValueError:
                            #print("Invalid input")
                            text = ''
                    elif event.key == py.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode  
                elif event.key == py.K_SPACE:
                    fixed_mode = not fixed_mode
                
                elif event.key == py.K_r:
                    charges = []
                elif event.key == py.K_q:
                    main_menu()
         
        #fill screen white
        screen.fill(screenColor)
        
        txt_surface = font.render(text, True, color)
        
        k_text = font.render("k=", True, fontColor)
        screen.blit(k_text, (10, 190))
        

        width = max(40, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        py.draw.rect(screen, color, input_box, 2)
    
        field_arrow = []
        if field_on:
            for x in range(0, WIDTH, field_spacing):
                for y in range(0, HEIGHT, field_spacing):
                    point = py.Vector2(x, y)
                    e_field = calculate_e_field(point)
                    if e_field.length() > 0:  # Add field vector if there's a significant field
                        field_arrow.append((point, e_field.normalize()))

            # Draw the E-field arrows
                    
            for point, e_vector in field_arrow:
                end_point = point + e_vector * 20  # Scale the arrow length
                py.draw.line(screen, (128, 128, 128), point, end_point, 1)
                #py.draw.circle(screen, (128, 128, 128), (int(end_point.x), int(end_point.y)), 2)



        #Display Pos
        pos = py.mouse.get_pos()
        mode_surface = font.render(str(pos), True, fontColor)
        screen.blit(mode_surface, (10, 35))
        

        # Calculate electric potential at the mouse position
        

        # Display the potential value near the cursor
        if potential_on:
            potential = calculate_potential(pos, charges)
            potential_text = font.render(f"{potential:.2e} V", True, (0,0,0))
            screen.blit(potential_text, (pos[0] + 10, pos[1] - 20))
        
        #Potential Button
        p_text = font.render("Potential", True, fontColor)
        screen.blit(p_text, (10, 160))
        button1 = py.Rect(p_text.get_width() + 12, 160, 19, 20)
        
        py.draw.rect(screen, (0,0,0), py.Rect(p_text.get_width() + 11, 159, 22, 22))
        py.draw.rect(screen, (230,230,230), button1)
        
        V_text = button_font.render(" X " if potential_on else "   ", True, fontColor)
        V_text_x = screen.blit(V_text, (V_text.get_width()+ 60,162))
        
       
        #Display Fixed Mode State
        mode_text = "Fixed Mode" if fixed_mode else "Non-Fixed Mode"
        mode_surface = font.render(mode_text, True, fontColor)
        screen.blit(mode_surface, (10, 60))
        
        #Restart Reminder
        restart_surface = font.render("R to restart", True, fontColor)
        screen.blit(restart_surface, (10, 85))
        
        #Quit Reminder
        quit_text = font.render("Q to quit", True, fontColor)
        screen.blit(quit_text, (10, 110))
        
        #Play Button
        rect_color = (0,255,0) if start else (255,0,0)
        py.draw.rect(screen, rect_color , py.Rect(10, 8, 90, 20))
        play_text = button_font.render("Running" if start else "Run    ", True, fontColor)
        play_button = screen.blit(play_text, (10,10))
        
        #Field Button
        f_text = font.render("E-Field", True, fontColor)
        screen.blit(f_text, (10, 135))
        
        button = py.Rect(quit_text.get_width() + 12, 135, 19, 20)
        
        py.draw.rect(screen, (0,0,0), py.Rect(quit_text.get_width() + 11, 134, 22, 22))
        py.draw.rect(screen, (230,230,230), button)
        
        field_text = button_font.render(" X " if field_on else "   ", True, fontColor)
        field_text_x = screen.blit(field_text, (quit_text.get_width()+ 9,137))
        
       
        
        #Pop Up Button
        popup_color = (0,0,255)
        py.draw.rect(screen, popup_color , py.Rect(WIDTH-100, 8, 90, 20))
        popup_text = button_font.render("Stats    ", True, fontColor)
        popup_button = screen.blit(popup_text, (WIDTH-100,10))
        
       
        
       
        

        #calculate and apply force from all charges on all charges
        
        for i,charge1 in enumerate(charges):
            total_force = py.Vector2(0,0)
            for j,charge2 in enumerate(charges):
                if i!= j:
                    force = calculate_force(charge1, charge2)
                    total_force += force
            if start:
                charge1.apply_force(total_force)
    
        #Check if target is out of bounds
        
        
        charges = [charge for charge in charges if not charge.out_of_bounds(WIDTH, HEIGHT)]       
    
        #Handle Circle Collsions
        for i, charge1 in enumerate(charges):
            for j in range(i+1, len(charges)):
                charge2 = charges[j]
                if charge1.check_collision(charge2):
                    charge1.handle_collision(charge2)
                
                    # remove second charge after combining
                    charges.pop(j)
                    break
    
        #Draw all circles
        for charge in charges:
            if start:
                charge.update_position()
            charge.draw(screen)
         
        if popup:
            py.draw.rect(screen, (0,0,0) , py.Rect(WIDTH-302, 0, 302, HEIGHT))
            py.draw.rect(screen, screenColor , py.Rect(WIDTH-300, 2, 298, HEIGHT-4))
            
            py.draw.rect(screen, screenColor , py.Rect(WIDTH-20, 10, 10, 10))
            close_text = button_font.render("X", True, fontColor)
            close_button = screen.blit(close_text, (WIDTH-20,10))
            
            head_text = hfont.render("Charge(C) Position(m,m) Net Force(F)", True, fontColor)
            screen.blit(head_text, (WIDTH-300, 10))

            
            x = 30
            for i, charge in enumerate(charges):
                net_force = py.Vector2(0,0)
                for j,charge2 in enumerate(charges):
                    if i!= j:
                        force = calculate_force(charge, charge2)
                        net_force += force
                force_text =  "({:.1e},{:.1e})"
                force_text_conv = force_text.format(net_force.x, net_force.y)
                

                charge_text = "{:^12}{:^22}{:^18}"
                charge_text_conv = charge_text.format(charge.q_charge,  f"({int(charge.position.x)},{int(charge.position.y)})", force_text_conv)
                
                chargestat = hfont.render(charge_text_conv, True, fontColor)
                screen.blit(chargestat, (WIDTH-300, x))
                x += 20
       
 
             
             
        #update display
        py.display.flip()
        #clock.tick(60)

        



def how_to_play_screen():
    while True:
        screen.fill(screenColor)
        instructions = [
            "Goal: Move the target Charge (light colored charge) to the goal area (orange)",
            "Left Click places a positive charge (red)",
            "Right Click places a negative charge (blue)",
            "SPACE to toggle between fixed and movable charges",
            "R to restart a Level",
            "Postive and Negative charges attract and like charges repel",
            "Hitting the boundaries automatically restarts the level",
            "Charges can combine to increase in magnitude",
            "There is a limit to the amount of charge you can place in each level"
            ]
        
        for i, line in enumerate(instructions):
            instruction_text = font.render(line, True, fontColor)
            screen.blit(instruction_text, (50, 100 + i * 40))
        back_text = button_font.render("Back", True, fontColor)
        back_button = screen.blit(back_text, (WIDTH //2 - back_text.get_width() // 2, HEIGHT - 50))

        py.display.flip()
        
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
                


#Looping Frames
def game_loop(level_index):
    global level, fixed_mode, target, game_won, charges, charge_count, level_text, level_text_position
    run = True
    fixed_mode = True
    
    while run:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            #Check if mouse is being clicked/outputted
            
            elif event.type == py.MOUSEBUTTONDOWN and charge_count < max_charges:
                #store position
                pos = py.mouse.get_pos()
            
                #if left click, positive char. if right click, negative charge
                if event.button == 1:
                    charges.append(Charge(pos, posColor, 1, fixed_mode))
                    charge_count += 1
                elif event.button == 3:
                    charges.append(Charge(pos, negColor, -1,fixed_mode))
                    charge_count += 1
            #space to switch between fixed and non fixed charges
            #R to reset    
            elif event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    fixed_mode = not fixed_mode
                
                elif event.key == py.K_r:
                    setup_level(level_index)
                elif event.key == py.K_q:
                    main_menu()
         
        #fill screen white
        screen.fill(screenColor)
    
        level_text = f"Level: {level_index + 1}"
        level_surface = font.render(level_text, True, fontColor)
        screen.blit(level_surface, (10,10))
    
        #make goal
        py.draw.rect(screen, goalColor, (goal_position.x, goal_position.y, GOAL_WIDTH, GOAL_HEIGHT))
        
        #Charge count
        charge_text = font.render(f"Charges: {charge_count}/{max_charges}", True, fontColor)
        screen.blit(charge_text, (10,60))
        
        #Display Fixed Mode State
        mode_text = "Fixed Mode" if fixed_mode else "Non-Fixed Mode"
        mode_surface = font.render(mode_text, True, fontColor)
        screen.blit(mode_surface, (10, 35))
        
        #Restart Reminder
        restart_surface = font.render("R to restart", True, fontColor)
        screen.blit(restart_surface, (10, 85))
        
        #Quit Reminder
        quit_text = font.render("Q to quit", True, fontColor)
        screen.blit(quit_text, (10, 110))
        
        # display some text for each level
        for i in range (0,len(custom_level_text)):
            level_text_surface = font.render(custom_level_text[i], True, fontColor)
            screen.blit(level_text_surface, level_text_position[i])
    
    

        #calculate and apply force from all charges on all charges
    
        for i,charge1 in enumerate(charges):
            total_force = py.Vector2(0,0)
            for j,charge2 in enumerate(charges):
                if i!= j:
                    force = calculate_force(charge1, charge2)
                    total_force += force
            
            charge1.apply_force(total_force)
    
        #Check if target is out of bounds
        if target.out_of_bounds(WIDTH,HEIGHT):
            setup_level(level_index)
        else:
            charges = [charge for charge in charges if not charge.out_of_bounds(WIDTH, HEIGHT) or charge == target]       
    
        #Handle Circle Collsions
        for i, charge1 in enumerate(charges):
            for j in range(i+1, len(charges)):
                charge2 = charges[j]
                if charge1.check_collision(charge2):
                    charge1.handle_collision(charge2)
                
                    # remove second charge after combining
                    charges.pop(j)
                    break
    
        #Draw all circles
        for charge in charges:
            charge.update_position()
            charge.draw(screen)
    
        if goal_position.x <= target.position.x <= goal_position.x + GOAL_WIDTH and goal_position.y <= target.position.y <= goal_position.y + GOAL_HEIGHT:
             level_index += 1
             if level_index >= len(LEVEL_DATA):
                game_won = True
                win_text = title_font.render("You Win All Levels!", True, fontColor)
                screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))
                py.display.flip()
                py.time.delay(3000)
                main_menu()
             else:
                 setup_level(level_index)
             
        #update display
        py.display.flip()
    
            
    

main_menu()

