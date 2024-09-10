from setuptools import find_packages, setup

readme = []
with open('README.rst', 'r') as fh:
    readme = fh.readlines()

tests_require = [
    'django-webtest',
    'factory-boy',
    'mock',
    'pytest-cov',
    'pytest-django',
    'pytest',
    'requests-mock',
    'requests-toolbelt',
]

setup(
    name='localshop',
    version='3.0.0-alpha.1',
    author='Michael van Tellingen',
    author_email='michaelvantellingen@gmail.com',
    url='http://github.com/mvantellingen/localshop',
    description='A private pypi server including auto-mirroring of pypi.',
    long_description='\n'.join(readme),
    zip_safe=False,
    install_requires=[
        'boto3',
        'celery',
        'django-braces',
        'django-celery-beat',
        'django-celery-results',
        'django-environ',
        'django-model-utils',
        'django-storages',
        'django-widget-tweaks',
        'Django',
        'docutils',
        'netaddr',
        'Pillow',
        'psycopg2-binary',
        'redis',
        'requests',
        'social-auth-app-django',
        'sqlparse',
        'Versio==0.4.0',
    ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
    license='BSD',
    include_package_data=True,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'localshop = localshop.runner:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: System',
        'Topic :: System :: Software Distribution',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
