from setuptools import setup, find_packages

setup(
    name="discord-webhook-async",
    version="0.1.1",
    description="Async library for working with Discord webhooks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ap4kk/discord-webhook-async",
    author="Ap4kk",
    author_email="arseniy.domrachev.12@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires="aiohttp==3.10.10",  # Укажите зависимости
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
