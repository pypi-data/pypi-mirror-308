# coding utf8
import setuptools
from yxtree.versions import get_versions

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="yxtree",
    version=get_versions(),
    author="Yuxing Xu",
    author_email="xuyuxing@mail.kib.ac.cn",
    description="Here's an example of a repository",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://github.com/SouthernCD/yxtree",
    include_package_data = True,

    entry_points={
        "console_scripts": ["yxtree = yxtree.cli:main"]
    },    

    packages=setuptools.find_packages(),

    install_requires=[
        "yxutil",
        "yxmath>=0.0.5",
        "matplotlib>=3.5.0",
        "networkx>=2.4",
        "biopython<=1.80",
        "numpy>=1.18.1",
    ],

    python_requires='>=3.5',
)