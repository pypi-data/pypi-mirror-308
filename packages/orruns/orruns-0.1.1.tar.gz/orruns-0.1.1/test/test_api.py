import pytest
import tempfile
import shutil
from pathlib import Path
import time
import json
from datetime import datetime
import pandas as pd

from orruns.api.experiment import ExperimentAPI
from orruns.tracker import ExperimentTracker
from orruns.core.config import Config

@pytest.fixture
def temp_dir():
    """创建临时目录"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def api(temp_dir):
    """创建API实例"""
    config = Config.get_instance()
    config.set_data_dir(temp_dir)
    return ExperimentAPI()

@pytest.fixture
def sample_experiment(api):
    """创建示例实验"""
    tracker = ExperimentTracker("test_exp", base_dir=api.config.get_data_dir())
    
    # 记录参数
    tracker.log_params({
        "learning_rate": 0.01,
        "batch_size": 32,
        "model": {
            "type": "cnn",
            "layers": [64, 32]
        }
    })
    
    # 记录指标
    tracker.log_metrics({
        "accuracy": 0.85,
        "loss": 0.15,
        "validation": {
            "accuracy": 0.83,
            "loss": 0.17
        }
    })
    
    # 记录CSV文件
    csv_content = "col1,col2\n1,2\n3,4"
    tracker.log_artifact("data.csv", csv_content, artifact_type="data")
    
    # 记录图像文件
    tracker.log_artifact("plot.png", b"fake_image_data", artifact_type="figure")
    
    # 等待文件写入完成
    time.sleep(0.1)
    
    return tracker

def test_list_experiments(api, sample_experiment):
    """测试列出实验"""
    # 等待文件写入完成
    time.sleep(0.1)
    
    experiments = api.list_experiments()
    assert len(experiments) > 0
    
    # 验证实验信息
    exp = next(e for e in experiments if e["name"] == "test_exp")
    assert len(exp["runs"]) == 1
    assert "params" in exp["runs"][0]
    assert "metrics" in exp["runs"][0]

def test_list_experiments_with_pattern(api, sample_experiment):
    """测试使用模式匹配列出实验"""
    # 创建额外的实验
    tracker2 = ExperimentTracker("test_exp_2", base_dir=api.config.get_data_dir())
    tracker2.log_params({"test": True})
    tracker2._save_experiment_info()  # 确保保存
    
    tracker3 = ExperimentTracker("other_exp", base_dir=api.config.get_data_dir())
    tracker3.log_params({"test": True})
    tracker3._save_experiment_info()  # 确保保存
    
    # 增加等待时间
    time.sleep(0.2)  # 增加等待时间
    
    # 使用模式匹配
    experiments = api.list_experiments(pattern="test_*")
    names = [exp["name"] for exp in experiments]
    assert "test_exp" in names
    assert "test_exp_2" in names
    assert "other_exp" not in names

def test_get_experiment(api, sample_experiment):
    """测试获取实验详情"""
    # 等待文件写入完成
    time.sleep(0.1)
    
    exp_info = api.get_experiment("test_exp")
    
    # 验证基本信息
    assert exp_info["name"] == "test_exp"
    assert len(exp_info["runs"]) == 1
    
    # 验证参数和指标
    latest_run = exp_info["latest_run"]
    assert latest_run["params"]["learning_rate"] == 0.01
    assert latest_run["metrics"]["accuracy"] == 0.85

def test_get_run(api, sample_experiment):
    """测试获取运行详情"""
    # 等待文件写入完成
    time.sleep(0.1)
    
    run_info = api.get_run("test_exp", sample_experiment.run_id)
    
    # 验证运行信息
    assert run_info["run"]["run_id"] == sample_experiment.run_id
    assert run_info["parameters"]["learning_rate"] == 0.01
    assert run_info["metrics"]["accuracy"] == 0.85

def test_query_experiments(api, sample_experiment):
    """测试查询实验"""
    # 创建一个新的实验并记录明确的测试数据
    tracker = ExperimentTracker("test_exp_query", base_dir=api.config.get_data_dir())
    
    # 记录参数并保存
    tracker.log_params({
        "learning_rate": 0.01,
        "batch_size": 32
    })
    tracker._save_experiment_info()  # 确保保存
    
    # 记录指标并保存
    tracker.log_metrics({
        "accuracy": 0.85,
        "loss": 0.15
    })
    tracker._save_experiment_info()  # 再次保存以更新指标
    
    # 增加等待时间
    time.sleep(0.2)
    
    # 参数过滤
    results = api.query_experiments(
        parameter_filters={
            "learning_rate__eq": 0.01  # 使用 __eq 操作符进行精确匹配
        }
    )
    assert len(results) > 0
    assert results[0]["parameters"]["learning_rate"] == 0.01

    # 指标过滤
    results = api.query_experiments(
        metric_filters={
            "accuracy__gte": 0.8  # 使用与参数过滤器相同的格式
        }
    )
    assert len(results) > 0
    assert results[0]["metrics"]["accuracy"] >= 0.8

def test_get_artifacts(api, sample_experiment):
    """测试获取文件工件列表"""
    # 等待文件写入完成
    time.sleep(0.1)
    
    artifacts = api.get_artifacts("test_exp", sample_experiment.run_id)
    
    # 验证文件列表
    assert "data.csv" in artifacts["data"]
    assert "plot.png" in artifacts["figures"]

def test_get_artifact_path(api, sample_experiment):
    """测试获取文件工件路径"""
    # 等待文件写入完成
    time.sleep(0.1)
    
    # 获取数据文件路径
    data_path = api.get_artifact_path(
        "test_exp",
        sample_experiment.run_id,
        "data.csv",
        artifact_type="data"
    )
    assert data_path.exists()
    with open(data_path, 'r', encoding='utf-8') as f:
        assert f.read() == "col1,col2\n1,2\n3,4"
    
    # 获取图像文件路径
    figure_path = api.get_artifact_path(
        "test_exp",
        sample_experiment.run_id,
        "plot.png",
        artifact_type="figure"
    )
    assert figure_path.exists()
    with open(figure_path, 'rb') as f:
        assert f.read() == b"fake_image_data"

def test_load_artifact(api, sample_experiment):
    """测试加载文件工件"""
    # 等待文件写入完成
    time.sleep(0.1)
    
    # 加载CSV文件
    data = api.load_artifact(
        "test_exp",
        sample_experiment.run_id,
        "data.csv",
        artifact_type="data"
    )
    # 检查是否为 DataFrame
    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ["col1", "col2"]

def test_error_handling(api):
    """测试错误处理"""
    # 测试不存在的实验
    with pytest.raises(FileNotFoundError):
        api.get_experiment("nonexistent")

    # 测试不存在的运行
    with pytest.raises(FileNotFoundError):
        api.get_run("nonexistent", "nonexistent_run")

    # 测试不存在的文件工件
    with pytest.raises(FileNotFoundError):
        api.get_artifact_path(
            "nonexistent",
            "nonexistent_run",
            "nonexistent.txt"
        )

    # 测试无效的查询条件
    with pytest.raises(ValueError):
        api.query_experiments(
            parameter_filters={"learning_rate__invalid": 0.1}
        )