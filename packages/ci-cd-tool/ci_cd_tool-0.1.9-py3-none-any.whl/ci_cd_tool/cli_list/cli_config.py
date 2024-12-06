import click
import inquirer
from ci_cd_tool.config.config_manager import load_config, show_config, change_config, reset_config
from ci_cd_tool.utils.cli_prompt import set_top_screen as sts


def cli_config(show, key, value, set, reset):
    """설정 파일을 관리하는 명령어"""
    #TODO: 이거 cc config --set 선택지프로포트 구조 늘리거나 다시 설계

    # 설정 파일 조회
    if show:
        show_config()

    # 설정 값 변경: 명령어 기반
    if key and value:
        change_config(key, value)
        click.echo(f"'{key}' 값이 '{value}'로 설정되었습니다.")

    # 설정 값 변경: 선택 기반
    elif set:
        config_data = load_config()
        sts()

        # 선택지를 보여주기 위한 질문
        question = [
            inquirer.List(
                'Framework',
                message="어떤 테스트 프레임워크를 사용할까요?",
                choices=['unittest', 'pytest']
            ),
            inquirer.List(
                'Pipline',
                message="포함할 파이프라인 단계를 선택하세요",
                choices=['build', 'test', 'deploy']
            )
        ]

        answers = inquirer.prompt(question)

        # 선택한 값으로 설정 파일을 업데이트
        if answers:
            for key, value in answers.items():
                change_config(key, value)
            click.echo("설정 값이 변경되었습니다.")

    # 설정 파일 초기화
    if reset:
        reset_config()
        click.echo("설정이 초기화되었습니다.")
