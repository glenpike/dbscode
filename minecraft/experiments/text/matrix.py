from math import cos, acos, sin
from numpy import matrix, array, cross, dot, zeros, int8
from numpy.linalg import norm

#http://uk.mathworks.com/help/symbolic/mupad_ref/textorientation.html

#http://gamedev.stackexchange.com/questions/20097/how-to-calculate-a-3x3-rotation-matrix-from-2-direction-vectors

#http://svn.gna.org/svn/relax/tags/1.3.4/maths_fns/rotation_matrix.py
def R_2vect(R, vector_orig, vector_fin):
    """Calculate the rotation matrix required to rotate from one vector to another.

    For the rotation of one vector to another, there are an infinit series of rotation matrices
    possible.  Due to axially symmetry, the rotation axis can be any vector lying in the symmetry
    plane between the two vectors.  Hence the axis-angle convention will be used to construct the
    matrix with the rotation axis defined as the cross product of the two vectors.  The rotation
    angle is the arccosine of the dot product of the two unit vectors.

    Given a unit vector parallel to the rotation axis, w = [x, y, z] and the rotation angle a,
    the rotation matrix R is::

              |  1 + (1-cos(a))*(x*x-1)   -z*sin(a)+(1-cos(a))*x*y   y*sin(a)+(1-cos(a))*x*z |
        R  =  |  z*sin(a)+(1-cos(a))*x*y   1 + (1-cos(a))*(y*y-1)   -x*sin(a)+(1-cos(a))*y*z |
              | -y*sin(a)+(1-cos(a))*x*z   x*sin(a)+(1-cos(a))*y*z   1 + (1-cos(a))*(z*z-1)  |


    @param R:           The 3x3 rotation matrix to update.
    @type R:            3x3 numpy array
    @param vector_orig: The unrotated vector defined in the reference frame.
    @type vector_orig:  numpy array, len 3
    @param vector_fin:  The rotated vector defined in the reference frame.
    @type vector_fin:   numpy array, len 3
    """

    # Convert the vectors to unit vectors.
    vector_orig = vector_orig / norm(vector_orig)
    vector_fin = vector_fin / norm(vector_fin)

    # The rotation axis (normalised).
    axis = cross(vector_orig, vector_fin)
    axis_len = norm(axis)
    if axis_len != 0.0:
        axis = axis / axis_len

    # Alias the axis coordinates.
    x = axis[0]
    y = axis[1]
    z = axis[2]

    print "axis ", axis

    # The rotation angle.
    angle = acos(dot(vector_orig, vector_fin))

    # Trig functions (only need to do this maths once!).
    ca = cos(angle)
    sa = sin(angle)

    # Calculate the rotation matrix elements.
    R[0,0] = 1.0 + (1.0 - ca)*(x**2 - 1.0)
    R[0,1] = -z*sa + (1.0 - ca)*x*y
    R[0,2] = y*sa + (1.0 - ca)*x*z
    R[1,0] = z*sa+(1.0 - ca)*x*y
    R[1,1] = 1.0 + (1.0 - ca)*(y**2 - 1.0)
    R[1,2] = -x*sa+(1.0 - ca)*y*z
    R[2,0] = -y*sa+(1.0 - ca)*x*z
    R[2,1] = x*sa+(1.0 - ca)*y*z
    R[2,2] = 1.0 + (1.0 - ca)*(z**2 - 1.0)


"""
    pretending we have text that has a default horizontal direction (
    the plane in which the letters follow each other) and a default
    vertical direction (the plane in which the letters go from top-to-bottom)
    defaultH & defaultV respectively

    We want to work out what the rotation matrices will be if we change
    the direction(s) in which text is printed
    newH & newV respectively.

    the resulting rotation matrices are rotH & rotV
"""


def rotateBy(h, v):
    defaultH = array([1, 0, 0], int)
    defaultV =  array([0, -1, 0], int)


    newH = array(h, int)
    newV =  array(v, int)

    rotH = zeros(shape=(3,3), dtype=int8)
    rotV = zeros(shape=(3,3), dtype=int8)

    #Could this be optimised if we know we"re only ever rotating
    #90degrees in any direction?
    R_2vect(rotH, defaultH, newH);
    R_2vect(rotV, defaultV, newV);

    print "rotH\n", rotH, "\nrotV\n", rotV
    equal = (rotH == rotV).all()

    print "Rotation matrices are same? ", equal

    pos = array([4, 3, 0], int)
    pos2 = array([5, 3, 0], int)

    if equal == False:
        print "Rotate pos by H, then V ", rotV.dot(rotH.dot(pos))
        print "Rotate pos2 by H, then V ", rotV.dot(rotH.dot(pos2))
    else:
        print "Rotate pos by H ", rotH.dot(pos)

        print "Rotate pos2 by H ", rotH.dot(pos2)


if __name__ == '__main__':

    print "rotate 90 about Z"
    rotateBy([0, 1, 0], [1, 0, 0])

    print "\nrotate 90 about y"
    rotateBy([0, 0, -1], [0, -1, 0])

    print "\nrotate 90 about y, then 90 about z"
    rotateBy([0, 0, -1],  [-1, 0, 0])
