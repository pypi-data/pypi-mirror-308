from setuptools import setup, find_packages

setup(
    name='cpapp',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cpapp=cpapp.main:main',
        ],
    },
    author='Your Name',
    author_email='mustafa.hakimi@outlook.dk',
    description='A command-line tool to copy file contents based on extension.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/HakimiX/cpapp',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)