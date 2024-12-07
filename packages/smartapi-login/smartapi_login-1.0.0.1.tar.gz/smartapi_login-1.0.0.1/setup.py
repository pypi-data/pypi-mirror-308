from setuptools import setup, find_packages

setup(
    name='smartapi_login',  # Name of the package
    version='1.0.0.1',  # Version of the package
    description='A library for interacting with SmartAPI for historical data, trading sessions, and more.',
    long_description=open('README.md').read(),  # Long description from your README.md file
    long_description_content_type='text/markdown',  # Format of the long description (markdown)
    author='Mahesh Kumar',  # Your name or organization's name
    author_email='maheshrajbhar90@gmail.com',  # Your contact email
    url='https://github.com/maheshrajbhar90/AutoSmartAPI',  # URL of your GitHub repo
    packages=find_packages(),  # Automatically find and include all packages in the repository
    
    install_requires=[
        'pandas>=1.0.0',  # pandas is required, specify the version range
        'requests>=2.0.0',  # requests library for making HTTP requests
        'pytz>=2020.1',  # pytz for timezone management
        'pyotp>=2.0.0',  # pyotp for TOTP (Two-factor authentication)
        'SmartApi',  # Assuming this is a custom module, ensure it is installed via pip
    ],  # List of dependencies for your package
    classifiers=[
        'Programming Language :: Python :: 3',  # Python 3
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',  # Works on any OS
    ],
    python_requires='>=3.6',  # Specify the required Python version
    include_package_data=True,  # Include any additional files specified in MANIFEST.in
    # Any additional options like data files can be added here
    entry_points={  # Define entry points for command-line scripts
        "console_scripts": [
            "smartapi_login=smartapi_login:SmartAPI",
        ],
    },
)
