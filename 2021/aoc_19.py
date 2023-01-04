import numpy as np

from utils import matvec, padd, pneg

with open('aoc_19_data') as f:
    data = f.readlines()

data = [row.replace('\n', '') for row in data]
solution = "improved"  # "original", "improved"

# Process data to 3d np array per scanner:
scanners = {}
curr_scanner = -1
curr_data = []
for row in data:
    if row.startswith('---'):
        curr_scanner = int(row.replace('--- scanner ', '').replace(' ---', ''))
        curr_data = []
    elif row == '':
        curr_data = [[int(x) for x in row.split(',')] for row in curr_data]
        scanners.update({curr_scanner: np.array(curr_data)})
    else:
        curr_data.append(row)

remaps = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
negatives = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1), (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1)]


# All rotations of a scan (some overlap after doing both remapping and taking negatives)
def rotate(remap, negation, scan):
    ret = []
    for item in scan:
        ret.append([negation[0] * item[remap[0]], negation[1] * item[remap[1]], negation[2] * item[remap[2]]])
    return np.array(ret)


# For a pair of scanners, find if they can match, and if so, return the observations from input 1 in the system of 2
def compare_scanners_orig(this_scanner_f, ref_scanner_f):
    for remap in remaps:
        for negation in negatives:
            iter_scanner = rotate(remap, negation, this_scanner_f)
            for pt_ref in ref_scanner_f:
                for pt_iter in iter_scanner:
                    diff_if_same = np.array([pt_iter[0] - pt_ref[0], pt_iter[1] - pt_ref[1], pt_iter[2] - pt_ref[2]])
                    matches = 0
                    shifted_points = []
                    for other_pt_iter in iter_scanner:
                        shifted_point = other_pt_iter - diff_if_same
                        matches = matches + 1 if list(shifted_point) in ref_scanner_f.tolist() else matches
                        shifted_points.append(shifted_point)
                    if matches >= 12:
                        scan_coords.append(diff_if_same)
                        return True, np.array(shifted_points)
    return False, None


FACINGS = [x for i in [-1, 1] for x in [[i, 0, 0], [0, i, 0], [0, 0, i]]]


def cross(a, b):
    c = [a[1] * b[2] - a[2] * b[1],
         a[2] * b[0] - a[0] * b[2],
         a[0] * b[1] - a[1] * b[0]]

    return c


def compare_scanners_better(a, b):
    aset = set(map(tuple, a))
    # return b's points, but now relative to a
    for facing in FACINGS:
        for up in [f for f in FACINGS if all(abs(x) != abs(y) for x, y in zip(f, facing) if x or y)]:

            # facing's
            right = cross(facing, up)

            matrix = [facing, up, right]
            new_b = [matvec(matrix, vec) for vec in b]

            for a_point in a:
                for b_point in new_b:
                    # assume they're the same
                    # add a-b to all b
                    delta = padd(a_point, pneg(b_point))
                    new_new_b = [padd(delta, b) for b in new_b]
                    if len(aset.intersection(map(tuple, new_new_b))) >= 12:
                        return new_new_b, delta
    return None


def compare_scanners(this_scanner_f, ref_scanner_f):
    if solution == "original":
        return compare_scanners_orig(this_scanner_f, ref_scanner_f)
    else:
        result = compare_scanners_better(ref_scanner_f, this_scanner_f)
        if result is None:
            return False, None
        else:
            scan_coords.append(np.array(result[1]))
            return True, np.array(result[0])


# Setting up input: at first, none are matched, scanner[0] is "known universe", and is taken as reference point.
matched = {x: False for x in scanners.keys() if x != 0}
ref_scanner = scanners[0]
scan_coords = [np.array((0, 0, 0))]

# Loop over all scanners>0, and compare against known universe (first just sc0). If match, expand universe.
# Continue until all are matched
while not all(matched.values()):
    for scanner_key in matched.keys():
        if not matched[scanner_key]:
            this_scanner = scanners[scanner_key]
            print(f"Comparing scanner {scanner_key} against known universe..")
            success, shifted = compare_scanners(this_scanner, ref_scanner)
            if success:
                matched[scanner_key] = True
                ref_scanner = np.unique(np.concatenate([ref_scanner, shifted]), axis=0)
                print(f"  Found scanner {scanner_key}! Adding to universe. Current number of unique beacons: "
                      f"{ref_scanner.shape[0]}.")
        else:
            print(f"Scanner {scanner_key} already part of universe, skipping..")

print(f"\n\nNumber of unique beacons: {ref_scanner.shape[0]}")

distances = []
for s_this in scan_coords:
    for s_other in scan_coords:
        distances.append(np.sum(np.abs(s_this - s_other)))
print(f"Maximum Manhattan distance: {max(distances)}")
