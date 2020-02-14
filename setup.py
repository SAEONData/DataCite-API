from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name='DataCite-API',
    version=version,
    description='A facade to the DOI functions of the DataCite REST API',
    url='https://github.com/SAEONData/DataCite-API',
    author='Mark Jacobson',
    author_email='mark@saeon.ac.za',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='~=3.6',
    install_requires=[
        'fastapi',
        'uvicorn',
        'python-dotenv',
        'requests',
    ],
    extras_require={
        'test': ['pytest', 'coverage']
    },
)
