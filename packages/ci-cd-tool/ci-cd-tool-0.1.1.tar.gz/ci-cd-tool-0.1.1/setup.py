from setuptools import setup, find_packages

setup(
    name='ci-cd-tool',  # 패키지 이름 (고유해야 함)
    version='0.1.1',  # 버전
    description='A CLI tool for managing CI/CD pipelines',
    long_description=open('README.md').read(),  # PyPI 페이지에 표시될 설명
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/username/ci-cd-tool',  # GitHub 또는 프로젝트 페이지
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'click',
        'requests',
        'rich',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'cc = ci_cd_tool.cli:main',  # CLI 명령어
        ],
    },
    include_package_data=True,
    classifiers=[  # 패키지 메타데이터
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
