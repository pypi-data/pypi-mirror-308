from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mqtt-router",
    use_scm_version={
        "version_scheme": "post-release",
        "local_scheme": "no-local-version",
    },
    setup_requires=["setuptools-scm"],
    author="Abdellatif Labreche",
    author_email="abdellatif.labreche@gmail.com",
    description="Simple client agnostic MQTT message router",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abdellatifLabr/mqtt-router",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    extras_require={},
    entry_points={},
    include_package_data=True,
)
