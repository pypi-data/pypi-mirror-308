from setuptools import setup, find_packages

setup(
    name="hurley_generic_plot",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "seaborn",
        "matplotlib",
        "numpy",
        "scipy",
        "pandas"
    ],
    author="Hurley Li",
    author_email="lihe.oscar@gmail.com",
    description="A Python package for creating clinical trial plots.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hurleyLi/generic-plot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 

