from setuptools import find_packages, setup

setup(
    name="slacknotifpy",  # Unique name for your package
    version="1.0.0",
    packages=find_packages(),
    py_modules=["slacknotif"],  # List your modules here
    install_requires=[
        "slack_sdk",  # Dependencies
    ],
    entry_points={
        "console_scripts": [
            "slacknotif=slacknotif:main",  # Allows `slacknotif` command
        ],
    },
    author="Zein Hajj-Ali",
    author_email="zeinhajjali@outlook.com",
    description="A Python tool for sending Slack notifications on job completion.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zeinhajjali/slacknotifpy",  # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
