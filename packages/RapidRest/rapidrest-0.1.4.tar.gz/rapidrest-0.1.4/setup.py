from setuptools import setup, find_packages

setup(
    name="RapidRest",
    version="0.1.4",
    author="shubham chavan",
    author_email="shubhamchavan7920@gmail.com",
    description="A Django package to quickly generate serializers and views for Django models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},  # Specify that packages are in 'src'
    packages=find_packages(where="src"),
    url="",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Django>=3.2",
    ],
    python_requires=">=3.6",
    
)
