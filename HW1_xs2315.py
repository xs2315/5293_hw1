# coding: utf-8

import numpy as np
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans


def rgb2lab(rgb):
    """this function copy from stackoverflow, convert rgb to lab
    https://stackoverflow.com/questions/13405956/convert-an-image-rgb-lab-with-python
    """
    RGB = []

    for b in rgb:
        value = float(b) / 255

        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        RGB.append(value * 100)

    XYZ = [0, 0, 0]

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    XYZ[0] = float(XYZ[0]) / 95.047  # ref_X =  95.047   Observer= 2°, Illuminant= D65
    XYZ[1] = float(XYZ[1]) / 100.0  # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883  # ref_Z = 108.883

    num = 0
    for value in XYZ:

        if value > 0.008856:
            value = value ** (1/3)
        else:
            value = (7.787 * value) + (16 / 116)

        XYZ[num] = value
        num = num + 1

    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])

    return [round(L, 4), round(a, 4), round(b, 4)]


def read_img(file_path):
    with open(file_path, 'rb') as f:
        data = []
        img = Image.open(f)  # read picture from file object
        m, n = img.size  # return row and col of image

        for i in range(m):
            for j in range(n):
                r, g, b = img.getpixel((i, j))
                lab = rgb2lab([r, g, b])
                data.append(lab)
        # read color info of every pixel and convert to lab
    return np.mat(data), m, n


def make_img(data, kn):
    """make image by color category"""
    data = data.reshape([row, col])
    res = []
    pic_new = Image.new("L", (row, col))
    for i in range(row):  # convert to gray scale image
        for j in range(col):
            pic_new.putpixel((i, j), int(256 / (data[i][j] + 1)))
    pic_new.save("part_all.jpg", "JPEG")
    for n in range(kn):  # make black and white image of each category
        rn = [[0 for i in range(col)] for j in range(row)]
        pic_new = Image.new("L", (row, col))
        for i in range(row):
            for j in range(col):
                category = data[i][j]
                if category == n:
                    pic_new.putpixel((i, j), 0)  # if current pixel belong current category, then set 0
                else:
                    pic_new.putpixel((i, j), 255) # if current pixel do not  belong current category, then set 255
                rn[i][j] = category == n
        res.append(rn)  # prepare data from next step
        pic_new.save("part_%s.jpg" % n, "JPEG")
    return res


def check_face(kn, imgs, row, col):
    """find face area"""
    check_box = (100, 75)  # set check box size
    cy, cx = check_box
    res = []
    con = False
    for seq in range(kn):   # read every category
        con = False
        for i in range(row - cx):
            for j in range(col - cy):
                count = 0
                for x in range(cx):
                    for y in range(cy):
                        if imgs[seq][i + x][j + y]:
                            count += 1
                if 0.84 < count / (cx * cy) < 0.95:     # calculate percent of black points
                    best_rate = count / (cx * cy)
                    z = 0
                    for z in range(1, 50):   # move check box to find best coverage
                        count = 0
                        for x in range(cx):
                            for y in range(cy):
                                if imgs[seq][i + x + z][j + y]:
                                    count += 1
                        current_rate = count/(cx*cy)
                        # print(current_rate)
                        if current_rate > best_rate:
                            best_rate = current_rate
                        else:
                            break
                    # print(seq, i, j, count / (cx * cy), z)
                    res.append([i + z, j, imgs[seq]])  # save check box top left
                    con = True
                if con:
                    break
            if con:
                break

    res2 = []
    for pair in res:
        if pair[0] != 0 and pair[1] != 0:
            res2.append(pair)
    pair = min(res2, key=lambda x: x[1])  # find most possible area
    generate_result(source_file_name, pair[0], pair[1], cx, cy, pair[2])


def generate_result(source_file, i, j, cx, cy, data):
    """draw face box"""
    with open(source_file, 'rb') as f:
        img = Image.open(f)
        m, n = img.size
        for x in range(m):
            for y in range(n):
                if not data[x][y]:
                    img.putpixel((x, y), (0, 0, 0))
        p = 15 # padding
        draw = ImageDraw.Draw(img)  # draw rectangle
        draw.line([(i-p, j-p), (i-p, j + cy + p)], fill='red', width=3)
        draw.line([(i-p, j-p), (i + cx + p, j - p)], fill='red', width=3)
        draw.line([(i + cx + p, j - p), (i + cx + p, j + cy + p)], fill='red', width=3)
        draw.line([(i - p, j + cy + p), (i + cx + p, j + cy + p)], fill='red', width=3)
        img.save("%s_%sresult.jpg" % (i, j), "JPEG")


n_clusters = 4 # set cluster number
source_file_name = "1.jpg"  # source file
img_data, row, col = read_img(source_file_name)  # read image content
result = KMeans(n_clusters=n_clusters).fit_predict(img_data)  # do k-means
imgs = make_img(result, n_clusters)  # separate every category
check_face(n_clusters, imgs, row, col)  # find face