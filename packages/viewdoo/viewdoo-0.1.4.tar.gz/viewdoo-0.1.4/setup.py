from setuptools import setup, find_packages

setup(
    name="viewdoo",
    version="0.1.4",
    author="Zachery Morton Colbert",
    author_email="zachery.colbert@health.qld.gov.au",
    description="Medical Image Viewing and Conversion Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/humunumuh/viewdoo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "matplotlib",
        "numpy",
        "pydicom",
        "opencv-python",
        "rt-utils",
        "scipy",
        "customtkinter",
        "nibabel",
        "pynrrd",
        "Pillow",
        "SimpleITK"
    ],
    include_package_data=True,
)
