from setuptools import setup, find_packages
setup(
    name = "resumableS3",
    packages = find_packages(),
    version = "0.1.3",
    license = "MIT",
    description = "A Python program for resumable S3 cp",
    author = "Jun Mencius",
    author_email = "acemencius@gmail.com",
    url = "https://github.com/JMencius/resumableS3",
    keywords = ["resumable", "download", "s3", "python"],
    python_requires = ">=3.8",
    install_requires = [
        "tqdm>=4.67.0",
        "boto3>=1.35.57",
        "click>=8.1.7",
        ],
    entry_points={
    "console_scripts": [
        "rs3 = resumableS3.main:main",
        ],
    },
)
