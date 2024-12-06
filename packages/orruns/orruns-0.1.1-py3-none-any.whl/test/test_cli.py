import pytest
from click.testing import CliRunner
import tempfile
import shutil
from pathlib import Path
import json
import time
from datetime import datetime

from orruns.cli.commands import cli
from orruns.tracker import ExperimentTracker
from orruns.core.config import Config

@pytest.fixture
def runner():
    """创建CLI测试运行器"""
    return CliRunner()

@pytest.fixture
def temp_dir():
    """创建临时目录"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def config(temp_dir):
    """设置测试配置"""
    config = Config.get_instance()
    old_dir = config.get_data_dir()  # 保存原始目录
    config.set_data_dir(temp_dir)
    yield config
    config.set_data_dir(old_dir)  # 恢复原始目录

@pytest.fixture
def sample_experiment(temp_dir):
    """创建示例实验数据"""
    tracker = ExperimentTracker("test_exp", base_dir=temp_dir)
    
    # 记录参数和指标
    params = {
        "param1": 1,
        "param2": "test"
    }
    metrics = {
        "metric1": 0.5,
        "metric2": 100
    }
    
    # 使用 tracker 的方法记录参数和指标
    tracker.log_params(params)
    tracker.log_metrics(metrics)
    
    # 等待文件写入完成
    time.sleep(0.5)
    
    return tracker

def test_config_commands(runner, temp_dir):
    """测试配置相关命令"""
    # 测试设置数据目录
    result = runner.invoke(cli, ['config', 'data-dir', temp_dir])
    assert result.exit_code == 0
    assert f"数据目录已设置为: {temp_dir}" in result.output
    
    # 测试显示配置
    result = runner.invoke(cli, ['config', 'show'])
    assert result.exit_code == 0
    assert temp_dir in result.output
    assert "版本:" in result.output

def test_list_command(runner, config, sample_experiment):
    """测试列出实验命令"""
    # 等待文件写入完成
    time.sleep(0.1)
    
    # 测试简略列表
    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert "test_exp" in result.output
    
    # 测试详细列表
    result = runner.invoke(cli, ['list', '--detailed'])
    assert result.exit_code == 0
    assert "test_exp" in result.output
    # 检查参数是否在输出中，使用更灵活的检查方式
    output = result.output.replace(" ", "")
    assert any(x in output for x in [
        "'param1':1",
        "param1:1",
        '"param1":1',
        "{'param1':1"
    ])
    
    # 测试模式匹配
    result = runner.invoke(cli, ['list', '--pattern', 'test_*'])
    assert result.exit_code == 0
    assert "test_exp" in result.output
    
    # 测试不存在的模式
    result = runner.invoke(cli, ['list', '--pattern', 'nonexistent_*'])
    assert result.exit_code == 0
    assert "没有找到匹配模式 'nonexistent_*' 的实验" in result.output

def test_info_command(runner, config, sample_experiment):
    """测试查看实验信息命令"""
    # 等待文件写入完成
    time.sleep(0.1)
    
    # 测试查看实验概览
    result = runner.invoke(cli, ['info', 'test_exp'])
    assert result.exit_code == 0
    assert "test_exp" in result.output
    assert "总运行次数" in result.output
    
    # 检查参数和指标，使用更灵活的检查方式
    output = result.output.replace(" ", "")
    assert any(x in output for x in [
        "'param1':1",
        "param1:1",
        '"param1":1',
        "{'param1':1"
    ])
    
    # 测试查看特定运行
    result = runner.invoke(cli, ['info', 'test_exp', '--run-id', sample_experiment.run_id])
    assert result.exit_code == 0
    assert sample_experiment.run_id in result.output
    output = result.output.replace(" ", "")
    assert "param1:1" in output

def test_delete_command(runner, config, sample_experiment):
    """测试删除命令"""
    # 等待文件写入完成
    time.sleep(0.1)
    
    # 测试删除确认
    result = runner.invoke(cli, ['delete', 'test_exp'], input='n\n')
    assert result.exit_code == 0
    assert "操作已取消" in result.output
    
    # 测试强制删除
    result = runner.invoke(cli, ['delete', 'test_exp', '--force'])
    assert result.exit_code == 0
    assert "已删除实验" in result.output
    
    # 验证实验已被删除
    result = runner.invoke(cli, ['list'])
    assert "test_exp" not in result.output
    
    # 测试删除不存在的实验
    result = runner.invoke(cli, ['delete', 'nonexistent', '--force'])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()

def test_error_handling(runner):
    """测试错误处理"""
    config = Config.get_instance()
    old_dir = config.get_data_dir()  # 保存原始目录
    
    try:
        # 使用不存在的目录
        nonexistent_dir = str(Path(tempfile.mkdtemp()) / "nonexistent")
        shutil.rmtree(nonexistent_dir, ignore_errors=True)  # 确保目录不存在
        config.set_data_dir(nonexistent_dir)
        
        result = runner.invoke(cli, ['list'])
        assert "没有找到任何实验" in result.output
        
    finally:
        # 恢复原始目录
        config.set_data_dir(old_dir)

def test_format_helpers(runner, config, sample_experiment):
    """测试格式化辅助函数"""
    # 等待文件写入完成
    time.sleep(0.1)
    
    result = runner.invoke(cli, ['info', 'test_exp'])
    assert result.exit_code == 0
    
    # 验证时间格式化
    assert "20" in result.output  # 年份
    assert ":" in result.output   # 时间分隔符
    
    # 验证指标格式化，使用更灵活的检查方式
    output = result.output.replace(" ", "")
    assert any(x in output for x in ["metric1:0.5", "metric1=0.5"])
    assert any(x in output for x in ["metric2:100", "metric2=100"])