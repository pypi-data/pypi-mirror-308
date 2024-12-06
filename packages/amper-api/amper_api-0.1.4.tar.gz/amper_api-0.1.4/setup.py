from setuptools import setup, find_packages

VERSION = '0.1.4'
DESCRIPTION = 'Amper API package'
LONG_DESCRIPTION = 'Package for communicating with Amplifier API.'

setup(
        name="amper_api",
        version=VERSION,
        author="Amplifier",
        author_email="support@ampliapps.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],

        keywords=['amplifier', 'b2b', 'erp'],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ]
)
