example_data = False

if example_data:
    area = [[20, 30], [-10, -5]]
else:
    area = [[241, 273], [-97, -63]]

max_steps = 30
# Must be positive, can't overshoot, and pos vertical velocity = negative vertical velocity when back at y=0.
velocity_start_bounds = [[0, area[0][1]+1], [area[1][0], -area[1][0]+1]]


def check_location(position, area):
    return (area[0][0] <= position[0] <= area[0][1]) and (area[1][0] <= position[1] <= area[1][1])


def check_velocity(velocity, area):
    position = [0, 0]
    high = 0
    in_area = False
    while velocity[0] != 0 or position[1] > area[1][0]:
        position[0] += velocity[0]
        position[1] += velocity[1]
        velocity[0] = velocity[0] - 1 if velocity[0] > 0 else (velocity[0] + 1 if velocity[0] < 0 else 0)
        velocity[1] -= 1
        high = position[1] if position[1] > high else high
        # print(check_location(position, area))
        in_area = True if in_area or check_location(position, area) else False

    return in_area, high


results = {}
max_result = 0
count_checked = 0
max_index = None
for x in range(velocity_start_bounds[0][0], velocity_start_bounds[0][1]):
    for y in range(velocity_start_bounds[1][0], velocity_start_bounds[1][1]):
        check_iter, result_iter = check_velocity([x, y], area)
        count_checked += check_iter
        if result_iter > max_result and check_iter:
            max_result = result_iter
            max_index = (x, y)
        results.update({f"{x},{y}": (check_iter, result_iter)})

print(f"Max found for {max_index} at {max_result}")
print(f"In total, {count_checked} are OK")
