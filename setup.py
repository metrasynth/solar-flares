""""""

from setuptools import find_packages, setup

dependencies = [
    'numpy',
    'orbitant',
    'radiant-voices',
    'scipy',
    'sounddevice',
    'sunvox-dll-python',
]

setup(
    name='solar-flares',
    version='0.1.0',
    url='https://github.com/metrasynth/solar-flares',
    license='MIT',
    author='Matthew Scott',
    author_email='matt@11craft.com',
    description='Sound design and performance tools for SunVox',
    long_description=__doc__,
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={},
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
