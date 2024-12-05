import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
version = '2.1.4'

setuptools.setup(
    name='pytimetag',
    version=version,
    author='Hwaipy',
    author_email='hwaipy@gmail.com',
    description='A data processing lib for TimeTag.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='gpl-3.0',
    # url='https://github.com/hwaipy/InteractionFreePy',
    # download_url='https://github.com/hwaipy/InteractionFreePy/archive/v{}.tar.gz'.format(version),
    keywords=['timetag', 'physics'],
    # packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'msgpack',
        'numba'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)
