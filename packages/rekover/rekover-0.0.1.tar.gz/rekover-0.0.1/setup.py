from setuptools import setup, find_packages

setup(
    name='rekover',                # Package name
    version='0.0.1',                  # Initial version
    description='rekover project',   # Short description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Francisco Costa',
    author_email='francisco@rekover.ai',
    url='https://github.com/yourusername/my_package',  # URL to the repo
    packages=find_packages(),         # Automatically find submodules
    install_requires=[
        # List dependencies (e.g., 'requests>=2.25.1')
    ],
    classifiers=[                     # Classify the package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
