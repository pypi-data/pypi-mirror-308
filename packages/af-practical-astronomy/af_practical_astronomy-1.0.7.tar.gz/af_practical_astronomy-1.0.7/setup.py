from setuptools import setup, find_packages

setup(
    name='af_practical_astronomy',
    version='1.0.7',
    description='A practical astronomy library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Artur Foden',
    url='https://github.com/yourusername/practical_astronomy',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    install_requires=[  
        'astronomy_types',
    ],
    test_suite='pytest',
)
