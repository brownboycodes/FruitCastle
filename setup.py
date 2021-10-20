from setuptools import find_packages,setup

with open("README.md","r",encoding="utf-8") as fh:
    long_description=fh.read()

setup(
    name='common-api-server-brownboycodes',
    version='0.0.1',
    author="Nabhodipta Garai",
    description="an open source platform to host various API endpoints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask',],
    license="MIT"
)

