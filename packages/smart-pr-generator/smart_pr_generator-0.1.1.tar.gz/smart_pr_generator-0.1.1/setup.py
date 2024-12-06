from pathlib import Path

import tomli
from setuptools import find_packages, setup

from smart_pr_generator.main import VERSION


def get_version():
    """pyproject.toml에서 버전 정보를 읽어옵니다."""
    # 현재 스크립트의 위치에서 프로젝트 루트 찾기
    current_dir = Path(__file__).parent.parent
    pyproject_path = current_dir / "pyproject.toml"
    print("pyproject_path", pyproject_path)

    with open(pyproject_path, "rb") as f:
        pyproject_data = tomli.load(f)
        print(pyproject_data)
        return pyproject_data["tool"]["poetry"]["version"]


setup(
    name="smart-pr-generator",  # PyPI에 등록될 패키지 이름
    version=VERSION,  # 버전
    packages=find_packages(),  # 패키지 자동 검색
    install_requires=[],  # 의존성 패키지
    entry_points={  # CLI 명령어 설정
        "console_scripts": [
            "pr=smart_pr_generator.main:main",
        ],
    },
    author="jeongsk",
    author_email="jeongseok@wantedlab.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jeongsk/Smart-PR-Generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
