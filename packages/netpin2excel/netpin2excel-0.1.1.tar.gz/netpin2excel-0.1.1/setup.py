from setuptools import setup, find_packages
import os

# # 读取README文件作为项目说明
# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setup(
    name="netpin2excel",                # 替换为你的包名
    version="0.1.1",                  # 版本号
    author="hfh",               # 作者信息
    author_email="your.email@example.com",
    description="A sample Python package with a .pyd file",
    url="https://github.com/yourusername/my_package",  # 项目主页
    packages=find_packages(),         # 自动查找包
    include_package_data=True,        # 包含所有文件，包括 .pyd 文件
    # package_data={
    #     "my_package": ["netpin_process.pyd"],      # 指定包含 .pyd 文件
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",          # Python 版本要求
    install_requires=[],              # 依赖项，可根据需要添加
)
