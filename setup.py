from setuptools import setup, find_packages

setup(
    name="chat_app",
    version="0.1.0",
    author="Abdullah Zainel & Kerem Durgut & Zeren Kavaz & Mesude Türkmen",
    author_email="your_email@example.com",
    description="A server-client chat application with Redis and MySQL support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MesudeTurkmen/cheat_chat",  # GitHub URL
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python",
        "redis",
        "asyncio"  # veya başka gerekli kütüphaneler
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
