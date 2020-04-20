from io import open
from setuptools import find_packages, setup

with open('src/ptkcmd/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'
with open('README.md','r') as f:
    readme = f.read()

REQUIRES = ['prompt-toolkit']

setup(
    name='ptkcmd',
    version=version,
    description='cmd.py from the standard library adapted to use prompt-toolkit instead of readline',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Matthew Miguel',
    author_email='mmiguel6288code@gmail.com',
    maintainer='Matthew Miguel',
    maintainer_email='mmiguel6288code@gmail.com',
    url='https://github.com/mmiguel6288code/ptkcmd',
    license='MIT',
    keywords=[
        'cmd','cmd.py','command line','cli','prompt-toolkit','ptkcmd','prompt',
        
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    install_requires=REQUIRES,
    tests_require=[],
    packages=find_packages('src'),
    package_dir={'':'src'},
)
