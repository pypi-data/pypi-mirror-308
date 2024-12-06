from setuptools import setup, find_packages

setup(
    name="img-characterize",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=2.0.0",
        "opencv-python>=4.9.0.80",
        "opencv-python-headless>=4.9.0.80",
        "pathos>=0.3.2",
        "Pillow>=10.3.0",
        "tqdm>=4.64.0",
    ],
    entry_points={
        'console_scripts': [
            'img-characterize=characterize.cli:main',
        ],
    },
    author="Augusto Rehfeldt",
    description="A tool for converting images into character-based art",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="ascii art, image processing, character art",
    python_requires=">=3.8",
)
