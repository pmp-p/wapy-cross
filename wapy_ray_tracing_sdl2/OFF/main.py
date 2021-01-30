#!/bin/python

from math import sqrt
from .vec import Vec3
from .ray import Ray

# SDL
from random.pseudo import randint
from .sdl import sdl_init
from .sdl import ttf_init
from .sdl import create_window_and_renderer
from .sdl import create_rgb_surface
from .sdl import Window
from .sdl import Renderer
from .sdl import Surface
from .sdl import Texture
from .sdl import Rect
from .sdl import Color

# use bmp instead of png
from .sdl import load_bmp


from .wapy import int
from .wapy import float

#if __EMSCRIPTEN__
from .wapy import MYS
from .wapy import mys_start
from .wapy import mys_loops
from .wapy import mys_counter
#else
from fiber import sleep
#endif


"""mys-embedded-c++-before-namespace
#if __EMSCRIPTEN__
#include "emscripten.h"
#include <unistd.h>
#endif
"""

TITLE: string = "ray tracing (SDL2)"
WIN_WIDTH: i64 = 480
WIN_HEIGHT: i64 = 640
MYS_LOGO: string = "assets/mys-logo-30-25.bmp"

#MYS_RD: string = "assets/out.bmp"
#FOREGROUND_COLOR: Color = Color(0, 170, 170, 0)




class Display:

    width: i64
    height: i64
    screen: Surface
    texture: Texture

    #mys_logo: Surface
    tmys_logo: Texture

    #mys_fb: Surface
    #tmys_fb: Texture


    window: Window
    renderer: Renderer

    def __init__(self, width: i64, height: i64, title: string):
        self.width = width
        self.height = height
        print("sdl_init")
        sdl_init()
        print("create windows+renderer")
        self.window, self.renderer = create_window_and_renderer(width, height, 0)
        print("created windows+renderer")
        #self.window.set_title(title)
        self.screen = create_rgb_surface(0,
                                         width,
                                         height,
                                         32,
                                         0x00ff0000,
                                         0x0000ff00,
                                         0x000000ff,
                                         0xff000000)
        print("tex")
        self.texture = self.renderer.create_texture(width, height)

        print("loading img")
        #img_init()
        #self.mys_logo = img_load(MYS_LOGO)
        print("loaded img")


        #print("load logo")
        #self.mys_logo = load_bmp(MYS_LOGO)
        #self.tmys_logo = self.renderer.create_texture_from_surface(self.mys_logo)

        print("loading bmp")
        self.tmys_logo = self.sprite(MYS_LOGO)
        print("loaded bmp")


    def sprite(self, path: string) -> Texture:
        return self.renderer.create_texture_from_surface( load_bmp(path) )


    def fill_rect(self, rect: Rect, fg_color: Color):
        value = self.screen.map_rgb(fg_color.r, fg_color.g, fg_color.b)
        self.screen.fill_rect(rect, value)


    def draw_logo(self):
        tw, th = self.tmys_logo.query()
        self.renderer.copy(self.tmys_logo, Rect((WIN_WIDTH - tw) / 2, 20, tw, th))

    def draw_content(self):
        #nx, ny = 50, 25
        nx, ny = 100, 50

        #print("P3")

        #print(f"{nx} {ny}")
        #print("255")

        lower_left_corner = Vec3(-2.0, -1.0, -1.0)
        horizontal = Vec3(4.0, 0.0, 0.0)
        vertical = Vec3(0.0, 2.0, 0.0)
        origin = Vec3(0.0, 0.0, 0.0)

        for j in range(ny - 1, -1, -1):
            for i in range(nx):
                u, v = f32(i) / f32(nx), f32(j) / f32(ny)
                ray = Ray(origin,
                          lower_left_corner + horizontal * u + vertical * v)
                col = color(ray)
                ir = i32(255.99 * col.x)
                ig = i32(255.99 * col.y)
                ib = i32(255.99 * col.z)
                #print(f"{ir} {ig} {ib}")

                self.renderer.set_draw_color(ir, ig, ib, 255);
                self.renderer.draw_point(150  + i, i64( 100 + ( i64(mys_counter()) % (WIN_HEIGHT/2)) + j ) )



    def step(self):

        self.renderer.set_draw_color(0, 0, 0, 0);
        self.renderer.clear()
        self.draw_logo()
        self.draw_content()
        self.renderer.present()


def hit_sphere(center: Vec3, radius: f32, ray: Ray) -> f32:
    oc = ray.origin - center
    a = ray.direction.dot(ray.direction)
    b = 2.0 * oc.dot(ray.direction)
    c = oc.dot(oc) - radius * radius
    discriminant = b * b - 4.0 * a * c

    if discriminant < 0.0:
        return -1.0
    else:
        return (-b - sqrt(discriminant)) / 2.0 / a

def color(ray: Ray) -> Vec3:
    t = hit_sphere(Vec3(0.0, 0.0, -1.0), 0.5, ray)

    if t > 0.0:
        n = (ray.point_at_parameter(t) - Vec3(0.0, 0.0, -1.0)).unit_vector()

        return Vec3(n.x + 1.0, n.y + 1.0, n.z + 1.0) * 0.5

    unit_direction = ray.direction.unit_vector()
    t = 0.5 * (unit_direction.y + 1.0)

    return Vec3(1.0, 1.0, 1.0) * (1.0 - t) + Vec3(0.5, 0.7, 1.0) * t



DPY : Display = None

def loop():
    if mys_loops() >0:
        DPY.step()
    else:
        c"""
        printf("Bye\r\n");
        emscripten_cancel_main_loop();
        """

def main():
    mys_start(15)




    DPY = Display(WIN_WIDTH, WIN_HEIGHT, TITLE)



    c"""
    printf("loop set\r\n");
    emscripten_set_main_loop(loop, 0, 1);
    """



