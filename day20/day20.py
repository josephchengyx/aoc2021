with open('day20_input.txt', newline='') as f:
    reader = f.read().splitlines()
    line_break = reader.index('')
    img_enhancement_algo = reader[0]
    input_image = reader[line_break+1:]

def copy_arr(arr):
    return [[elem for elem in row] for row in arr]

def empty_arr(x_range, y_range, default):
    return [[default for _ in range(x_range)] for _ in range(y_range)]

def print_arr(arr):
    for row in arr:
        print(row)

def pixel_to_bit(pixel):
    mapping = {'.': 0, '#': 1}
    return mapping[pixel]

def get_width_and_height(img):
    width, height = len(img[0]), len(img)
    return width, height

def enhance_img(input, algo, iters):
    def get_neighbours(x, y):
        return [(x+dx, y+dy) for dy in range(-1, 2) for dx in range(-1, 2)]

    def get_pixel(x, y):
        if 0 <= x < width and 0 <= y < height:
            return img[y][x]
        else:
            return default_pixel

    def convolve(x, y):
        neighbours = get_neighbours(x, y)
        bitcode = list()
        for px, py in neighbours:
            pixel = get_pixel(px, py)
            digit = pixel_to_bit(pixel)
            bitcode.append(str(digit))
        bitcode = int(''.join(bitcode), 2)
        return algo[bitcode]

    def process_background(default_pixel):
        if default_pixel == '.':
            return algo[0]
        else: # default_pixel == '#'
            return algo[-1]

    img = copy_arr(input)
    width, height = get_width_and_height(img)
    default_pixel = '.'

    for _ in range(iters):
        output = empty_arr(width+2, height+2, '')
        for y in range(-1, height+1):
            for x in range(-1, width+1):
                output[y+1][x+1] = convolve(x, y)
        default_pixel = process_background(default_pixel)
        img = output
        width, height = get_width_and_height(img)

    return [''.join(row) for row in img]

def count_lit_pixels(input_image, img_enhancement_algo, iters):
    output_image = enhance_img(input_image, img_enhancement_algo, iters)
    width, height = get_width_and_height(output_image)
    lit_pixels = 0
    for y in range(height):
        for x in range(width):
            lit_pixels += pixel_to_bit(output_image[y][x])
    return lit_pixels

print(f"Part 1: {count_lit_pixels(input_image, img_enhancement_algo, 2)}")
print(f"Part 2: {count_lit_pixels(input_image, img_enhancement_algo, 50)}")
