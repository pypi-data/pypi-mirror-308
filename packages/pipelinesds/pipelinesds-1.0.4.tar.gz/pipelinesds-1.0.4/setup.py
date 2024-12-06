from setuptools import setup, find_packages

with open("docs/ALTERNATIVE_README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pipelinesds",
    version="1.0.4",
    packages=find_packages(),
       install_requires=[
           'google-cloud-bigquery',
           'google-cloud-bigquery-storage',
           'google-cloud-storage',
           'pandas',
           'db-dtypes',
           'evidently'
    ],
    author="DS Team",
    author_email="ds@sts.pl",
    description="Solution for DS Team",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
