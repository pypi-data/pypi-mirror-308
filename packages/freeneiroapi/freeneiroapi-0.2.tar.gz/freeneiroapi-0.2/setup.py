from setuptools import setup, find_packages

setup(
    name='freeneiroapi',
    version='0.2',
    description='API library for interacting with DuckGPT',
    author='FutFut19',
    author_email='futfut19@icloud.com',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
