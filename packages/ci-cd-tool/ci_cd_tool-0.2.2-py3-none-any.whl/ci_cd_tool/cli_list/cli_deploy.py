import click
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from rich.console import Console
from rich.panel import Panel

console = Console()

def cli_deploy(env):
    console.print(Panel(f"[blue]{env} 환경으로 배포 중...[/blue]", title="배포 진행", border_style="blue"))

    # AWS 배포 설정
    region_name = click.prompt("AWS Region", default='us-east-1')

    try:
        # S3에 파일 업로드 예제
        s3 = boto3.client('s3', region_name=region_name)
        bucket_name = click.prompt("S3 버킷 이름", type=str)
        file_path = click.prompt("업로드할 파일 경로", type=str)
        s3_key = click.prompt("S3에 저장할 파일 키", type=str)

        console.print(Panel(f"[yellow]S3 버킷 {bucket_name}에 파일 {file_path} 업로드 중...[/yellow]", title="S3 업로드", border_style="yellow"))
        s3.upload_file(file_path, bucket_name, s3_key)
        console.print(Panel("[green]파일 업로드 완료[/green]", title="업로드 결과", border_style="green"))

        # EC2 인스턴스 생성 예제
        ec2 = boto3.resource('ec2', region_name=region_name)
        instance_type = click.prompt("EC2 인스턴스 타입", default='t2.micro')
        #TODO: AMI ID를 사용자 입력으로 변경 or 사용가능한 AMI 목록 출력
        ami_id = click.prompt("AMI ID", default='ami-042e8287309f5df03')

        console.print(Panel("[yellow]EC2 인스턴스 생성 중...[/yellow]", title="EC2 생성", border_style="yellow"))
        instance = ec2.create_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1
        )
        console.print(Panel(f"[green]EC2 인스턴스 생성 완료: ID {instance[0].id}[/green]", title="EC2 결과", border_style="green"))

    except NoCredentialsError:
        console.print(Panel("[red]AWS 자격 증명이 올바르지 않습니다. 환경 변수를 확인해주세요.[/red]", title="오류", border_style="red"))
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDenied':
            console.print(Panel("[red]접근이 거부되었습니다. 권한을 확인하세요.[/red]", title="오류", border_style="red"))
        elif error_code == 'NoSuchBucket':
            console.print(Panel("[red]지정한 S3 버킷이 존재하지 않습니다. 버킷 이름을 확인하세요.[/red]", title="오류", border_style="red"))
        else:
            console.print(Panel(f"[red]AWS 클라이언트 오류: {str(e)}[/red]", title="오류", border_style="red"))
    except FileNotFoundError:
        console.print(Panel("[red]업로드할 파일을 찾을 수 없습니다. 경로를 확인하세요.[/red]", title="오류", border_style="red"))
    except Exception as e:
        console.print(Panel(f"[red]배포 중 오류가 발생했습니다: {str(e)}[/red]", title="오류", border_style="red"))

if __name__ == '__main__':
    cli_deploy("dev")