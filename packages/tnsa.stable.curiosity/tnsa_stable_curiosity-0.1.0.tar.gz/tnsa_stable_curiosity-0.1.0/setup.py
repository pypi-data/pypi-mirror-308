from setuptools import setup, find_packages

setup(
    name='tnsa.stable.curiosity',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0',  # Adjust according to your dependencies
        'numpy',
        'six',
    ],
    license='NGen2Community License',  # Your custom license
    description='A transformer model with advanced features for casual language modeling.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/TnsaAi/tnsa.stable.curiosity',  # Replace with actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
