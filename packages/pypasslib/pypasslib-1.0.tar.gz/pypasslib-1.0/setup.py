from setuptools import setup, find_packages

setup(
    name='pypasslib',
    version='1.0',
    packages=find_packages(),
    description='A Python module containing a list of a million passwords to use for educational purposes only',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Opticz',
    author_email='cartiscott45@gmail.com',
    url='https://github.com/Opticz45/pypasslib', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    license_expression='CC-BY-NC-4.0',
    python_requires='>=3.6',
)
