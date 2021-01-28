from matrix import *
from numba import njit


class Object:
    def __init__(self, pos, vert, faces):
        self.pos = pos
        self.vert = vert
        self.faces = faces

    def rotate_x(self, a):
        self.vert = self.vert @ rotate_x(a)

    def rotate_y(self, a):
        self.vert = self.vert @ rotate_y(a)

    def rotate_z(self, a):
        self.vert = self.vert @ rotate_z(a)

    def draw(self, screen, zbuffer, cam):
        w, h = screen.width, screen.height

        vert = self.vert
        vert = vert @ translate(self.pos[:3])

        for f in self.faces:
            screen_coords = []
            world_coords = []

            for i in range(3):
                v = self.vert[f[i]]
                screen_coords.append(np.array([
                    (v[0] + 1) * screen.width * 0.5, (v[1] + 1) * screen.height * 0.5, (v[2] + 1) * 255 * 0.5
                ]))
                world_coords.append(v)

            n = get_normal(*world_coords)
            l = get_light(n)

            triangle(*screen_coords, screen, zbuffer, [int(l*255)])


def load_obj(pos, file, sc = 1):
    vertex, faces = [], []

    with open(file) as f:
        for line in f:
            if line.startswith('v '):
                vertex.append([float(i) for i in line.split()[1:]] + [1])

            elif line.startswith('f'):
                faces_ = line.split()[1:]

                faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
    
    vertex = vertex @ scale(sc)

    return Object(pos, vertex, faces)


@njit(fastmath=True)
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

@njit(fastmath = True)
def get_normal(v1, v2, v3):
    ab = v1 - v2
    bc = v2 - v3

    return norm([ab[1] * bc[2] - ab[2] * bc[1], ab[2] * bc[0] - ab[0] * bc[2], ab[0] * bc[1] - ab[1] * bc[0]])

@njit(fastmath = True)
def norm(v):
    s = (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) ** 0.5

    return np.array([v[0] / s, v[1] / s, v[2] / s])

@njit(fastmath=True)
def get_light(n):
    return dot(n, np.array([0, 0, 1]))


def triangle(t0, t1, t2, image, zbuffer, color):
    if t0[0] == t1[0] and t0[0] == t2[0]:
        return
    if t0[1] > t1[1]:
        t0, t1 = t1, t0
    if t0[1] > t2[1]:
        t0, t2 = t2, t0
    if t1[1] > t2[1]:
        t1, t2 = t2, t1
    total_height = int(t2[1] - t0[1])
    for i in range(total_height):
        second_half = i > t1[1] - t0[1] or t1[1] == t0[1]
        segment_height = int(t2[1]-t1[1]) if second_half else int(t1[1]-t0[1])
        alpha = i / total_height
        if segment_height == 0:
            beta = 0
        else:
            beta = (i - (t1[1] - t0[1] if second_half else 0)) / segment_height
        A = t0 + (t2 - t0) * alpha
        for k in range(len(A)):
            A[k] = int(A[k])
        B = t1 + (t2 - t1) * beta if second_half else t0 + (t1 - t0) * beta
        for k in range(len(B)):
            B[k] = int(B[k])
        if A[0] > B[0]:
            A, B = B, A
        for j in range(int(A[0] + 0.5), int(B[0] + 0.5)):
            phi = 1 if B[0] == A[0] else (j - A[0]) / (B[0] - A[0])
            P = A + (B - A) * phi
            P[0] = int(P[0])
            P[1] = int(P[1])
            idx = int(P[0]+P[1]*image.width)
            if zbuffer[idx] < P[2]:
                zbuffer[idx] = P[2]
                P[0] = j; P[1] = t0[1]+i
                image.point(P[0], P[1], color)