from setuptools import setup, find_packages

setup(
    name="lakeel",
    version="0.0.4",
    description="파이썬 패키지 관리를 위한 편리한 도구 모음",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="bunhine0452",
    author_email="hb000122@gmail.com",
    url="https://github.com/bunhine0452/pip_lakeel",
    packages=find_packages(),
    license='MIT',
    install_requires=['matplotlib', 'pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.8',
)


