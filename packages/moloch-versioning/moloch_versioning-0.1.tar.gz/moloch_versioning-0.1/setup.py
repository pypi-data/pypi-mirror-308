from setuptools import setup, find_packages

setup(
    name="moloch_versioning",
    version="0.1",
    description="Automated version control system with customizable changelog and version management",
    author="Jorge Mieres",
    author_email="jamieres@gmail.com",
    url="https://github.com/jamieres/Moloch.-Automated-Version-Control-Library",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
)
