import sys
import os


# from ci_cd_tool.cli_list.cli_status import cli_status
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import click
from rich.console import Console
# from src.ci_cd_tool.cli_list import cli_init
# from src.ci_cd_tool.cli_list import cli_deploy
# from src.ci_cd_tool.cli_list import cli_test
from ci_cd_tool.cli_list import cli_init
from ci_cd_tool.cli_list import cli_deploy
from ci_cd_tool.cli_list import cli_test
from ci_cd_tool.cli_list import cli_config



set_config = {
    "Project_Root": None,
    "Pipline": None,
    "Framework": None,
    "ci_tool": None,
    "Remote_Repo": None
}

console = Console()


#config 명령어 정의
@click.command(help="설정 파일 조회 및 변경")
@click.option('--show', is_flag=True, help="현재 설정 파일을 조회")
@click.option('--set', is_flag=True, help="설정 값을 변경 (옵션 선택)")
@click.option('--reset', is_flag=True, help="설정 파일을 초기화")
@click.option('--key', type=str, help="설정 키 (예: Framework)")
@click.option('--value', type=str, help="설정 값 (예: unittest)")
def config(show, set, reset, key, value):
    cli_config.cli_config(show, key, value, set, reset)


# 'init' 명령어 정의
# @click.command(help="CI/CD 기본설정 및 초기화")
@click.command(help="CI/CD 기본설정 및 초기화", options_metavar='[no options available]')
def init():
    cli_init.cc_init(set_config)

# 'deploy' 명령어 정의
@click.command(help="환경별 배포 및 모니터링 설정// 변경함 기술적 문제있음")
@click.option('--env', type=str, default='dev', help="배포할 환경 설정 (예: dev, staging, prod)")
def deploy(env):
    cli_deploy.cli_deploy(env)


# 'monitor' 명령어 정의
# @click.command(help="배포된 애플리케이션 상태 모니터링")
# @click.option('--app', type=str, required=True, help="모니터링할 애플리케이션 이름")
# @click.option('--threshold', type=int, help="알림 임계값 설정")
# def monitor(app, threshold):
#     click.echo(f"{app} 애플리케이션 모니터링 중...")
#     if threshold:
#         click.echo(f"임계값 설정: {threshold}")


# 'status' 명령어 정의
@click.command(help="파이프라인 상태 확인")
@click.option('--env', type=str, default='prod', help="상태를 확인할 환경 설정 (예: dev, staging, prod)")
@click.option('--details', is_flag=True, help="파이프라인의 각 단계에 대한 상세 정보를 표시")
@click.option('--limit', type=int, help="최근 n개의 파이프라인 실행 내역만 표시")
def status(env, details, limit):
    cli_status(env, details, limit)


# 'rollback' 명령어 정의
# @click.command(help="특정 버전으로 롤백 또는 자동 롤백")
# @click.option('--version', type=str, required=True, help="롤백할 버전 지정")
# @click.option('--force', is_flag=True, help="강제 롤백")
# def rollback(version, force):
#     click.echo(f"버전 {version}으로 롤백 중...")
#     if force:
#         click.echo("강제 롤백 활성화")


# # 'versions' 명령어 정의
# @click.command(help="배포된 버전 목록 조회")
# def versions():
#     click.echo("배포된 버전 목록 조회 중...")


# 'test' 명령어 정의
@click.command(help="CI/CD 파이프라인에서 테스트 실행")
@click.option('--env', type=str, default='staging', help="테스트 실행 환경 설정 (예: dev, staging, prod)")
@click.option('--fast', is_flag=True, help="빠른 테스트 모드로 일부 테스트만 실행")
@click.option('--report', is_flag=True, help="테스트 결과 리포트를 생성")

def test(env, fast, report):
    cli_test.cli_test(env, fast, report)
    # click.echo(f"{env} 환경에서 테스트 실행 중...")
    # if fast:
    #     click.echo("빠른 테스트 모드 활성화")


# 'help' 명령어 정의 (click의 get_help() 기능을 사용하여 전체 명령어 설명 출력)
@click.command(help="Command별 도움말 출력")
# @click.group(context_settings=dict(help_option_names=['--help']))
@click.pass_context
def help(ctx):
    click.echo(ctx.parent.get_help())



# Main 함수 및 명령어 그룹 정의
@click.group()
# @click.group(context_settings=dict(help_option_names=['--help']))
def main():
    """메인 CLI 진입점"""
    pass


# 명령어들을 main 그룹에 추가
main.add_command(init)
main.add_command(deploy)
# main.add_command(monitor)
main.add_command(status)
# main.add_command(rollback)
# main.add_command(versions)
main.add_command(test)
main.add_command(config)
main.add_command(help)

if __name__ == '__main__':
    main()
