import git  # GitPython 라이브러리
import os
import click

# 템플릿 생성 및 Git 커밋 함수
def generate_and_commit_ci_template(ci_tool, config_data):
    """사용자가 선택한 CI 도구에 맞는 템플릿을 생성하고 Git에 커밋 및 푸시"""
    # 템플릿 파일 생성 경로
    project_root = config_data.get('Project_Root', '.')
    template_filename = f"{ci_tool.lower()}_ci.yml"
    output_file = os.path.join(project_root, template_filename)

    # 템플릿 경로 지정 및 파일 생성
    TEMPLATES_PATH = "CCproject/ci_cd_tool/templates/templates"
    default_template_file = os.path.join(TEMPLATES_PATH, f"{ci_tool.lower()}.yml")

    # 템플릿 파일이 없으면 기본 템플릿 생성
    if not os.path.exists(default_template_file):
        click.echo(f"{ci_tool} CI 템플릿 파일이 존재하지 않습니다. 기본 템플릿을 생성합니다.")
        default_template_content = get_default_template_content(ci_tool)
        with open(default_template_file, 'w') as default_template:
            default_template.write(default_template_content)
        click.echo(f"기본 {ci_tool} CI 템플릿 파일이 생성되었습니다: {default_template_file}")

    # 템플릿 파일 로드
    if not os.path.exists(default_template_file):
        click.echo(f"템플릿 파일을 찾을 수 없습니다: {default_template_file}")
        return

    with open(default_template_file, 'r') as file:
        template_content = file.read()

    # 프로젝트 루트에 템플릿 파일 생성
    os.makedirs(project_root, exist_ok=True)
    with open(output_file, 'w') as output:
        output.write(template_content)

    click.echo(f"프로젝트 루트에 {ci_tool} CI 템플릿 파일이 생성되었습니다: {output_file}")

    # Git 커밋 및 푸시 (템플릿 파일과 프로젝트 루트를 인자로 전달)
    commit_and_push_template(ci_tool, output_file, project_root)


def commit_and_push_template(ci_tool, template_file, project_root):
    """
    생성된 템플릿 파일을 Git에 커밋하고 푸시합니다.
    """
    try:
        # Git 리포지토리 열기
        repo = git.Repo(project_root)

        # 파일 상태 확인 후 스테이징
        if not os.path.exists(template_file):
            click.echo(f"템플릿 파일을 찾을 수 없습니다: {template_file}")
            return

        # 변경 사항 스테이징
        repo.index.add([template_file])

        # 커밋
        commit_message = f"Add {ci_tool} CI template"
        repo.index.commit(commit_message)

        # 원격 저장소 푸시
        origin = repo.remote(name='origin')
        origin.push()

        click.echo(f"{ci_tool} CI 템플릿 파일이 커밋되고 푸시되었습니다.")
    except git.exc.InvalidGitRepositoryError:
        click.echo("유효한 Git 리포지토리가 아닙니다. 먼저 Git 리포지토리를 초기화하세요.")
    except Exception as e:
        click.echo(f"템플릿 커밋 및 푸시 중 오류가 발생했습니다: {str(e)}")


def get_default_template_content(ci_tool):
    """
    기본 템플릿 내용을 반환합니다.
    """
    if ci_tool == "GitHub Actions":
        return """
name: CI Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Check out repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: pytest
        """
    elif ci_tool == "GitLab CI":
        return """
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - echo "Building the project..."

test:
  stage: test
  script:
    - echo "Running tests..."

deploy:
  stage: deploy
  script:
    - echo "Deploying the project..."
        """
    elif ci_tool == "Jenkins":
        return """
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
            }
        }
    }
}
        """
    else:
        return "# Unsupported CI tool"
