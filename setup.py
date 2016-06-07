from setuptools import setup, find_packages

setup(
    name='hcl_translator',
    packages=find_packages(),
    dependency_links=['git+https://github.com/virtuald/pyhcl.git@0830b300774f94b930255bded91c08cb03c1df8e#egg=pyhcl'],
    install_requires=[
        'pyhcl',
    ],
    tests_require=['pytest', 'moto'],
    version='0.1.4',
    description='Translator for HCL configuration files',
    author='Derrick Petzold',
    author_email='dpetzold@clearcareonline.com',
    url='https://github.com/clearcare/cc_hcl_translator',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: System :: Distributed Computing',
    ]
)
