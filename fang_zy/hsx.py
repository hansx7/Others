import cv2
import numpy as np
import imageio


def init():
    global path, input_num, output_size, result, result_for_csv
    path = './data'
    input_num = 5
    output_size = 1000
    result = np.zeros((output_size, output_size, 5))
    result_for_csv = np.zeros((output_size, output_size))
    return


def img_read(img_name):
    img = imageio.mimread(path + img_name)[0]
    # cv2.imshow(img_name, img)
    # cv2.waitKey(0)
    return img, img.shape[0], img.shape[1]


def show_result(result):
    img = np.zeros((output_size, output_size, 4))
    for i in range(output_size):
        for j in range(output_size):
            if result[i, j, 0] == 1:
                img[i, j, 0] = 200
            if result[i, j, 1] == 1:
                img[i, j, 1] = 200
            if result[i, j, 2] == 1:
                img[i, j, 2] = 200
            if result[i, j, 3] == 1:
                img[i, j, 1] = 200
                img[i, j, 2] = 100
            if result[i, j, 4] == 1:
                img[i, j, 0] = 200
                img[i, j, 2] = 100
    cv2.imshow('result', img)
    cv2.waitKey(0)


def main():
    for i in range(input_num):
        img_name = '/{}.gif'.format(i+1)
        img, height, width = img_read(img_name)
        bias_vertical, bias_horizontal = int((output_size - height) / 2), int((output_size - width) / 2)
        # print(height, width)
        img_backup = img.copy()
        min_x = min_y = 10000
        max_x = max_y = 0
        # print(img_backup.shape)
        for j in range(height):
            for k in range(width):
                img_r, img_g, img_b = img_backup[j, k][0], img_backup[j, k][1], img_backup[j, k][2]
                if img_r == 192 and img_g == 192 and img_b == 192:
                    result[j + bias_vertical, k + bias_horizontal, i] = 0
                    result_for_csv[j + bias_vertical, k + bias_horizontal] *= 2
                else:
                    if min_x > j:
                        min_x = j
                    if min_y > k:
                        min_y = k
                    if max_x < j:
                        max_x = j
                    if max_y < k:
                        max_y = k
                    result[j + bias_vertical, k + bias_horizontal, i] = 1
                    result_for_csv[j + bias_vertical, k + bias_horizontal] *= 2
                    result_for_csv[j + bias_vertical, k + bias_horizontal] += 1
        print(min_x, min_y, max_x, max_y)
    show_result(result)
    np.savetxt('result.csv', result_for_csv, '%d', ',')


if __name__ == '__main__':
    init()
    main()
