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
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask',],
    license="MIT",
    url="https://github.com/brownboycodes/common-api-server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages= find_packages(where="src"),
    python_requires=">=3.6",
)

