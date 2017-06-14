from setuptools import setup, find_packages

setup(
    name="apkg",
    version="0.1",
    description="Support for the Apple Distribution Package format",
    packages=['apkg'],
    author="mosen",
    license="MIT",
    url="https://github.com/mosen/apkg",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='apple package pkg',
    install_requires=[
    ],
    python_requires='>=3.3',
    tests_require=[
        'pytest',
        'mock'
    ],
    setup_requires=['pytest-runner'],
    entry_points={
        'console_scripts': [
            'lsbom=apkg.lsbom:main',
            'dumpbom=apkg.dumpbom:main'
        ]
    },
    zip_safe=False
)


