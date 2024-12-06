from setuptools import setup


def readme():
    with open("README_PYPI.md", "r") as f:
        return f.read()


setup(
    name="polotsk",
    version="1.1.0",
    fullname="polotsk",
    description="This is polotsk module",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=[
        "polotsk",
        "polotsk-admin",
        # "polotsk-admin/app",
        "polotsk-admin/app/main",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="polotsk python",
    python_requires=">=3.11",
)
