from setuptools import setup, find_packages

setup(
    name="cloudbrowser-puppeteer-connector",
    version="0.1.1",
    author="cloudbrowser",
    author_email="contact@cloudbrowser.ai",
    description="Client for connection with CloudBrowser.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[ 
        'aiohttp>=3.7.0',
        'pyppeteer>=0.2.5',
        'asyncio',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
