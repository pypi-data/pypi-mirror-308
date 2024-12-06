from setuptools import setup, find_packages

setup(
    name="pdxwave",  # パッケージ名
    version="0.0.4",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pdxwave = pdxwave:main',  # 実行コマンドとエントリポイント
        ],
    },
    install_requires=[  # 依存関係
        "requests"
    ],
)
