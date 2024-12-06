from setuptools import setup, find_packages

setup(
    name='fast-part',
    version='0.1',
    packages=find_packages(),
    install_requires=['biopython'],
    entry_points={
        'console_scripts': [
            'fast-part = fast_part.fast_part:main'
        ],
    },
    description='Fast_Part: A tool for efficient partitioning and clustering of sequences.',
    author='Shafayat Ahmed',
    author_email='shafayatpiyal@vt.edu',
    url='https://github.com/Shafayat115/fast-part',  # Update with your GitHub repo URL if available
)
