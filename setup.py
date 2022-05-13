from setuptools import setup

setup(
    name='pubmedake',
    version='0.1.0',    
    description='A example Python package',
    url='https://github.com/GarfieldLeo/PubMedAKE',
    author='Leo Sheng',
    author_email='',
    license='BSD 2-clause',
    packages=['pubmedake'],
    install_requires=['nltk',
                      'numpy'                     
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)