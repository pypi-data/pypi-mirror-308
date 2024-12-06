from setuptools import setup, find_packages

setup(
    name="pdxwave",  # パッケージ名
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pdxwave = pdxwave.main:main',  # 実行コマンドとエントリポイント
        ],
    },
    install_requires=[  # 依存関係
        "requests"
    ],
)
