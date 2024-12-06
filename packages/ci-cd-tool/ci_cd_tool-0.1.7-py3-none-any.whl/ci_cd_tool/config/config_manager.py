import yaml  # PyYAML 라이브러리
import os
import click
from rich import box
from rich.console import Console
from rich.panel import Panel

# 설정 파일 경로
# CONFIG_FILE = "ci_cd_tool/config/config_test.yml"
CONFIG_FILE = "ci_cd_tool/config/config.yml"
console = Console()



# 설정 파일 로드 함수
def load_config():
    """config.yml 파일을 로드"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f)
    else:
        return {}


# 설정 파일 저장 함수
def save_config(config):
    """config.yml 파일을 저장"""
    config_directory = os.path.dirname(CONFIG_FILE)
    if not os.path.exists(config_directory):
        os.makedirs(config_directory)  # 디렉토리 생성
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    click.echo(f"설정이 {CONFIG_FILE}에 저장되었습니다.")


# 설정 파일 조회 기능
def show_config():
    """설정 파일을 출력"""
    config_data = load_config()  # 설정 파일 로드 (예: config.yml에서)

    if config_data:
        console.print("\n[bold yellow]설정 파일 내용:[/]\n")

        # YAML 파일의 모든 키-값을 출력
        config_text = ""
        for key, value in config_data.items():
            config_text += f"[bold]{key}:[/bold] {str(value)}\n"

        # Panel로 전체 설정 내용 출력
        result_panel = Panel(
            config_text,
            title="[green bold]Config 설정 정보[/]",
            border_style="green",
            box=box.ROUNDED
        )
        console.print(result_panel)

    else:
        console.print("\n[red bold]설정 파일이 존재하지 않거나 비어 있습니다.[/]")
        console.print("[yellow]설정값을 다시 세팅 하시려면 \"cc init\" 명령어를 사용하세요.[/]")


# 설정 파일 값 변경 기능
def change_config(key, value):
    """설정 파일의 특정 값을 변경"""
    config_data = load_config()
    config_data[key] = value
    save_config(config_data)
    click.echo(f"'{key}' 값이 '{value}'로 설정되었습니다.")


# 설정 파일 초기화 기능
def reset_config():
    """설정 파일 초기화"""
    config_data = {}
    save_config(config_data)
    click.echo(f"{CONFIG_FILE} 파일이 초기화되었습니다.")