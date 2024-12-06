from setuptools import setup, find_packages

setup(
    name='SqlSupport',
    version='1.0.0',
    author='Artex Team',
    description='A python library to ease down sql database query',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JunaidParkar/SqlSupport',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    project_urls={
        'Documentation': 'https://github.com/JunaidParkar/SqlSupport',
        'Source': 'https://github.com/JunaidParkar/SqlSupport',
        'Tracker': 'https://github.com/JunaidParkar/SqlSupport',
    },
)