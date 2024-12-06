from setuptools import setup

name = '${LibName}'

setup(
    name=name,
    version='${version}',
    author="KeyisB",
    author_email="keyisb.pip@gmail.com",
    description=name,
    long_description='',
    long_description_content_type="text/markdown",
    url=f"https://github.com/KeyisB/libs/tree/main/{name}",
    packages=[name.replace('-','_')],
    package_dir={'': f'{name}'.replace('-','_')},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    license="MMB License v1.0",
    install_requires= '${install_requires}',
)
