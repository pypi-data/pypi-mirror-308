from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()


# setup(
#     name="polotsk",
#     version="1.0.25",
#     author="B",
#     fullname="polotsk",
#     description="This is polotsk module",
#     long_description=readme(),
#     long_description_content_type="text/markdown",
#     # packages=find_packages(),
#     # packages=[
#     #     "polotsk",
#     # ],
#     classifiers=[
#         "Programming Language :: Python :: 3.11",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     package_dir={"polotsk/": "package/src/"},
#     # package_dir={"polotsk": "package/src"},
#     # packages=find_packages(where="package/src"),
#     keywords="polotsk python",
#     python_requires=">=3.7",
# )

setup(
    name="polotsk",
    version="1.0.38",
    # author="",
    fullname="polotsk",
    # description="This is polotsk module",
    # long_description=readme(),
    # long_description_content_type="text/markdown",
    # packages=find_packages(),
    packages=[
        "polotsk",
        "polotsk-admin",
        "polotsk-admin/app",
        "polotsk-admin/app/main",
    ],
    # classifiers=[
    #     "Programming Language :: Python :: 3.11",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
    # package_dir={"polotsk": "package/src/"},
    # packages=find_packages(where="package/src"),
    # keywords="polotsk python",
    # python_requires=">=3.7",
)
