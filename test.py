import svg.path
from svg.path import parse_path

def cubic_benzier(curve, step):
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

def main():
	step = 0.1

	results = []
	with open('tear.svg') as inputfile:
	    for line in inputfile:
	        results.append(line.strip())

	path = results[2].split("=")[1][:-2]
	parsed_path = parse_path(path)

	for element in parsed_path:
		if type(element) is svg.path.path.CubicBezier:
			print cubic_benzier(element, step)
		if type(element) is svg.path.path.Line:
			print 'found'

if __name__ == "__main__":
    main()