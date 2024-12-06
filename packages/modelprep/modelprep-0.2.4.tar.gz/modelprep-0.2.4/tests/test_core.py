import pytest
from pathlib import Path
from modelprep.core import (
    collect_files_recursively,
    check_existing_training
)

def test_check_training_status():
    """Test training status check."""
    # Test non-existent training
    assert check_existing_training("nonexistent") == False

def test_collect_files(tmp_path):
    """Test file collection with temporary directory."""
    # Create test files
    image_dir = tmp_path / "images"
    image_dir.mkdir()

    # Create test image and label
    (image_dir / "test.jpg").touch()
    (image_dir / "test.txt").touch()

    images, labels = collect_files_recursively(image_dir)

    assert len(images) == 1
    assert "test" in labels
