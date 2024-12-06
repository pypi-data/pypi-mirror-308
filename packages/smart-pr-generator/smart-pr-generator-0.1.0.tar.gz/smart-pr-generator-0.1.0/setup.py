from setuptools import setup, find_packages

setup(
    name="smart-pr-generator",  # PyPI에 등록될 패키지 이름
    version="0.1.0",                  # 버전
    packages=find_packages(),         # 패키지 자동 검색
    install_requires=[                # 의존성 패키지
        'requests>=2.25.1',
    ],
    entry_points={                    # CLI 명령어 설정
        'console_scripts': [
            'pr=smart_pr_generator.main:main',
        ],
    },
    author="jeongsk",
    author_email="jeongseok@wantedlab.com",
    description="A short description of your package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jeongsk/Smart-PR-Generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)