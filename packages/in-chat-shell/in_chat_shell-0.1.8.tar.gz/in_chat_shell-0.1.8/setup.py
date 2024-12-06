from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# with open("requirements.txt", "r", encoding="utf-8") as fh:
#     requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

requirements = [
    "prompt_toolkit==3.0.48",
    "Pygments==2.18.0",
    "Requests==2.32.3",
    "tenacity==9.0.0",
]

setup(
    name="in-chat-shell",
    version="0.1.8",
    author="litongxue",
    author_email="litonglitong@hotmail.com",
    description="An intelligent shell with AI chat capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/l1905/smart_shell",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'in-chat-shell=chat_shell.main:entry_point',
        ],
    },
)
