import click
import os
import inquirer
import git  # GitPython 라이브러리 사용
from rich.console import Console
from ci_cd_tool.config.config_manager import save_config, show_config
from ci_cd_tool.utils.cli_prompt import set_top_screen as sts

# 설정 딕셔너리
set_config = {
    "Project_Root": None,
    "Pipline": None,
    "Framework": None,
    "ci_tool": None,
    "Remote_Repo": None
}

console = Console()

# CI/CD 초기화 함수
def cc_init(set_config):
    """CI/CD 설정 초기화"""

    sts()  # 화면을 상단으로 이동하여 깔끔하게 보이도록 설정

    # 프로젝트 이름 설정
    set_config['Project_Root'] = ask_question(
        inquirer.Text('Project_Root', message="프로젝트 이름을 입력하세요"),
        "프로젝트 이름 설정에 실패했습니다."
    )

    # 프로젝트 루트 경로 유효성 검사
    if not os.path.isdir(set_config['Project_Root']):
        click.echo("유효한 프로젝트 경로를 입력하세요.")
        return

    # 파이프라인 단계 선택
    set_config['Pipline'] = ask_question(
        inquirer.List('Pipline', message="포함할 파이프라인 단계를 선택하세요", choices=['build', 'test', 'deploy']),
        "파이프라인 단계 설정에 실패했습니다."
    )

    # 테스트 프레임워크 선택
    set_config['Framework'] = ask_question(
        inquirer.List('Framework', message="어떤 테스트 프레임워크를 사용할까요?", choices=['unittest', 'pytest']),
        "테스트 프레임워크 설정에 실패했습니다."
    )

    # CI 도구 선택
    selected_ci_tool = ask_question(
        inquirer.List('ci_tool', message="어떤 CI 도구를 사용할까요?", choices=['GitHub Actions', 'GitLab CI', 'Jenkins']),
        "CI 도구 설정에 실패했습니다."
    )
    set_config['ci_tool'] = selected_ci_tool

    # 선택한 CI 도구에 따른 추가 설정
    if selected_ci_tool == "GitHub Actions":
        python_version = ask_question(
            inquirer.Text('python_version', message="Python 버전을 지정하세요 (기본값: 3.x)", default="3.x"),
            "Python 버전 설정에 실패했습니다."
        )
        set_config['python_version'] = python_version
        click.echo(f"GitHub Actions가 Python {set_config['python_version']} 버전으로 설정되었습니다.")
    elif selected_ci_tool == "GitLab CI":
        gitlab_stages = ask_question(
            inquirer.Checkbox('stages', message="GitLab CI 파이프라인에 포함할 단계를 선택하세요",
                              choices=['build', 'test', 'deploy']),
            "GitLab CI 단계 설정에 실패했습니다."
        )
        set_config['gitlab_stages'] = gitlab_stages
        click.echo(f"GitLab CI 단계가 다음으로 설정되었습니다: {', '.join(set_config['gitlab_stages'])}.")
    elif selected_ci_tool == "Jenkins":
        click.echo("Jenkins 설정 중...")

    # Git 원격 저장소 설정
    remote_repo_url = ask_question(
        inquirer.Text('Remote_Repo', message="원격 저장소 URL을 입력하세요 (공백일 경우 로컬에서 Git 초기화)"),
        "원격 저장소 설정에 실패했습니다."
    )
    set_config['Remote_Repo'] = remote_repo_url.strip()

    # Git 리포지토리 초기화 및 원격 저장소 설정
    initialize_git_repository(set_config)

    # 설정 파일을 config.yml로 저장
    save_config(set_config)

    # 결과 박스 출력
    sts()  # 화면을 상단으로 이동하여 결과가 깔끔하게 보이도록 설정
    show_config()

    # CI 템플릿 생성
    generate_and_commit_ci_template(selected_ci_tool, set_config)

    return set_config

# 질문을 통해 답변을 받고 유효성을 검사하는 함수
def ask_question(question, error_message):
    """질문을 통해 답변을 받고 유효성을 검사하는 함수"""
    answer = inquirer.prompt([question])
    if answer and isinstance(answer, dict):
        return list(answer.values())[0]
    else:
        click.echo(error_message)
        return None

