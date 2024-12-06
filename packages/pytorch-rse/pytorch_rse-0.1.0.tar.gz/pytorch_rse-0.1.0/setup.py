from setuptools import setup, find_packages

setup(
    name='pytorch_rse',
    version='0.1.0',
    author='Tobias M. Brambo',
    author_email='tobias.m.brambo@gmail.com',
    description='A PyTorch wrapper for Random Self-Ensemble (RSE)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tobiasbrambo/pytorch_rse',
    packages=find_packages(),
    install_requires=[
        'torch>=1.10.0',  # Adjust version as needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

