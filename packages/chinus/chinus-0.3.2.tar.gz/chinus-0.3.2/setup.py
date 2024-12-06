from setuptools import setup, find_packages

setup(
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    install_requires=[
        'json5',  # 추가할 종속성 패키지
    ],
)