# Git 리포지토리를 초기화하고 원격 저장소를 설정하는 함수
def initialize_git_repository(config):
    """Git 리포지토리를 초기화하고 원격 저장소를 설정"""
    project_root = config.get('Project_Root')
    remote_repo_url = config.get('Remote_Repo')

    if not project_root:
        click.echo("프로젝트 루트가 설정되지 않았습니다.")
        return

    if not os.path.exists(project_root):
        os.makedirs(project_root)

    try:
        # 프로젝트 루트에서 Git 리포지토리 초기화
        repo = git.Repo.init(project_root)
        click.echo(f"{project_root}에 Git 리포지토리가 초기화되었습니다.")

        if remote_repo_url:
            # 원격 저장소 추가
            origin = repo.create_remote('origin', remote_repo_url)
            click.echo(f"원격 저장소 '{remote_repo_url}'가 설정되었습니다.")
        else:
            click.echo("원격 저장소 URL이 제공되지 않았습니다. 원격 저장소를 수동으로 설정하세요.")

    except git.exc.GitCommandError as e:
        click.echo(f"Git 리포지토리 초기화 중 오류가 발생했습니다: {str(e)}")

# CI 템플릿 생성 및 커밋 함수
def generate_and_commit_ci_template(ci_tool, config_data):
    """CI 템플릿을 생성하고 Git에 커밋 및 푸시"""
    # 템플릿 파일 경로
    project_root = config_data.get('Project_Root', '.')
    template_root = os.path.join(project_root, "ci_cd_tool","templates" ,"templates")
    template_filename = f"{ci_tool.lower().replace(' ', '_')}_ci.yml"
    output_file = os.path.join(template_root ,template_filename)

    # 템플릿 디렉토리
    TEMPLATES_PATH = "CCproject/ci_cd_tool/templates/templates"
    default_template_file = os.path.join(TEMPLATES_PATH, f"{ci_tool.lower().replace(' ', '_')}.yml")

    # 템플릿 파일이 없으면 기본 템플릿 생성
    if not os.path.exists(default_template_file):
        click.echo(f"{ci_tool} CI 템플릿 파일이 존재하지 않습니다. 기본 템플릿을 생성합니다.")
        default_template_content = get_default_template_content(ci_tool)
        os.makedirs(TEMPLATES_PATH, exist_ok=True)
        with open(default_template_file, 'w') as default_template:
            default_template.write(default_template_content)
        click.echo(f"기본 {ci_tool} CI 템플릿 파일이 생성되었습니다: {default_template_file}")

    # 템플릿 파일 로드
    template_content = load_template_file(default_template_file)

    # 프로젝트 루트에 템플릿 파일 생성
    os.makedirs(template_root, exist_ok=True)
    with open(output_file, 'w') as output:
        output.write(template_content)

    click.echo(f"프로젝트 루트에 {ci_tool} CI 템플릿 파일이 생성되었습니다: {output_file}")

    # Git에 템플릿 커밋 및 푸시
    commit_and_push_template(ci_tool, output_file, project_root)

# 템플릿 파일을 로드하는 함수
def load_template_file(template_file_path):
    """템플릿 파일을 로드"""
    try:
        with open(template_file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        click.echo(f"템플릿 파일을 찾을 수 없습니다: {template_file_path}")
        return ""

# 생성된 템플릿 파일을 Git에 커밋하고 푸시하는 함수
def commit_and_push_template(ci_tool, template_file, project_root):
    """생성된 CI 템플릿 파일을 Git에 커밋하고 푸시"""
    try:
        # Git 리포지토리 열기
        repo = git.Repo(project_root)

        # 템플릿 파일 스테이징
        if not os.path.exists(template_file):
            click.echo(f"템플릿 파일을 찾을 수 없습니다: {template_file}")
            return

        repo.index.add([template_file])

        # 커밋
        commit_message = f"Add {ci_tool} CI template"
        repo.index.commit(commit_message)

        # 원격 저장소 푸시
        origin = repo.remote(name='origin')
        retry_attempts = 3  # 푸시 재시도 횟수
        for attempt in range(retry_attempts):
            try:
                origin.push(refspec='main:main', set_upstream=True)
                click.echo(f"{ci_tool} CI 템플릿 파일이 커밋되고 푸시되었습니다.")
                break
            except git.exc.GitCommandError as e:
                if attempt < retry_attempts - 1:
                    click.echo(f"푸시 중 오류가 발생했습니다. 재시도 중입니다... (시도 {attempt + 1}/{retry_attempts})")
                else:
                    click.echo(f"푸시 중 오류가 발생했습니다: {str(e)}")
    except git.exc.InvalidGitRepositoryError:
        click.echo("유효한 Git 리포지토리가 아닙니다. 먼저 Git 리포지토리를 초기화하세요.")
    except Exception as e:
        click.echo(f"템플릿 커밋 및 푸시 중 오류가 발생했습니다: {str(e)}")

# 기본 템플릿 내용을 반환하는 함수
def get_default_template_content(ci_tool):
    """기본 템플릿 내용을 반환"""
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