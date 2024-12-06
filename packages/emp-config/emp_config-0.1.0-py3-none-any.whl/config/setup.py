# Building setup to package 'utl_logger'
import os
from setuptools import setup, find_packages

# Reading README.md as description
readme_path: os.PathLike[str] = os.path.join(os.path.dirname(__file__), 'README.md')
with open(file = readme_path, mode = 'r') as fh:
    long_description = fh.read()
    fh.close()

# Reading requirements.txt for utl_logger
requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(file = requirements_path, mode = 'r') as f:
    required = f.read().splitlines()
    f.close()

# Setup
setup(
    name = 'emp_config',
    version = '0.1.0',
    description = """Custom configuration loader with integrated Fallback to local retrievement of environment variables in case Spring Config Server isn't available""",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'AbdoCherry',
    packages = find_packages(where = 'src', exclude = ['tests*']),
    package_dir = {'' : 'src'},
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires = required,
    license = 'MIT',
    url = 'https://github.com/AbdoCherry/EMP_UTL-S'
)