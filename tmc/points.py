from inspect import isclass, isfunction, getmembers
import pdb
import atexit

point_register = {'suite': {}, 'test': {}}


def qualifier(test):
    return "%s.%s" % (test.__module__, test.__qualname__)


def save_points(o, points, dst):
    q = qualifier(o)
    if q not in dst:
        dst[q] = []
    for point in points:
        if point not in dst[q]:
            dst[q].append(point)


def points(*points):

    def points_wrapper(o):
        if isclass(o):
            save_points(o, points, point_register['suite'])
        elif isfunction(o):
            # pdb.set_trace()
            save_points(o, points, point_register['test'])
        else:
            raise Exception("Expected decorator object '%s' type to be Class or Function but was %s." % (o, type(o)))
        return o

    if not points:
        raise Exception("You need to define at least one point in the points decorator declaration")
    for point in points:
        if type(point) is not str:
            raise Exception("Points decorator argument '%s' needs to be a string, but was %s." % (point, type(point).__name__))
    return points_wrapper


@atexit.register
def write_points():
    f = open("tmc_available_points.txt", "w")
    for register in point_register:
        for qualifier, points in point_register[register].items():
            f.write("[%s] [%s] %s\n" % (register, qualifier, " ".join(points)))
    f.close()
