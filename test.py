import svg.path
from itertools import chain
from svg.path import parse_path
from xml.dom import minidom
from Tkinter import *
import numpy as np
import csv
import os

def get_coords_from_shape(curve, n_pts=1000):
    pts = np.linspace(0,1,n_pts)
    coords = [ (curve.point(x).real, curve.point(x).imag) for x in pts]
    #print coords
    return coords

master = Tk()

SCALE_FACTOR = 100
PADDING = 0.10          # Add much padding to the edges of the 1x1 image

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
    n_pts = 100
    all_coords = []
    svg_image = minidom.parse(svg_path)
    path_strings = [path.getAttribute('d') for path in svg_image.getElementsByTagName('path')]
    for i in range(len(path_strings)):
        path_strings[i] = parse_path(str(path_strings[i]))
    svg_image.unlink()

    for current_path in path_strings:
        for element in current_path:
            all_coords.append(get_coords_from_shape(element))

    return all_coords


def maprange( a, b, s):
    (a1, a2), (b1, b2) = a, b
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def get_dimensions(path):
    all_coords_flat = list(chain.from_iterable(chain.from_iterable(path))) # flatten the list
    if len(all_coords_flat)<1:
        raise Exception("empty file")
    odd_indices = range(0,len(all_coords_flat),2) 
    even_indices = range(1,len(all_coords_flat),2) 
    xcoords = [all_coords_flat[i] for i in odd_indices] # odds only
    ycoords = [all_coords_flat[i] for i in even_indices] # evens only
    return min(xcoords), min(ycoords), max(xcoords), max(ycoords)

def normalize_path(path):
    """ Normalize the image size to 1x1 """
    x_min, y_min, x_max, y_max = get_dimensions(path);
    max_dimension = max(x_max-x_min, y_max-y_min)
    for i in range(len(path)):
        segment = path[i]
        for j in range(len(segment)):
            # scale the image down, but add some padding so that two edges aren't cut off
            path[i][j] = ((path[i][j][0]-x_min)/max_dimension + PADDING, (path[i][j][1]-y_min)/max_dimension + PADDING)
    return path

def scale_path(path, scale_factor):
    """ Scale the image with fixed aspect ratio """
    for i in range(len(path)):
        segment = path[i]
        for j in range(len(segment)):
            path[i][j] = (scale_factor*path[i][j][0], scale_factor*path[i][j][1])
    return path

def draw_path(coords, height, width):
    w = Canvas(master, width=width, height=height)
    w.pack()
    for line in coords:
        for i in range(len(line)-1):
            w.create_line(line[i], line[i+1])
    mainloop()

def output_csv(coords):
    csvfile = open('coords_out.csv','wb')
    outfile = csv.writer(csvfile,delimiter=',')
    # move to (0,0) first
    outfile.writerow([0,0,'off'])
    for i in coords:
        ct = 0
        for j in i:
            if ct == 0:
                outfile.writerow([j[0],j[1],0])
                ct = ct + 1
            else:
                outfile.writerow([j[0],j[1],1])
                ct = ct + 1
    # append an 'off' at the end to move to (0,0)
    outfile.writerow([0,0,'off'])
    csvfile.close()

def main():
    path = get_path_from_svg('officeworker2.svg')
    print "Path is : ", path
    
    path = normalize_path(path)
    path = scale_path(path, SCALE_FACTOR)
    height = SCALE_FACTOR*(1+2*PADDING)
    width = height
    draw_path(path, height, width)
    output_csv(path)

if __name__ == "__main__":
    main()