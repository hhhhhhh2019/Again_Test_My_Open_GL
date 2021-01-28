import numpy as np
import math


def translate(pos):
    tx, ty, tz = pos
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ])


def rotate_x(a):
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(a), math.sin(a), 0],
        [0, -math.sin(a), math.cos(a), 0],
        [0, 0, 0, 1]
    ])


def rotate_y(a):
    return np.array([
        [math.cos(a), 0, -math.sin(a), 0],
        [0, 1, 0, 0],
        [math.sin(a), 0, math.cos(a), 0],
        [0, 0, 0, 1]
    ])


def rotate_z(a):
    return np.array([
        [math.cos(a), math.sin(a), 0, 0],
        [-math.sin(a), math.cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def scale(n):
    return np.array([
        [n, 0, 0, 0],
        [0, n, 0, 0],
        [0, 0, n, 0],
        [0, 0, 0, 1]
    ])


def proj(cam):
    near = cam.near_plane
    far = cam.far_plane
    right = math.tan(cam.h_fov / 2)
    left = -right
    top = math.tan(cam.v_fov / 2)
    bottom = -top

    m00 = 2 / (right - left)
    m11 = 2 / (top - bottom)
    m22 = (far + near) / (far - near)
    m32 = -2 * near * far / (far - near)
    return np.array([
        [m00, 0, 0, 0],
        [0, m11, 0, 0],
        [0, 0, m22, 1],
        [0, 0, m32, 0]
    ])


def to_screen(w, h):
    hw, hh = w // 2, h // 2
    return np.array([
            [hw, 0, 0, 0],
            [0, -hh, 0, 0],
            [0, 0, 1, 0],
            [hw, hh, 0, 1]
        ])