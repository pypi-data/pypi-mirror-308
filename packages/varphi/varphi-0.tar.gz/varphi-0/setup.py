from setuptools import setup, find_packages

setup(
    name="varphi",
    version="0",
    description="Compiler and tools for the Varphi Programming Language.",
    author="Hassan El-Sheikha",
    author_email="hassan.elsheikha@utoronto.ca",
    packages=find_packages(),
    install_requires=[
        "varphi_parsing_tools",
        "varphi_compiler"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.12',  # Specify the required Python version
)

