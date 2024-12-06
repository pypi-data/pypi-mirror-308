# 'test' 명령어 정의
import unittest
import os

import inquirer
from rich.console import Console
from rich.panel import Panel
from ci_cd_tool.cli_list.cli_init import ask_question

#TODO: 경로 하드코딩 바꾸삼
github_actions_file = '/src/ci_cd_tool/templates/templates/github_actions_ci.yml'  # GitHub Actions 설정 파일 경로
console = Console()

def cli_test(env, fast, report):
    """CI/CD 파이프라인에서 테스트를 실행하는 함수"""
    console.print(Panel(f"[blue]{env} 환경에서 테스트 실행 중...[/blue]", title="테스트 진행", border_style="blue"))

    # 빠른 테스트 모드로 유닛 테스트 일부 실행
    if fast:
        console.print(Panel("[yellow]빠른 테스트 모드 활성화: 일부 유닛 테스트 실행[/yellow]", title="테스트 모드", border_style="yellow"))
        test_dir = 'tests/fast'
    else:
        test_dir = 'tests'

    # 테스트 디렉토리 유효성 검사
    if not os.path.exists(test_dir):
        console.print(Panel(f"[red]테스트 디렉토리가 존재하지 않습니다: {test_dir}[/red]", title="오류", border_style="red"))
        return

    # unittest를 사용하여 테스트 실행
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 테스트 결과 출력
    if result.wasSuccessful():
        console.print(Panel("[green]모든 테스트가 성공했습니다![/green]", title="테스트 결과", border_style="green"))
        # GitHub Actions 파일에 테스트 추가 여부 묻기
        add_to_github_actions = ask_question(
            inquirer.List(
                'add_to_github_actions', message="GitHub Actions 설정 파일에 테스트 추가할까요?", choices=['yes','no']),
            "GitHub Actions 설정 파일 업데이트에 실패했습니다."
        )
        if add_to_github_actions == 'yes':
            add_test_to_github_actions(env, fast, report)
    else:
        console.print(Panel(f"[red]일부 테스트가 실패했습니다. 실패한 테스트 수: {len(result.failures)}[/red]", title="테스트 결과", border_style="red"))

    # 테스트 리포트 생성 옵션
    if report:
        report_file = os.path.join(test_dir, 'test_report.txt')
        with open(report_file, 'w') as f:
            suite = loader.discover(start_dir=test_dir)  # 테스트 스위트를 다시 로드하여 실행
            runner = unittest.TextTestRunner(stream=f, verbosity=2)
            runner.run(suite)
        console.print(Panel(f"[cyan]테스트 리포트가 생성되었습니다: {report_file}[/cyan]", title="리포트 생성", border_style="cyan"))

def add_test_to_github_actions(env, fast, report):
    """GitHub Actions 설정 파일에 테스트 추가"""
    new_block = ""
    if fast:
        new_block += "        python -m unittest discover -s tests/fast\n"
    else:
        new_block += "        python -m unittest discover -s tests\n"
    if report:
        new_block += "        python -m unittest discover -s tests --report\n"

    try:
        with open(github_actions_file, 'r+') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if '- name: Run Tests' in line:
                    # Run Tests 블록에 새로운 테스트 명령 추가
                    while i + 1 < len(lines) and lines[i + 1].strip().startswith('run: |'):
                        i += 1
                    lines.insert(i + 1, new_block)
                    break
            else:
                # Run Tests 블록이 없으면 새로 추가
                lines.append("\n    - name: Run Tests\n      run: |\n" + new_block)
            file.seek(0)
            file.writelines(lines)
        console.print(Panel(f"[green]GitHub Actions 설정 파일에 테스트 명령이 추가되었습니다.[/green]", title="GitHub Actions 업데이트", border_style="green"))
    except FileNotFoundError:
        console.print(Panel(f"[red]{github_actions_file} 파일을 찾을 수 없습니다.[/red]", title="오류", border_style="red"))
    except Exception as e:
        console.print(Panel(f"[red]GitHub Actions 업데이트 중 오류가 발생했습니다: {str(e)}[/red]", title="오류", border_style="red"))

# 예제 명령어 실행을 위해 함수 등록
if __name__ == '__main__':
    cli_test()