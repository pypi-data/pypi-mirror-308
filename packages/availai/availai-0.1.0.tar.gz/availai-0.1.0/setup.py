from setuptools import setup, find_packages

setup(
    name='availai',
    version='0.1.0',
    description='A library for computer vision and machine learning',
    author='Vasyl Arsenii',
    author_email='varsenyi@gmail.com',
    packages=find_packages(),
    install_requires=[
        "ultralytics>=8.3.28",
        "wandb>=0.18.6"
    ],
)