import numpy as np

with open('aoc_20_data') as f:
    data = f.readlines()

data = [row.replace('\n', '') for row in data]

nr_enhancements = 50

# Convert data to list/arrays
algorithm = [int(x.replace("#", "1").replace(".", "0")) for x in data[0]]
curr_image = np.array([[int(x.replace("#", "1").replace(".", "0")) for x in row] for row in data[2:]])


def pad_image(image, pad_dim=2, even=False):
    # Make an array of 0s around the image

    dims = image.shape
    if even:
        image = np.concatenate([np.zeros([pad_dim, dims[1] + 2 * pad_dim]),
                                np.concatenate([np.zeros([dims[0], pad_dim]), image, np.zeros([dims[0], pad_dim])], axis=1),
                                np.zeros([pad_dim, dims[1] + 2 * pad_dim])])
    else:
        image = np.concatenate([np.ones([pad_dim, dims[1] + 2 * pad_dim]),
                                np.concatenate([np.ones([dims[0], pad_dim]), image, np.ones([dims[0], pad_dim])], axis=1),
                                np.ones([pad_dim, dims[1] + 2 * pad_dim])])
    return image, not even


def apply_algorithm(image, even=False):
    if even:
        output_image = np.zeros_like(image)
    else:
        output_image = np.ones_like(image)
    for i in range(1, image.shape[0] - 1):
        for j in range(1, image.shape[1] - 1):
            subimage = image[i - 1:i + 2, j - 1:j + 2]
            number = int("".join(str(int(x)) for x in np.concatenate(subimage)), 2)
            output_image[i, j] = algorithm[number]

    return output_image

iseven = True
# For odd iterations, it is actually infinite.
for _iter in range(nr_enhancements):
    print(f"After {_iter} iterations: {int(np.sum(curr_image))}")
    [curr_image, iseven] = pad_image(curr_image, even=iseven)
    curr_image = apply_algorithm(curr_image, even=iseven)


print(int(np.sum(curr_image)))
