from setuptools import setup, find_packages

package_name = "SpotSegmentation"

def read_requirements():
    with open('requirements.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

setup(
    name=package_name,
    version='0.5',
    packages=find_packages(),
    install_requires=read_requirements(),
    author="Matthias Kellner",
    include_package_data=True,
    author_email="matthias.kellner@ccri.at",
    description="",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/TaschnerMandlGroup/SpotSegmentation",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)