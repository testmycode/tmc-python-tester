from setuptools import setup

setup(
    name='tmc-python-tester',
    version='0.0.1',
    author='Joni Salmi <josalmi@cs.helsinki.fi>, ' +
           'Henrik Nygren <nygrenh@gmail.com>, ' +
           'Ilari Sinkkonen <ilari.sinkkonen@cs.helsinki.fi>',
    author_email='josalmi@cs.helsinki.fi',
    description='',
    license='BSD',
    platforms=['Any'],
    keywords=[
        'unittest', 'testrunner', 'tmc', 'tmc-langs', 'points', 'json'
    ],
    url='http://github.com/rage/tmc-python3-utils/tree/master/',
    zip_safe=False,
    include_package_data=True,
    test_suite='test',
    entry_points={
        'console_scripts': [
            'tmc-python3-utils=tmc_python3_utils:main'
        ]
    }
)
