import asyncio
from vpython import sphere, vector, rate, mag, norm, cross
import random

async def main():
    ###### Define Parameters #####
    G = 1
    M = 1
    R = 1
    rsoft = 0.03
    w = vector(0, 0.05, 0)
    n = 0
    N = 100
    stars = []

    ##### Main #####
    while n < N:
        rt = R * vector(2 * random.random() - 1, 2 * random.random() - 1, 2 * random.random() - 1)
        stars.append(sphere(pos=rt, radius=R / 30, make_trail=False, retain=100))
        n += 1

    for star in stars:
        star.m = M / N
        star.p = star.m * cross(w, vector(star.pos.x, 0, star.pos.z))
        star.F = vector(0, 0, 0)

    t = 0
    dt = 0.01

    while t < 10:
        rate(100)
        for star in stars:
            star.F = vector(0, 0, 0)
        for i in range(len(stars)):
            for j in range(len(stars)):
                if i != j:
                    rji = stars[i].pos - stars[j].pos
                    stars[i].F -= G * stars[i].m * stars[j].m * norm(rji) / (mag(rji)**2 + rsoft**2)

        for star in stars:
            star.p += star.F * dt
            star.pos += star.p * dt / star.m
        t += dt

# Run the main function using asyncio
asyncio.run(main())




