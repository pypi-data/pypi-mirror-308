from setuptools import setup, find_packages

# 通过长描述解释库的功能
long_description = """
PicToCmd 是一个图像处理和 ASCII 艺术生成库。它允许用户通过边缘检测算法将图像转换为字符命令，
并能将结果保存为文本文件。通过该库，你可以方便地将图像转换成简单的字符画，适用于图像分析、艺术创作等领域。
"""

setup(
    name="PicToCmd",  # 库名称
    version="0.1",  # 当前版本号
    packages=find_packages(),  # 自动发现所有包
    description="A Python library to convert images to ASCII art using edge detection.",
    long_description=long_description,  # 包的详细描述
    long_description_content_type="text/markdown",  # 长描述格式
    url="https://github.com/486lv/PicToCmd",  # 替换为你的GitHub链接
    author="486lv",  # 作者名称
    author_email="2876587146@qq.com",  # 作者电子邮件
    classifiers=[  # 用于在 PyPI 中分类
        "Programming Language :: Python :: 3",  # Python 3支持
        "License :: OSI Approved :: MIT License",  # 许可证
        "Operating System :: OS Independent",  # 操作系统支持
        "Intended Audience :: Developers",  # 面向开发者
        "Intended Audience :: End Users/Desktop",  # 面向终端用户
    ],
    keywords="ASCII, art, image, edge detection, PicToCmd",  # 关键词，帮助搜索
    install_requires=[  # 必须的依赖
        'opencv-python>=4.5.0',  # OpenCV 版本要求
        'numpy>=1.21.0',  # Numpy 版本要求
    ],
    python_requires='>=3.6',  # Python 版本要求
    entry_points={  # 可选：允许创建命令行工具
        'console_scripts': [
            'PicToCmd=PicToCmd.edge_detector:picToCmd',  # 创建命令行工具
        ],
    },
    include_package_data=True,  # 包括非Python文件（如数据文件、图像等）
    zip_safe=False,  # 不将包打包成 zip
)
