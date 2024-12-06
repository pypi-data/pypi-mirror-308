# ModelPrep

A command-line tool for managing image datasets, optimized for training object detection models.

## Installation

```bash
# Quick install
pip install modelprep

# Development install
make develop
```

## Commands

### Dataset Management

```bash
# Show dataset information
modelprep show                  # Show all images and their properties
modelprep show --small-images   # Show only small images (<32x32)

# Remove images
modelprep remove --small-images # Remove small images (<32x32)
```

### Person Crop Operations

```bash
# Create and manage person crops
modelprep person-crop create --padding 20          # Create person crops with 20% padding
modelprep person-crop show                         # Show all person crops
modelprep person-crop show --sort-by-size          # Sort by size (large to small)
modelprep person-crop show --sort-by-size --reverse # Sort by size (small to large)

# Manage small person crops
modelprep person-crop show-small --min-size-kb 10 --min-pixels 100   # Preview small crops
modelprep person-crop remove-small --min-size-kb 10 --min-pixels 100 # Remove small crops

# Dataset integration
modelprep person-crop add-to-dataset --train-split 0.7 --valid-split 0.2 --test-split 0.1
modelprep person-crop remove-from-dataset
```

### Training YOLOv8 Models

```bash
# Basic training (auto-names with current date)
modelprep train

# Model size options
modelprep train --size nano    # Fastest training
modelprep train --size small   # Default
modelprep train --size medium  # Better accuracy
modelprep train --size large   # High accuracy
modelprep train --size xlarge  # Best accuracy

# Advanced training options
modelprep train \
    --size medium \           # Model size
    --epochs 300 \           # Number of epochs
    --batch 256 \            # Batch size (adjust for GPU)
    --img 640 \              # Image size
    --device 0 \             # GPU device (empty for auto)
    --project "my_project" \ # Project name
    --name "exp1"            # Experiment name

# Training management
modelprep train --resume                                    # Resume from last checkpoint
modelprep train --weights "runs/train/Nov14/weights/best.pt" # Resume from specific weights
modelprep train --val-only --weights "runs/train/best.pt"    # Validation only
modelprep train --nohup                                      # SSH-safe training

# Start training
modelprep train --nohup  # Creates nohup_train_Nov14.py and nohup_train_Nov14.log

# Monitor training
modelprep status                    # Show latest training status
modelprep status --name Nov14       # Show specific training status
modelprep status --follow           # Follow log output (like tail -f)
modelprep status -f -n Nov14 -n 100 # Follow specific training, show 100 lines
```

### Roboflow Integration

```bash
# Project management
modelprep roboflow create-project --project-name "my_project" \
    --project-type "object-detection" \
    --project-license "CC BY 4.0" \
    --annotation "object-detection"

# Upload datasets
modelprep roboflow upload --project-name "my_project" --dataset-name "person-crops"
```

## Features

- Complete dataset management and analysis
- Automated person cropping with annotation adjustment
- Size-based filtering and sorting
- YOLOv8 training optimized for small object detection
- SSH-safe training with nohup
- Roboflow integration for dataset management
- Rich CLI output with formatted tables

## Requirements

- Python 3.7+
- Ultralytics (YOLOv8)
- Pillow (PIL)
- Typer
- Rich
- Roboflow
- python-dotenv
- tqdm

## Development

```bash
# Installation
make help     # Show all make commands
make develop  # Install for development
make install  # Install for production
make clean    # Clean up everything
make format   # Format code

# Testing
make test              # Run all tests
make test-ci          # Run tests with coverage report
pytest tests/ -v      # Run tests directly

# Release Management
make release          # Create a new release
```

## Testing

```bash
# Install test dependencies
pip install -e
```

## License

MIT License