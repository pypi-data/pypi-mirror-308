from setuptools import setup, find_packages

setup(
    name='calendly-fetcher',
    version='0.1.0',
    author='Malek Ibrahim',
    author_email='shmeek8@gmail.com',
    description='A package to fetch availability data from Calendly',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/malekinho8/calendly-fetcher.git',
    packages=find_packages(),
    install_requires=[
        'requests',
        # Add any other dependencies
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Choose your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)