"""for 2-dimensional physics"""
import math
from pygame.math import Vector2 as V

def projection_length(v1, v2):
    """Norm of the projection of v1 on v2."""
    angle = v1.angle_to(v2)
    return cos(angle)*v1.length()

def projection(v1, v2):
    """Projection of v1 on v2."""
    return projection_length(v1,v2)*v2.normalize()

#dv' * n = -e*dv*n
#impulse p1 = j*n (for A) and p2 = -j*n (for B) (newton's 3rd law)
#definition : rPoi = rPi.rotate(90) (rPoi = vect from an object's cm to point P)
#v1' = v1 + p1/m1; v2' = v2 + p2/m2 (translation only)
#w1' = w1 + L1/I1 = w1 + rPo1*|j|n / I1 (rotations only)
#v1P' = v1' + w1'*rPo1
# ==> j = -(1+e)*dv*n / K,
# K = n*n(1/m1 + 1/m2) + (rPo1*n)^2/I1 + (rPo2*n)^2/I2

def point_collision(ves1, ves2, point, e=1.):
    #1. get some variables
    v1, v2 = ves1.physics.v, ves2.physics.v
    dv = v1-v2
    rP1 = point - ves1.physics.q+ves1.physics.cm
    rP2 = point - ves2.physics.q+ves2.physics.cm
    n = (rP2-rP1).normalize()
    if dv*n >= 0: #then this is not a collision
        return
    rP1o = rP1.rotate(90)
    rP2o = rP2.rotate(90)
    I1, I2 = ves1.physics.I, ves2.physics.I
    m1, m2 = ves1.physics.m, ves2.physics.m
    w1, w2 = ves1.physics.w, ves2.physics.w
    #2. compute impulse
    K = n*n*(1./m1 + 1./m2) + (rP1o*n)**2/I1 + (rP2o*n)**2/I2
    j = -(1.+e)*dv*n / K
    jn = j*n
    #3. get quantiteis after collision
    v1new = v1 + jn/m1
    v2new = v2 - jn/m2
    w1new = w1 + rP1o*jn / I1
    w2new = w2 - rP2o*jn / I2
    #4. attribute new quantities
    ves1.physics.v = v1new
    ves2.physics.v = v2new
    ves1.physics.w = w1new
    ves2.physics.w = w2new

#functions for discrete bodies (not continuum)
def discrete_compute_center_mass(m, q):
    """m : list of masses
    q : list of corresponding positions.
    """
    M = sum(m)
    Rx = sum([m[i]*q[i][0] for i in range(len(m))]) / M
    Ry = sum([m[i]*q[i][1] for i in range(len(m))]) / M
    R = V(Rx,Ry)
    return R

def discrete_compute_I(m, q):
    """m : list of masses
    q : list of corresponding positions.
    """
    return sum([m[i]*q[i].length()**2 for i in range(len(m))])

def I_box(m,w,l):
    """Moment of a box with mass m, width w and length l."""
    return m * (w**2 + l**2) / 12

class RigidBody(object):

    def __init__(self, m=1, cm=(0,0), I=1, t=0, q=(0,0)):
        #translations:
        self.m = m #mass
        self.q = V(q) #position
        self.v = V(0,0) #velocity
        self.f = V(0,0) #external force
        #rotations (z-axis only):
        self.cm = V(cm) #to be updated!
        self.I = I # ~rotational mass
        self.t = t # ~rotational position
        self.w = 0 # ~rotational velocity (dteta/dt)
        self.tau = 0.# torque~rotational external force

    def get_copy(self):
        x = RigidBody(self.m, self.cm, self.I, self.t, self.q)
        x.v = V(self.v)
        x.f = V(self.f)
        x.w = self.w
        x.tau = self.tau
        return x

    def kinetic_translation_energy(self):
        return 0.5 * self.m * self.vnorm()**2

    def kinetic_rotation_energy(self):
        return 0.5 * self.I * self.w**2

    def decompose(self, vect, point):
        """Returns:
            a) A vector that is the the projection of <vect> along the line from
                <point> to the center of self;
            b) A scalar that is the torque.
        """
        cm_to_point = self.cm - point
        if cm_to_point: #rotation + translation
            cm_unit = cm_to_point.normalize()
            angle = cm_to_point.angle_to(vect)
            angle_rad = math.radians(angle)
            sin, cos = math.sin(angle_rad), math.cos(angle_rad)
            norm = vect.length()
            return cos*norm*cm_unit, sin*norm*cm_unit
        else: #translation only
            return vect, 0.

    def apply_force(self, force, point):
        """Returns:
            a) A vector that is the force for translations;
            b) A scalar that is the torque.
        """
        cm_to_point = self.cm - point
        if cm_to_point: #rotation + translation
            cm_unit = cm_to_point.normalize()
            angle = cm_to_point.angle_to(force)
            angle_rad = math.radians(angle)
            sin, cos = math.sin(angle_rad), math.cos(angle_rad)
            norm = force.length()
            return cos*norm*cm_unit, sin*norm*cm_to_point.length()
        else: #translation only
            return force, 0.


    def iterate(self, dt):
        #translation
##        print(self.f.length())
        a = self.f / self.m
        self.v += a*dt
        self.q += self.v*dt
        #rotation
        a = self.tau / self.I
        self.w += a*dt
        self.t += self.w*dt

    def vnorm(self):
        return self.v.length()

    def get_cm_to_point(self, q):
        return self.cm - q

    def get_point(self, q0):
        """Returns the location of q0, taking into account the fact that the
        body rotate. q0 here is the location of the point for teta = 0.
        """
        cm_to_point = self.get_cm_to_point(q0)
        return q0 + cm_to_point - cm_to_point.rotate(self.t)

