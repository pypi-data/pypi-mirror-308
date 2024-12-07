from setuptools import setup, find_packages

setup(
    name="CCFToolkit",  # 模块名称
    version="1.0.0",  # 版本号
    author="Ma Chenxing",  # 作者姓名
    author_email="tammcx@gmail.com",  # 作者邮箱
    description="A toolkit for reading and generating Paintman CCF files for color chart management.",  # 简短描述
    long_description=open("README.md", "r", encoding="utf-8").read(),  # 读取 README 作为长描述
    long_description_content_type="text/markdown",  # 长描述的格式
    url="https://github.com/ChenxingM/CCFToolkit",  # 项目主页（如 GitHub 仓库）
    packages=find_packages(),  # 自动查找所有包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 支持的 Python 版本
)
