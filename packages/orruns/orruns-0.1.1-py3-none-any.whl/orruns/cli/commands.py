import click
import os
from typing import Optional
from tabulate import tabulate
from datetime import datetime
from ..core.config import Config
from ..tracker import ExperimentTracker

VERSION = "0.1.0"  # 版本号

@click.group()
@click.version_option(version=VERSION, prog_name="ORRuns")
def cli():
    """ORRuns 实验管理工具"""
    pass

@cli.group()
def config():
    """配置管理"""
    pass

def format_time(timestamp_str: str) -> str:
    """格式化时间戳"""
    try:
        timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S_%f")
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str

def format_metrics(metrics: dict) -> str:
    """格式化指标"""
    if not metrics:
        return "N/A"
    return "; ".join(f"{k}: {v}" for k, v in metrics.items())

@cli.command()
@click.option('--last', '-l', default=10, help='显示最近n个实验')
@click.option('--pattern', '-p', default=None, help='实验名称匹配模式')
@click.option('--detailed/--no-detailed', '-d/-nd', default=False, help='是否显示详细信息')
def list(last: int, pattern: Optional[str], detailed: bool):
    """列出实验"""
    try:
        config = Config.get_instance()
        if not config.get_data_dir():
            raise click.ClickException("数据目录未设置。请先运行 'orruns config data-dir PATH' 设置数据目录。")

        experiments = ExperimentTracker.list_experiments(
            base_dir=config.get_data_dir()
        )

        if not experiments:
            click.echo("没有找到任何实验")
            return

        # 过滤实验
        if pattern:
            import fnmatch
            experiments = [
                exp for exp in experiments 
                if fnmatch.fnmatch(exp['name'].lower(), pattern.lower())
            ]
            
            if not experiments:
                click.echo(f"没有找到匹配模式 '{pattern}' 的实验")
                return

        # 限制显示数量
        experiments = experiments[:last]

        if detailed:
            # 详细视图
            for exp in experiments:
                click.echo(f"\n实验名称: {exp['name']}")
                click.echo("运行记录:")
                headers = ["运行ID", "时间", "参数", "指标"]
                table_data = [
                    [
                        run['run_id'],
                        format_time(run['timestamp']),
                        str(run.get('params', {})),
                        format_metrics(run.get('metrics', {}))
                    ]
                    for run in exp['runs'][:5]
                ]
                click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            # 简略视图
            headers = ["实验名称", "运行次数", "最近运行时间"]
            table_data = [
                [
                    exp['name'],
                    len(exp['runs']),
                    format_time(exp['runs'][0]['timestamp']) if exp['runs'] else "N/A"
                ]
                for exp in experiments
            ]
            click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))

    except Exception as e:
        raise click.ClickException(str(e))

@cli.command()
@click.argument('experiment_name')
@click.option('--run-id', '-r', help='特定运行ID')
def info(experiment_name: str, run_id: Optional[str]):
    """查看实验详细信息"""
    try:
        config = Config.get_instance()
        exp_info = ExperimentTracker.get_experiment(
            experiment_name=experiment_name,
            base_dir=config.get_data_dir(),
            run_id=run_id
        )
        
        if run_id:
            # 显示特定运行的详细信息
            run = exp_info['run']
            click.echo(f"\n运行ID: {run['run_id']}")
            click.echo(f"时间: {format_time(run['timestamp'])}")
            click.echo("\n参数:")
            for k, v in run.get('params', {}).items():
                click.echo(f"  {k}: {v}")
            click.echo("\n指标:")
            for k, v in run.get('metrics', {}).items():
                click.echo(f"  {k}: {v}")
        else:
            # 显示实验概览
            click.echo(f"\n实验名称: {exp_info['name']}")
            click.echo(f"总运行次数: {exp_info['total_runs']}")
            click.echo(f"最近运行时间: {exp_info['last_updated']}")
            
            # 显示最近的运行记录
            click.echo("\n最近的运行记录:")
            headers = ["运行ID", "时间", "参数", "指标"]
            table_data = [
                [
                    run['run_id'],
                    format_time(run['timestamp']),
                    str(run.get('params', {})),
                    format_metrics(run.get('metrics', {}))
                ]
                for run in exp_info['runs'][:5]  # 只显示最近5次运行
            ]
            click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
            
    except Exception as e:
        raise click.ClickException(str(e))

@cli.command()
@click.argument('experiment_name')
@click.option('--run-id', '-r', help='特定运行ID')
@click.option('--force/--no-force', '-f/-nf', default=False, help='强制删除，不提示确认')
def delete(experiment_name: str, run_id: Optional[str], force: bool):
    """删除实验或特定运行"""
    try:
        if not force:
            msg = f"确定要删除实验 '{experiment_name}'"
            if run_id:
                msg += f" 的运行 '{run_id}'"
            msg += "? [y/N]: "
            
            if not click.confirm(msg):
                click.echo("操作已取消")
                return

        config = Config.get_instance()
        ExperimentTracker.delete_experiment(
            experiment_name=experiment_name,
            base_dir=config.get_data_dir(),
            run_id=run_id
        )
        
        if run_id:
            click.echo(f"已删除实验 '{experiment_name}' 的运行 '{run_id}'")
        else:
            click.echo(f"已删除实验 '{experiment_name}'")
            
    except Exception as e:
        raise click.ClickException(str(e))

@config.command()
@click.argument('path', type=click.Path())
def data_dir(path):
    """设置实验数据目录"""
    try:
        # 创建目录（如果不存在）
        os.makedirs(path, exist_ok=True)
        
        config = Config.get_instance()
        config.set_data_dir(path)
        click.echo(f"数据目录已设置为: {path}")
    except Exception as e:
        raise click.ClickException(f"设置数据目录失败: {str(e)}")

@config.command()
def show():
    """显示当前配置"""
    try:
        config = Config.get_instance()
        data_dir = config.get_data_dir()
        
        click.echo("\n当前配置:")
        click.echo(f"数据目录: {data_dir or '未设置'}")
        click.echo(f"版本: {VERSION}")
    except Exception as e:
        raise click.ClickException(str(e))