import noise


def make_noise_map(x, y, size, scale=1, base=1.0):
    max_noise = float('-inf')
    min_noise = float('inf')
    octaves = 6
    persistance = 0.5
    lacunarity = 2
    height_map = dict()
    base = base
    for j in range(x, x + size):
        for k in range(y, y + size):
            noise_value = noise.snoise2(j / scale,
                                        k / scale,
                                        octaves=octaves,
                                        persistence=persistance,
                                        lacunarity=lacunarity,
                                        base=base)

            if noise_value > max_noise:
                max_noise = noise_value
            elif noise_value < min_noise:
                min_noise = noise_value
            height_map[(j, k)] = noise_value

    return height_map, max_noise, min_noise
