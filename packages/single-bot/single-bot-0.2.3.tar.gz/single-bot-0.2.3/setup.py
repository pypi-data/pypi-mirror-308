from setuptools import setup

setup(
    name="single-bot",
    version="0.2.3",
    author="Nikita Karfidov",
    author_email="krfdv.ai@gmail.com",
    license="AGPL-3.0",
    description="Omnichannel state-based chatbot framework",
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    packages=["single_bot"],
    install_requires=["aiogram", "sqlitedict", "dill", "python-dotenv", "sqlalchemy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
)
