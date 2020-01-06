import cv2
import numpy as np
import imageio


path = ''
input_num = 0
output_size = 0
result = np.zeros(())
result_for_csv = np.zeros(())


def init():
    global path, input_num, output_size, result, result_for_csv
    path = './data'
    input_num = 5
    output_size = 250
    result = np.zeros((output_size, output_size, 5))
    result_for_csv = np.zeros((output_size, output_size))
    return


def img_read(img_name):
    img = imageio.mimread(path + img_name)[0]
    # cv2.imshow(img_name, img)
    # cv2.waitKey(0)
    # print(img.shape[0], img.shape[1])
    return img, img.shape[0], img.shape[1]


def cut_image(image, height, width):
    min_x = min_y = 10000
    max_x = max_y = 0
    for i in range(height):
        for j in range(width):
            image_r, image_g, image_b = image[i, j][0], image[i, j][1], image[i, j][2]
            # print(image_r, image_g, image_b)
            if not((image_r == 192 and image_g == 192 and image_b == 192)
                    or (image_r == 0 and image_g == 0 and image_b == 0)):
                if min_x > i:
                    min_x = i
                if min_y > j:
                    min_y = j
                if max_x < i:
                    max_x = i
                if max_y < j:
                    max_y = j
    img = image[min_x:max_x, min_y:max_y, :]
    # cv2.imshow('after cutting', img)
    # cv2.waitKey(0)
    # print(img.shape[0], img.shape[1])
    return img, max_x - min_x, max_y - min_y


def sample_image(image, length, direction):
    sampled_points = np.linspace(0, length-1, num=output_size, dtype=int)
    ratio = length / output_size
    if direction:
        width = image.shape[1]
        sampled_points_another_axis = np.linspace(0, width-1, num=int(width/ratio), dtype=int)
        img = image[:, sampled_points_another_axis, :]
        img = img[sampled_points, :, :]
    else:
        height = image.shape[0]
        sampled_points_another_axis = np.linspace(0, height-1, num=int(height/ratio), dtype=int)
        img = image[:, sampled_points, :]
        img = img[sampled_points_another_axis, :, :]
    # cv2.imshow('after sampling', img)
    # cv2.waitKey(0)
    # print(img.shape[0], img.shape[1])
    return img, img.shape[0], img.shape[1]


def show_result(result):
    img = np.zeros((output_size, output_size, 4))
    for i in range(output_size):
        for j in range(output_size):
            if result[i, j, 0] == 1:
                img[i, j, 0] = 200
            if result[i, j, 1] == 1:
                img[i, j, 1] = 200
            if result[i, j, 3] == 1:
                img[i, j, 1] = 200
                img[i, j, 2] = 100
            if result[i, j, 4] == 1:
                img[i, j, 0] = 200
                img[i, j, 2] = 100
            if result[i, j, 2] == 1:
                img[i, j, 2] = 200
    cv2.imshow('result', img)
    cv2.waitKey(0)
    cv2.imwrite('./result/result{}.png'.format(output_size), img)
    return


# def main():
init()
for i in range(input_num):
    print(i)
    img_name = '/{}.gif'.format(i+1)
    img, height, width = img_read(img_name)
    img_backup, height, width = cut_image(img, height, width)
    if output_size < height:
        img_backup, height, width = sample_image(img_backup, height, True)
    if output_size < width:
        img_backup, height, width = sample_image(img_backup, width, False)
    height, width = img_backup.shape[0], img_backup.shape[1]
    bias_vertical, bias_horizontal = int((output_size - height) / 2), int((output_size - width) / 2)

    result_for_csv *= 2

    for j in range(height):
        for k in range(width):
            img_r, img_g, img_b = img_backup[j, k][0], img_backup[j, k][1], img_backup[j, k][2]
            if (img_r == 192 and img_g == 192 and img_b == 192) or (img_r == 0 and img_g == 0 and img_b == 0):
                result[j + bias_vertical, k + bias_horizontal, i] = 0
                # result_for_csv[j + bias_vertical, k + bias_horizontal] *= 2
            else:
                result[j + bias_vertical, k + bias_horizontal, i] = 1
                # result_for_csv[j + bias_vertical, k + bias_horizontal] *= 2
                result_for_csv[j + bias_vertical, k + bias_horizontal] += 1
show_result(result)
np.savetxt('./result/result{}.csv'.format(output_size), result_for_csv, '%d', ',')


# if __name__ == '__main__':
#     init()
#     main()
