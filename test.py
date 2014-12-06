from svg.path import parse_path

results = []
with open('tear.svg') as inputfile:
    for line in inputfile:
        results.append(line.strip())

path = results[2].split("=")[1][:-2]
print parse_path(path)