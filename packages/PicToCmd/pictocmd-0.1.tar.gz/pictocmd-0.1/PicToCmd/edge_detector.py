# PicToCmd/edge_detector.py
import cv2
import numpy as np

def edge_pic(image_path, resize_factor=0.2, show_image_edge=False):
    """
    检测图像的边缘并返回二值化的边缘图。
    :param image_path: 图像路径
    :param resize_factor: 图像缩放因子
    :param show_image_edge: 是否显示图像边缘
    :return: 二值化的边缘图像
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError(f"无法读取图像文件: {image_path}")

    # 根据缩放因子对图像进行缩放
    height, width = image.shape
    new_width = int(width * resize_factor)
    new_height = int(height * resize_factor)

    resized_image = cv2.resize(image, (new_width, new_height))

    # 对图像进行高斯模糊，去除噪声
    blurred_image = cv2.GaussianBlur(resized_image, (5, 5), 0)

    # 使用 Canny 算法进行边缘检测
    edges = cv2.Canny(blurred_image, threshold1=50, threshold2=150)

    if show_image_edge:
        # 显示边缘图
        cv2.imshow('Original Image', resized_image)
        cv2.imshow('Improved Edge Image', edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return edges

def toCmd(edges):
    """
    将边缘图转化为命令字符数组。
    :param edges: 二值化的边缘图
    :return: 字符命令数组
    """
    height, width = edges.shape
    cmd = np.zeros((height, width), dtype=str)

    # 对每行字符进行处理
    for i in range(height):
        for j in range(width):
            if edges[i][j] > 0:
                cmd[i][j] = '*'
            else:
                cmd[i][j] = ' '

    # 删除全空格的行和列
    cmd_resized = remove_empty_rows_and_columns(cmd)

    return cmd_resized

def remove_empty_rows_and_columns(cmd):
    """
    删除全空格的行和列
    :param cmd: 字符数组
    :return: 删除空白行和列后的字符数组
    """
    cmd = [row for row in cmd if ''.join(row).strip() != '']

    # 转置矩阵，删除全空格的列，再转回来
    cmd_transposed = list(zip(*cmd))
    cmd_transposed = [col for col in cmd_transposed if ''.join(col).strip() != '']
    cmd_resized = list(zip(*cmd_transposed))

    cmd_resized = [''.join(row) for row in cmd_resized]
    return cmd_resized

def saveCmdToFile(cmd, file_path='output.txt', saveByFile=True):
    """
    将字符命令数组保存到文件
    :param cmd: 字符命令数组
    :param file_path: 输出文件路径
    :param saveByFile: 是否保存文件
    """
    if saveByFile:
        with open(file_path, 'w', encoding='utf-8') as f:
            for row in cmd:
                f.write(row + '\n')
                print(row)

def picToCmd(image_path, resize_factor=0.2, outputFilePath='output.txt', saveByFile=True, show_image_edge=False):
    """
    从图片路径生成边缘命令并保存到文件。
    :param image_path: 图像路径
    :param resize_factor: 图像缩放因子
    :param outputFilePath: 输出文件路径
    :param saveByFile: 是否保存文件
    :param show_image_edge: 是否显示图像边缘
    """
    edges = edge_pic(image_path, resize_factor, show_image_edge)
    cmd = toCmd(edges)
    saveCmdToFile(cmd, outputFilePath, saveByFile)
