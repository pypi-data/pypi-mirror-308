import typer
from rich import print
from typing import Optional
from . import core
from roboflow import Roboflow
from datetime import datetime
from . import __version__

app = typer.Typer(help="ModelPrep: A tool for managing image datasets")

def version_callback(value: bool):
    if value:
        typer.echo(f"modelprep version: {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=version_callback,
        is_eager=True,
    )
):
    """
    ModelPrep CLI tool for managing and analyzing image datasets.
    """
    return

@app.command()
def show(
    small_images: bool = typer.Option(False, "--small-images", help="Show only small images"),
):
    """Show dataset information and statistics."""
    if small_images:
        core.show_small_images()
    else:
        core.show_all()

@app.command()
def remove(
    small_images: bool = typer.Option(False, "--small-images", help="Remove small images"),
):
    """Remove images based on specified criteria."""
    if small_images:
        core.remove_small_images()
    else:
        print("[red]Please specify what to remove using --small-images[/red]")

@app.command("train")
def train_model(
    model_size: str = typer.Option("small", "--size", "-s",
        help="Model size: nano, small, medium, large, xlarge"),
    epochs: int = typer.Option(300, "--epochs", "-e",
        help="Number of training epochs"),
    batch_size: int = typer.Option(256, "--batch", "-b",
        help="Batch size"),
    image_size: int = typer.Option(640, "--img", "-i",
        help="Image size"),
    device: str = typer.Option("", "--device", "-d",
        help="Device to train on (empty for auto)"),
    project_name: str = typer.Option("runs/train", "--project", "-p",
        help="Project name"),
    name: str = typer.Option("", "--name", "-n",
        help="Experiment name (default: current date)"),
    resume: bool = typer.Option(False, "--resume",
        help="Resume training from last checkpoint"),
    validation_only: bool = typer.Option(False, "--val-only",
        help="Run validation only"),
    nohup: bool = typer.Option(False, "--nohup",
        help="Run training with nohup"),
    weights: str = typer.Option("", "--weights",
        help="Path to weights file to resume from"),
):
    """Train YOLOv8 model optimized for small object detection."""
    # Generate default experiment name if not provided
    if not name:
        name = datetime.now().strftime("%b%d")  # e.g., Nov14

    core.train_yolo_model(
        model_size=model_size,
        epochs=epochs,
        batch_size=batch_size,
        image_size=image_size,
        device=device,
        project_name=project_name,
        name=name,
        resume=resume,
        validation_only=validation_only,
        nohup=nohup,
        weights=weights
    )

@app.command("status")
def training_status(
    name: str = typer.Option(None, "--name", "-n", help="Training name (e.g., Nov14)"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow log output"),
    lines: int = typer.Option(50, "--lines", "-n", help="Number of lines to show")
):
    """Show status of training jobs."""
    core.get_training_status(name=name, follow=follow, lines=lines)

person_crop_app = typer.Typer()
app.add_typer(person_crop_app, name="person-crop", help="Person cropping operations")

@person_crop_app.command("create")
def person_crop_create(
    padding: int = typer.Option(20, help="Padding percentage around person crop"),
):
    """Create person crops with adjusted annotations."""
    core.create_person_crops(padding_percent=padding)

@person_crop_app.command("show")
def person_crop_show(
    sort_by_size: bool = typer.Option(False, "--sort-by-size", help="Sort images by size"),
    reverse: bool = typer.Option(False, "--reverse", help="Reverse the sorting order")
):
    """Show details of all person crops."""
    core.show_person_crops(sort_by_size=sort_by_size, reverse=reverse)

@person_crop_app.command("show-small")
def show_small_crops(
    min_size_kb: float = typer.Option(10.0, help="Minimum file size in KB"),
    min_pixels: int = typer.Option(100, help="Minimum width/height in pixels"),
):
    """Show person crops that are smaller than specified size thresholds."""
    core.show_small_crops(min_size_kb=min_size_kb, min_pixels=min_pixels)

@person_crop_app.command("remove-small")
def remove_small_crops(
    min_size_kb: float = typer.Option(10.0, help="Minimum file size in KB"),
    min_pixels: int = typer.Option(100, help="Minimum width/height in pixels"),
):
    """Remove person crops that are smaller than specified size thresholds."""
    core.remove_small_crops(min_size_kb=min_size_kb, min_pixels=min_pixels)

@person_crop_app.command("add-to-dataset")
def add_person_crops_to_dataset(
    train_split: float = typer.Option(0.7, help="Percentage of data for training"),
    valid_split: float = typer.Option(0.2, help="Percentage of data for validation"),
    test_split: float = typer.Option(0.1, help="Percentage of data for testing"),
):
    """Add person crops to the dataset with train/valid/test split."""
    core.add_person_crops_to_dataset(train_split, valid_split, test_split)

@person_crop_app.command("remove-from-dataset")
def remove_person_crops_from_dataset():
    """Remove all person crops from the dataset."""
    core.remove_person_crops_from_dataset()

roboflow_app = typer.Typer()
app.add_typer(roboflow_app, name="roboflow", help="Roboflow operations")

@roboflow_app.command("create-project")
def create_roboflow_project(
    project_name: str = typer.Option(..., prompt=True, help="Project name"),
    project_type: str = typer.Option("object-detection", help="Project type"),
    project_license: str = typer.Option("CC BY 4.0", help="Project license"),
    annotation: str = typer.Option("object-detection", help="Annotation type"),
):
    """Create a new project on Roboflow."""
    api_key = core.get_or_prompt_api_key()
    core.create_roboflow_project(
        api_key,
        project_name,
        project_type,
        project_license,
        annotation
    )

@roboflow_app.command("upload")
def upload_to_roboflow(
    project_name: str = typer.Option(..., prompt=True, help="Project name"),
    dataset_name: str = typer.Option("person-crops", help="Dataset name for this upload"),
):
    """Upload person crops to Roboflow project."""
    api_key = core.get_or_prompt_api_key()
    core.upload_to_roboflow(api_key, project_name, dataset_name)

if __name__ == "__main__":
    app()