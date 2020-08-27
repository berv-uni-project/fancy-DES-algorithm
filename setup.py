import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="fancyDES",
    version="0.1.0",
    author="Bervianto Leo Pratama",
    author_email="bervianto.leo@gmail.com",
    description="DES Custom with Fancy Algorithm",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/berv-uni-project/fancy-DES-algorithm",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
