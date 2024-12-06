from setuptools import setup, find_packages

setup(
    name="af_practical_astronomy",
    version="1.0.6",
    packages=find_packages(include=["practical_astronomy", "practical_astronomy.*"]),
    install_requires=[
    'astronomy_types',
    ],
    author="Artur Foden",
    description="A collection of astronomy functions for practical applications",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Arturius771/practical_astronomy",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.12.4',  
)
