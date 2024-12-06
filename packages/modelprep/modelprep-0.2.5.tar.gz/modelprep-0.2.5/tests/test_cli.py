from typer.testing import CliRunner
from modelprep.cli import app

runner = CliRunner()

def test_version():
    """Test version command."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "modelprep" in result.stdout.lower()

def test_show_help():
    """Test help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout

def test_train_help():
    """Test train help command."""
    result = runner.invoke(app, ["train", "--help"])
    assert result.exit_code == 0
    assert "train" in result.stdout.lower()
