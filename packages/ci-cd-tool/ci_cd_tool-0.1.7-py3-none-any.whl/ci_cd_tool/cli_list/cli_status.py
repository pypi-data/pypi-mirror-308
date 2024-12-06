import click
import requests
from rich.console import Console
from rich.panel import Panel
from datetime import datetime
import os
import yaml

console = Console()


# 설정 파일 로드 함수
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yml')
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)


config = load_config()

# API 호출에 필요한 값 설정
base_url = config['ci_cd']['base_url']
token = config['ci_cd']['token']
repo_owner = config['repository']['owner']
repo_name = config['repository']['name']


def cli_status(env, details, limit):
    branch = config['environments'][env]['branch']
    console.print(Panel(f"[blue]{env} 환경의 파이프라인 상태 확인 중...[/blue]", title="파이프라인 상태", border_style="blue"))

    try:
        # API 호출 URL 구성
        url = f"{base_url}/repos/{repo_owner}/{repo_name}/actions/runs?branch={branch}&status=in_progress"
        headers = {'Authorization': f'token {token}'}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if len(data['workflow_runs']) == 0:
            console.print(Panel("[green]현재 실행 중인 파이프라인이 없습니다.[/green]", title="파이프라인 상태", border_style="green"))
        else:
            runs = data['workflow_runs'][:limit] if limit else data['workflow_runs']

            # 파이프라인 요약 정보
            success_count = len([run for run in runs if run.get('conclusion') == 'success'])
            failure_count = len([run for run in runs if run.get('conclusion') == 'failure'])
            in_progress_count = len([run for run in runs if run['status'] == 'in_progress'])
            console.print(
                Panel(f"성공: {success_count}, 실패: {failure_count}, 진행 중: {in_progress_count}", title="파이프라인 요약",
                      border_style="cyan"))

            for run in runs:
                status = run['status']
                conclusion = run.get('conclusion', '진행 중')
                commit_message = run['head_commit']['message'] if 'head_commit' in run else "N/A"
                run_id = run['id']
                run_url = run['html_url']
                actor = run['actor']['login'] if 'actor' in run else "N/A"

                details_msg = f"상태: {status}\n결과: {conclusion}\n커밋 메시지: {commit_message}\n실행 ID: {run_id}\n실행 링크: {run_url}\n실행자: {actor}"

                if details or config['output']['details']:
                    created_at = datetime.strptime(run['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                    updated_at = datetime.strptime(run['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
                    duration = updated_at - created_at
                    details_msg += f"\n시작 시간: {run['created_at']}\n업데이트 시간: {run['updated_at']}\n소요 시간: {duration}"

                    if config['pipeline']['fetch_job_details']:
                        jobs_response = requests.get(run['jobs_url'], headers=headers)
                        jobs_response.raise_for_status()
                        jobs_data = jobs_response.json()

                        if 'jobs' in jobs_data:
                            for job in jobs_data['jobs']:
                                job_name = job['name']
                                job_status = job['status']
                                job_conclusion = job.get('conclusion', '진행 중')
                                details_msg += f"\n  단계: {job_name}, 상태: {job_status}, 결과: {job_conclusion}"

                console.print(Panel(details_msg, title="파이프라인 정보", border_style="yellow"))
    except requests.exceptions.RequestException as e:
        console.print(Panel(f"[red]파이프라인 상태 확인 중 오류가 발생했습니다: {str(e)}[/red]", title="오류", border_style="red"))


if __name__ == '__main__':
    cli_status(env="dev", details=True, limit=3)
