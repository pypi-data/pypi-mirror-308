from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Define the required dependencies
install_requires = [
    'certifi>=2024.7.4',
    'charset-normalizer>=3.3.2',
    'contourpy>=1.2.1',
    'cycler>=0.12.1',
    'Cython>=3.0.11',
    'fonttools>=4.53.1',
    'idna>=3.7',
    'kiwisolver>=1.4.5',
    'llvmlite>=0.43.0',
    'mathutils>=3.3.0',
    'matplotlib>=3.7.1',
    'numba>=0.60.0',
    'numpy>=1.26.4',
    'opencv-python>=4.10.0.84',
    'packaging>=24.1',
    'pillow>=9.4.0',
    'pyparsing>=3.1.2',
    'python-dateutil>=2.8.2',
    'requests>=2.32.3',
    'scipy>=1.13.1',
    'six>=1.16.0',
    'urllib3>=2.0.7',
    'zstandard>=0.23.0',
]

setup(
    name='sensingsp',
    version='1.0',
    packages=find_packages(),
    install_requires=install_requires,
    url='https://sensingsp.github.io/',
    license='MIT',
    author='Moein Ahmadi',
    author_email='moein.ahmadi@uni.lu, gmoein@gmail.com',
    description='SensingSP™ is an open-source library for simulating sensing systems with a focus on array radar signal processing.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    extras_require={
        'no_deps': [],  # Allows installing without any dependencies
    },
)
