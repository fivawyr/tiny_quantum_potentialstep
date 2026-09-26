from vpython import *
import math
type f32 = float


e = float(input("Please enter your desired initial kinetic Energy (in eV): "))
v = float(input("Please enter your desired potential energy height (in eV): "))
hbar = 1.0545718 * 10**(-34)
e_mass = 9.11 * 10**(-31)

def schroedinger(e: f32, v: f32):
    k_1 = math.sqrt(2 * e_mass * e) / hbar
    if e > v:
        k_2 = math.sqrt(2 * e_mass * (e - v)) / hbar
        r = ((k_1 - k_2) / (k_1 + k_2)) ** 2
        t = (4 * k_1 * k_2) / (k_1 + k_2) ** 2
    else:
        k_2 = None
        r = 1.0
        t = 0.0

    return t, r, k_1, k_2

eV = 1.602176634 * 10**(-19)
t_coef, r_coef, k_1, k_2 = schroedinger(e * eV, v * eV)

print(f"Transmission T = {t_coef:.4f}, Reflection R = {r_coef:.4}, T + R = {t_coef + r_coef:.4f}")

scene.title = "Quantum Potential Step"
scene.width = 900
scene.height = 500
scene.background = color.black
scene.range = 12
step_x = 0

step_height_visual = 3 * (v / max(e, 0.001)) 
step_height_visual = min(step_height_visual, 6)
floor = curve(pos=[vector(-10, 0, 0), vector(step_x, 0, 0)], color=color.white)
wall_up = curve(pos=[vector(step_x, 0, 0), vector(step_x, step_height_visual, 0)], color=color.red)
step_top = curve(pos=[vector(step_x, step_height_visual, 0), vector(10, step_height_visual, 0)], color=color.red)
label(pos=vector(-5, -1.5, 0), text=f"E = {e} eV", box=False, height=14, color=color.cyan)
label(pos=vector(5, step_height_visual + 1, 0), text=f"V = {v} eV", box=False, height=14, color=color.red)
label(pos=vector(0, -3, 0), text=f"T = {t_coef:.3f}   R = {r_coef:.3f}",box=False, height=16, color=color.yellow)

particle = sphere(pos=vector(-10, 0.3, 0), radius=0.3, color=color.cyan, make_trail=True)
speed = 0.08
reached_step = False
outcome_decided = False
transmitted = None

while True:
    rate(60)
    if not reached_step:
        particle.pos.x += speed
        if particle.pos.x >= step_x:
            reached_step = True
            transmitted = random() < t_coef
    else:
        if transmitted:
            particle.pos.x += speed * 0.6
            particle.color = color.green
        else:
            particle.pos.x -= speed
            particle.color = color.orange

    if particle.pos.x > 10 or particle.pos.x < -10:
        particle.pos = vector(-10, 0.3, 0)
        particle.clear_trail()
        reached_step = False
        particle.color = color.cyan
