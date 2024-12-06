from setuptools import setup, find_packages

setup(
    name="EasyAPIOpenAI",
    version="0.1.0",
    author="Wojtekb30 (Wojciech B)",
    author_email="wojtekb30.player@gmail.com",
    description="Python classes for interacting with OpenAI's API to use ChatGPT or DALL-E very easily.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Wojtekb30/EasyAPIOpenAI",  # Change to your GitHub repository
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0",
        "pillow>=8.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

