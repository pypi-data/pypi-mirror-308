from setuptools import setup, find_packages

setup(
    name                = 'vscenv',
    version             = '0.1.1',
    description         = 'Isolate your vscode environment and keep it simple!',
    long_description    = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    author              = 'Gangdae Ju',
    author_email        = 'jugangdae@gamil.com',
    license             = 'MIT',
    url                 = 'https://github.com/jugangdae/vscenv',
    donwload_url        = '',
    python_requires     = '>=3',
    install_requires    = [],
    package_data        = {},
    packages            = find_packages(exclude = []),
    keywords            = ['vscenv', 'manage', 'isolated', 'vscode', 'environment', 'simple', 'cli', 'tool'],
    zip_safe            = False, # Use zip_safe, if you use pacaged_data.
    classifiers         = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points = {
        'console_scripts': [
            'vscenv = vscenv.vscenv:main'
        ]
    }
)

#