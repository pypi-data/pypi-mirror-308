import setuptools
setuptools.setup(     
     name="sub-module",     
     version="0.0.1",
     python_requires=">=3.6",
     packages=["AdvancedLogger"],
     install_requires=['boto3>=1', 'requests>=2'],
)
