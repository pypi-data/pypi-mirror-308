from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="JunoAccessManager",  # 替换为你的项目名称
    version="1.1.2",  # 版本号
    author="Yuhui.Wang",  # 作者姓名
    author_email="wangyuhui341@163.com",  # 作者邮箱
    description="租户接入",  # 项目简介
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/your_project_name",  # 项目主页
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "backports.tarfile",
        "certifi",
        "charset-normalizer",
        "docutils",
        "idna",
        "importlib_metadata",
        "jaraco.classes",
        "jaraco.context",
        "jaraco.functools",
        "keyring",
        "markdown-it-py",
        "mdurl",
        "more-itertools",
        "nh3",
        "pkginfo",
        "pulsar-client",
        "Pygments",
        "pywin32-ctypes",
        "readme_renderer",
        "requests",
        "requests-toolbelt",
        "rfc3986",
        "rich",
        "twine",
        "typing_extensions",
        "urllib3",
        "zipp",
    ]
)