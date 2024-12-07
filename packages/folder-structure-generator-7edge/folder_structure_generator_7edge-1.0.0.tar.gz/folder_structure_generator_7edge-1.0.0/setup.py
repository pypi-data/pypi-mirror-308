from setuptools import setup, find_packages

setup(
    name='folder-structure-generator-7edge',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['InquirerPy'],
    entry_points={
        'console_scripts': [
            'generate-structure=folder_structure_generator.generator:create_service_structure',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='CLI tool to generate folder structures for services',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/folder-structure-generator-7edge',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
