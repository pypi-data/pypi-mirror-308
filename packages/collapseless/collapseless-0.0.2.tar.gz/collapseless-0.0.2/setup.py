import setuptools #导入setuptools打包工具

"""
cd E:\编程\pypi\collapseless
python setup.py sdist bdist_wheel
python -m twine upload dist/*
"""
#token: pypi-AgEIcHlwaS5vcmcCJGU2ZTU0YTBhLWZiZDMtNDJkMi1hODA3LTM4NzgxOTQ4NGUxYwACKlszLCJlZjZkNTZlMi1mMGNlLTQ2ZjMtYWU5NC0yZGM0YjI5NzI5ODAiXQAABiAWePG9uKY1z-USoZigzHCUKqfdXKUqeKtMA1z7qJitlg

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="collapseless", # 用自己的名替换其中的YOUR_USERNAME_
    version="0.0.2",    #包版本号，便于维护版本
    author="Collapseless",    #作者，可以写自己的姓名
    author_email="Collapseless@163.com",    #作者联系方式，可写自己的邮箱地址
    description="",#包的简述
    long_description=long_description,    #包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://github.com/Collapseless",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',    #对python的最低版本要求
)
