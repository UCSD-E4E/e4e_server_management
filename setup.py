from setuptools import setup, find_packages

setup(
    name='ServerManagement',
    version='0.0.0.1',
    author='UCSD Engineers for Exploration',
    author_email='e4e@eng.ucsd.edu',
    entry_points={
        'console_scripts': [
            'manager = ServerManagement.ssh_manager:ssh_manager',
            'remote_manager = ServerManagement.remote_manger:main'
        ]
    },
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        'pytest',
        'schema',
        'fabric2',
        'glances-api',
    ]
)