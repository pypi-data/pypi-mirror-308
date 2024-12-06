from setuptools import setup, find_packages

setup(
    name='pyduckchat',
    version='0.1.0',
    description='An unofficial library for interacting with DuckDuckGo chat API.',
    author='Dev',
    author_email='asd@w.cn',
    url='https://github.com/tolgakurtuluss/pyduckchat',  # Update with your GitHub URL
    packages=find_packages(),
    install_requires=[
        'httpx',  # Add any other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
