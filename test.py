import svg.path
from svg.path import parse_path
from xml.dom import minidom
from Tkinter import *

master = Tk()
width = 700
height = 700


def get_cubic_benzier(curve, step):
    coords = []
    p0 = curve.start
    p1 = curve.control1
    p2 = curve.control2
    p3 = curve.end
    t = 0
    while t <= 1:
        bx = ((1-t)**3)*p0.real+3*((1-t)**2)*t*p1.real+3*((1-t)**2)*p2.real+(t**3)*p3.real
        by = ((1-t)**3)*p0.imag+3*((1-t)**2)*t*p1.imag+3*((1-t)**2)*p2.imag+(t**3)*p3.imag
        coords.append((bx, by))
        t+=step
    return coords


def get_line(line, step):
    return [(line.start.real, line.start.imag),(line.end.real, line.end.imag)]


def get_path_from_svg(svg_path):
    step = 0.1
    all_coords = []
    svg_image = minidom.parse(svg_path)
    path_strings = [path.getAttribute('d') for path in svg_image.getElementsByTagName('path')]
    for i in range(len(path_strings)):
        path_strings[i] = parse_path(str(path_strings[i]))
    svg_image.unlink()

    for current_path in path_strings:
        for element in current_path:
            if type(element) is svg.path.path.CubicBezier:
                # all_coords.append(get_cubic_benzier(element, step))
                pass
            if type(element) is svg.path.path.Line:
                all_coords.append(get_line(element, step))
    return all_coords


def maprange( a, b, s):
    (a1, a2), (b1, b2) = a, b
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


def normalize_path(path, height, width):
    # TODO scale to dimension
    return path


def draw_path(coords, height, width):
    w = Canvas(master, width=width, height=height)
    w.pack()
    for line in coords:
        for i in range(len(line)-1):
            w.create_line(line[i], line[i+1])
    mainloop()


def main():
    path = get_path_from_svg('house.svg')
    path = normalize_path(path, height, width)
    print "Path is : ", path
    draw_path(path, height, width)


if __name__ == "__main__":
    main()