import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import json
import pytest
from pathlib import Path
from orruns.tracker import ExperimentTracker
from orruns import ExperimentTracker
from orruns.core.config import Config
import time

@pytest.fixture
def temp_dir():
    """创建临时目录"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def tracker(temp_dir):
    """创建实验追踪器实例"""
    return ExperimentTracker("test_experiment", base_dir=temp_dir)

def test_init(tracker, temp_dir):
    """测试初始化"""
    assert tracker.experiment_name == "test_experiment"
    assert tracker.base_dir == Path(temp_dir)
    assert tracker.run_dir.exists()
    assert tracker.params_dir.exists()
    assert tracker.metrics_dir.exists()
    assert tracker.artifacts_dir.exists()
def test_log_params(tracker):
    """测试参数记录，包括嵌套字典"""
    # 测试基本参数
    params = {
        "learning_rate": 0.001,
        "batch_size": 32
    }
    tracker.log_params(params)
    
    # 验证基本参数
    saved_params = tracker.get_params()
    assert saved_params == params
    
    # 测试嵌套字典
    nested_params = {
        "optimizer": {
            "name": "adam",
            "settings": {
                "beta1": 0.9,
                "beta2": 0.999
            }
        },
        "scheduler": {
            "name": "cosine",
            "settings": {
                "T_max": 100,
                "eta_min": 1e-6
            }
        }
    }
    tracker.log_params(nested_params)
    
    # 验证嵌套参数
    saved_params = tracker.get_params()
    assert saved_params["optimizer"]["name"] == "adam"
    assert saved_params["optimizer"]["settings"]["beta1"] == 0.9
    assert saved_params["scheduler"]["settings"]["T_max"] == 100
    
    # 测试使用前缀
    prefixed_params = {
        "weight_decay": 0.01,
        "momentum": 0.9
    }
    tracker.log_params(prefixed_params, prefix="optimizer.settings")
    
    # 验证前缀参数
    saved_params = tracker.get_params()
    assert saved_params["optimizer"]["settings"]["weight_decay"] == 0.01
    assert saved_params["optimizer"]["settings"]["momentum"] == 0.9
    
    # 验证文件保存
    params_file = tracker.params_dir / "params.json"
    assert params_file.exists()
    
    # 验证文件内容
    with open(params_file, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert saved_data["optimizer"]["settings"]["weight_decay"] == 0.01

def test_log_metrics(tracker):
    """测试指标记录，包括嵌套指标"""
    # 测试单次记录
    metrics = {
        "loss": 0.5, 
        "accuracy": 0.95
    }
    tracker.log_metrics(metrics)
    saved_metrics = tracker.get_metrics()
    assert saved_metrics["loss"] == 0.5
    assert saved_metrics["accuracy"] == 0.95
    
    # 测试嵌套指标
    nested_metrics = {
        "train": {
            "loss": 0.4,
            "metrics": {
                "accuracy": 0.96,
                "f1_score": 0.94
            }
        },
        "val": {
            "loss": 0.45,
            "metrics": {
                "accuracy": 0.93,
                "f1_score": 0.92
            }
        }
    }
    tracker.log_metrics(nested_metrics)
    
    # 验证嵌套指标
    saved_metrics = tracker.get_metrics()
    assert saved_metrics["train"]["loss"] == 0.4
    assert saved_metrics["train"]["metrics"]["accuracy"] == 0.96
    assert saved_metrics["val"]["metrics"]["f1_score"] == 0.92
    
    # 测试带步骤的记录
    tracker.log_metrics({"train": {"loss": 0.3}}, step=1)
    tracker.log_metrics({"train": {"loss": 0.2}}, step=2)
    saved_metrics = tracker.get_metrics()
    assert saved_metrics["train"]["loss"]["steps"] == [1, 2]
    assert saved_metrics["train"]["loss"]["values"] == [0.3, 0.2]
    
    # 测试使用前缀的嵌套指标
    tracker.log_metrics(
        {"accuracy": 0.97, "f1_score": 0.95}, 
        prefix="train.metrics",
        step=3
    )
    saved_metrics = tracker.get_metrics()
    assert saved_metrics["train"]["metrics"]["accuracy"]["steps"] == [3]
    assert saved_metrics["train"]["metrics"]["accuracy"]["values"] == [0.97]

def test_invalid_metrics(tracker):
    """测试无效指标值处理"""
    # 测试非数值类型
    with pytest.raises(ValueError):
        tracker.log_metrics({"invalid": "not a number"})
    
    # 测试嵌套字典中的非数值类型
    with pytest.raises(ValueError):
        tracker.log_metrics({
            "train": {
                "metrics": {
                    "invalid": ["not", "a", "number"]
                }
            }
        })
    
    # 测试使用前缀的非数值类型
    with pytest.raises(ValueError):
        tracker.log_metrics(
            {"invalid": {"nested": "not a number"}},
            prefix="train"
        )

def test_deep_update(tracker):
    """测试深度更新功能"""
    # 初始参数
    initial_params = {
        "model": {
            "layers": [64, 32],
            "activation": "relu"
        }
    }
    tracker.log_params(initial_params)
    
    # 更新部分参数
    update_params = {
        "model": {
            "layers": [128, 64, 32],
            "dropout": 0.5
        }
    }
    tracker.log_params(update_params)
    
    # 验证更新结果
    saved_params = tracker.get_params()
    assert saved_params["model"]["layers"] == [128, 64, 32]
    assert saved_params["model"]["activation"] == "relu"
    assert saved_params["model"]["dropout"] == 0.5

def test_log_artifact(tracker):
    """测试文件工件记录"""
    # 测试CSV文件
    data = "col1,col2\n1,2\n3,4"
    tracker.log_artifact("data.csv", data, artifact_type="data")
    
    # 验证CSV文件
    csv_path = tracker.data_dir / "data.csv"
    assert csv_path.exists(), f"CSV file not found at {csv_path}"
    with open(csv_path, 'r', encoding='utf-8') as f:
        assert f.read() == data
    
    # 测试图像文件
    image_data = b"fake_image_data"
    tracker.log_artifact("plot.png", image_data, artifact_type="figure")
    
    # 验证图像文件
    png_path = tracker.figures_dir / "plot.png"
    assert png_path.exists(), f"PNG file not found at {png_path}"
    with open(png_path, 'rb') as f:
        assert f.read() == image_data
    
    # 验证文件列表
    artifacts = tracker.get_artifacts()  # 使用实例方法
    assert "data.csv" in artifacts["data"]
    assert "plot.png" in artifacts["figures"]

@pytest.mark.parametrize("experiment_name,expected_runs", [
    ("test_exp_1", 2),
    ("test_exp_2", 1),
])
def test_list_experiments(temp_dir, experiment_name, expected_runs):
    """测试实验列表"""
    # 创建测试实验
    for _ in range(expected_runs):
        tracker = ExperimentTracker(experiment_name, base_dir=temp_dir)
        tracker.log_params({"test": True})
    
    experiments = ExperimentTracker.list_experiments(base_dir=temp_dir)
    exp = next(e for e in experiments if e["name"] == experiment_name)
    assert len(exp["runs"]) == expected_runs

def test_query_experiments(temp_dir):
    """测试实验查询"""
    # 创建测试数据
    tracker1 = ExperimentTracker("exp1", base_dir=temp_dir)
    tracker1.log_params({"learning_rate": 0.1})
    tracker1.log_metrics({"accuracy": 0.9})
    
    tracker2 = ExperimentTracker("exp2", base_dir=temp_dir)
    tracker2.log_params({"learning_rate": 0.01})
    tracker2.log_metrics({"accuracy": 0.95})
    
    # 等待文件写入完成
    time.sleep(0.1)
    
    # 测试参数过滤
    results = ExperimentTracker.query_experiments(
        base_dir=temp_dir,
        parameter_filters={"learning_rate__gt": 0.05}
    )
    assert len(results) == 1
    assert results[0]["parameters"]["learning_rate"] == 0.1

def test_get_experiment(temp_dir):
    """测试获取实验详情"""
    # 创建测试实验
    tracker = ExperimentTracker("test_exp", base_dir=temp_dir)
    tracker.log_params({"param1": 1})
    tracker.log_metrics({"metric1": 0.5})
    
    # 获取实验详情
    exp_info = ExperimentTracker.get_experiment("test_exp", base_dir=temp_dir)
    assert exp_info["name"] == "test_exp"
    assert exp_info["parameters"] == {"param1": 1}
    assert exp_info["metrics"] == {"metric1": 0.5}

def test_get_artifacts(temp_dir):
    """测试获取文件工件"""
    # 创建测试实验和文件
    tracker = ExperimentTracker("test_exp", base_dir=temp_dir)
    
    # 创建测试文件
    csv_content = "col1,col2\n1,2\n3,4"
    tracker.log_artifact("data.csv", csv_content, artifact_type="data")
    
    png_content = b"fake_image_data"
    tracker.log_artifact("plot.png", png_content, artifact_type="figure")
    
    # 等待文件写入完成
    time.sleep(0.1)
    
    # 获取文件列表
    artifacts = tracker.get_artifacts()  # 使用实例方法
    assert "data.csv" in artifacts["data"]
    assert "plot.png" in artifacts["figures"]
    
    # 也可以使用类方法
    artifacts = ExperimentTracker.list_artifacts(
        "test_exp",
        tracker.run_id,
        base_dir=temp_dir
    )
    assert "data.csv" in artifacts["data"]
    assert "plot.png" in artifacts["figures"]
    
    # 验证文件内容
    data_path = tracker.data_dir / "data.csv"
    with open(data_path, 'r', encoding='utf-8') as f:
        assert f.read() == csv_content
        
    figure_path = tracker.figures_dir / "plot.png"
    with open(figure_path, 'rb') as f:
        assert f.read() == png_content

def test_error_handling(temp_dir):
    """测试错误处理"""
    # 测试不存在的实验
    with pytest.raises(FileNotFoundError):
        ExperimentTracker.get_experiment("nonexistent", base_dir=temp_dir)
    
    # 测试无效的指标格式
    tracker = ExperimentTracker("test_exp", base_dir=temp_dir)
    with pytest.raises(ValueError):
        tracker.log_metrics({"metric": "invalid"})  # 应该是数字