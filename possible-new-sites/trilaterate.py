import numpy
from numpy import sqrt, dot, cross
from numpy.linalg import norm

thargmeter_constant = 871.02

# Find the intersection of three spheres
# P1,P2,P3 are the centers, r1,r2,r3 are the radii
# Implementaton based on Wikipedia Trilateration article.


# source:
# https://stackoverflow.com/questions/1406375/finding-intersection-points-between-3-spheres/1406415
def trilaterate(P1, P2, P3, r1, r2, r3):
    r1 *= thargmeter_constant
    r2 *= thargmeter_constant
    r3 *= thargmeter_constant
    temp1 = P2-P1
    e_x = temp1/norm(temp1)
    temp2 = P3-P1
    i = dot(e_x,temp2)
    temp3 = temp2 - i*e_x
    e_y = temp3/norm(temp3)
    e_z = cross(e_x,e_y)
    d = norm(P2-P1)
    j = dot(e_y,temp2)
    x = (r1*r1 - r2*r2 + d*d) / (2*d)
    y = (r1*r1 - r3*r3 -2*i*x + i*i + j*j) / (2*j)
    temp4 = r1*r1 - x*x - y*y
    if temp4<0:
        raise Exception("The three spheres do not intersect!");
    z = sqrt(temp4)
    p_12_a = P1 + x*e_x + y*e_y + z*e_z
    p_12_b = P1 + x*e_x + y*e_y - z*e_z
    return p_12_a, p_12_b

if __name__ == '__main__':
    center_merope = numpy.array([-78.59375, -149.625, -340.53125])
    # Col 70 Sector FY-N C21-3
    center_col70 = numpy.array([687.0625, -362.53125, -697.0625])
    # Mel 22 Sector NX-U d2-31
    center_origin = numpy.array([-64.40625, -269.5625, -373.59375])

    # distances = [0.151 * thargmeter_constant, 0.01 * thargmeter_constant, 0.937 * thargmeter_constant]
    # distances = [0.01 * thargmeter_constant, 0.151 * thargmeter_constant, 0.937 * thargmeter_constant]
    # distances = [0.01 * thargmeter_constant, 0.937 * thargmeter_constant, 0.151 * thargmeter_constant]
    distances = [0.151 * thargmeter_constant, 0.937 * thargmeter_constant, 0.01 * thargmeter_constant]
    answer = trilaterate(center_merope, center_col70, center_origin, distances[0], distances[1], distances[2])
    print(answer[1])
    # should be close to: [ -57.1, -274.7, -373.7 ]