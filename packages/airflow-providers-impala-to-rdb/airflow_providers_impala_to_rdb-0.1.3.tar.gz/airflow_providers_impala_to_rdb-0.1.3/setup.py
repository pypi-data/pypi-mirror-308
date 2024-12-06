from setuptools import setup, find_packages

setup(
    name='airflow-providers-impala-to-rdb',
    version='0.1.3',
    author='Archer Yang',
    author_email='archer.yang@crypto.com',
    description='A custom Airflow operator to upsert data from Impala to PostgreSQL.',
    packages=find_packages(),
    install_requires=[
        'impyla'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Apache Airflow',
        'License :: OSI Approved :: MIT License',
    ],
)