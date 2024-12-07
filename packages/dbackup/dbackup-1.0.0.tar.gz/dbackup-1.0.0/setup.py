from setuptools import setup, find_packages

setup(
    name="dbackup",
    version="1.0.0",
    description="A Django application for UTF-8 database backups.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Enes HAZIR",
    author_email="your.email@example.com",
    url="https://github.com/eneshazr/django-dbackup",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=4.2",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.12",
    ],
)
