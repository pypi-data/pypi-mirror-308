from setuptools import find_packages, setup

setup(
    name="slacknotifpy",
    version="1.0.3",
    packages=find_packages(),
    py_modules=["slacknotif"],
    install_requires=[
        "slack_sdk",
    ],
    entry_points={
        "console_scripts": [
            "slacknotif=slacknotif:main",
        ],
    },
    author="Zein Hajj-Ali",
    author_email="zeinhajjali@outlook.com",
    description="A Python tool for sending Slack notifications on job completion.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zeinhajjali/slacknotifpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
