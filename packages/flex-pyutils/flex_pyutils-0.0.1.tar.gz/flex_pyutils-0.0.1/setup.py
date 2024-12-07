from setuptools import setup, find_packages
import os

setup(
    name="flex-pyutils", # 包名称
    version="0.0.1", # 包版本
    author="江浩",  # 作者
    author_email="jh.vip.1024@gmail.com", # 作者邮箱
    description="常用开发工具箱",
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="UTF8").read(),
    packages=find_packages(),

    # 表明当前模块依赖哪些包，若环境中没有，则会从pypi中下载安装
    install_requires=['numpy'],

    # 仅在测试时需要使用的依赖，在正常发布的代码中是没有用的。
    # 在执行python setup.py test时，可以自动安装这三个库，确保测试的正常运行。
    # tests_require=[
    #     'pytest>=3.3.1',
    # ],

    #keywords=['python', 'moviepy', 'cut video'],
    #data_files=[('cut_video', ['cut_video/clip_to_erase.json'])],

    # 用来支持自动生成脚本，安装后会自动生成 /usr/bin/foo 的可执行文件
    # 该文件入口指向 foo/main.py 的main 函数
    # entry_points={
    #     'console_scripts': [
    #         'cut_video = cut_video.main:main'
    #     ]
    # },
    # 将 bin/foo.sh 和 bar.py 脚本，生成到系统 PATH中
    # 执行 python setup.py install 后
    # 会生成 如 /usr/bin/foo.sh 和 如 /usr/bin/bar.py
    # scripts=['cut_video/cut_video.py'],

    license="MIT",
    url="https://g-fxqk2467.coding.net/p/saas-flex/d/pyutils/git/tree/master", #程序官方地址
    classifiers=[
        # 发展时期,常见的如下
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # 开发的目标用户
        "Intended Audience :: Developers",
        # 目标 Python 版本
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ],
    python_requires='>=3.6',
)