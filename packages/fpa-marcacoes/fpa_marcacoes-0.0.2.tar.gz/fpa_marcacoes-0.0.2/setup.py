from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'An API Wrapper for the FPA\'s website of trainings and massage scheduler'
LONG_DESCRIPTION = 'An API Wrapper for the FPA\'s website of trainings and massage scheduler'

setup(
    name='fpa_marcacoes',
    version=VERSION,
    author='André Oliveira',
    author_email='andre_pinto_oliveira@outlook.pt',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_required=[
        'requests'
    ],

    keywords=['python', 'FPA'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)