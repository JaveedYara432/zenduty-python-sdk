from setuptools import setup, find_packages

setup(
    name="zenduty-api",
    version="2.6",
    description="Python SDK wrapper for the Zenduty API",
    long_description="Python SDK wrapper for the Zenduty API",
    long_description_content_type="text/x-rst",
    author="Javeed Yara",
    author_email="javeed@zenduty.com",
    packages=find_packages(),
    install_requires=[
        "requests==2.32.3",
        "urllib3==2.2.2",
        "six==1.9.0",
        "charset-normalizer==3.3.2",
        "idna==3.7",
        "certifi==2024.7.4",
    ],
    url="https://github.com/Zenduty/zenduty-python-sdk",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",  # Update based on your package's status
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",  # Specify Python versions supported
    ],
    python_requires=">=3.6",  # Specify the minimum Python version
    scripts=["bin/client.py"],  # Include any scripts you want to make executable
)
