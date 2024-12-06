from setuptools import setup, find_packages

setup(
    name="dh_test_package_cli",  # Name of your package
    version="0.1.1",  # Initial version
    author="sample name",
    author_email="ds2000434@protonmail.ch",
    description="A short description of the package",
    long_description="cli",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",  # Project URL
    packages=find_packages(),  # Automatically finds `my_package` and other sub-packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
    install_requires=[  # List of dependencies
        # e.g., "requests", "numpy"
    ],
)

