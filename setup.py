from setuptools import setup, find_packages
import os

# Look for requirements file
parent_folder = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(parent_folder, 'requirements.txt')) as req:
    INSTALL_REQUIRES = req.read().split('\n')

setup(
    author='Whitman Bohorquez',
    author_email='whitman-2@hotmail.com',
    name='simpleid',
    license='',
    description='64bits integer ids for any database vendor',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7.0',
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        'Development Status :: Alpha',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
)
