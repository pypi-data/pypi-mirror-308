from pathlib import Path
from PIL import Image
from rich import print
from rich.table import Table
from typing import List, Dict, Tuple, Optional
import numpy as np
from ultralytics import YOLO
import shutil
from tqdm import tqdm
from roboflow import Roboflow
from dotenv import load_dotenv, set_key
import os
import yaml
import subprocess
import sys
from rich.live import Live
from datetime import datetime
import time
import psutil

SMALL_IMAGE_THRESHOLD = (32, 32)  # Define what constitutes a "small" image

def collect_files_recursively(directory: Path = Path.cwd()) -> Tuple[List[Path], Dict[str, Path]]:
    """
    Recursively collect all images and label files, matching them by name.
    Returns (image_files, label_dict) where label_dict maps image stem to label path.
    """
    print("[blue]Collecting files recursively...[/blue]")

    # Collect all images
    image_files = []
    for ext in ('*.jpg', '*.jpeg', '*.png'):
        for file in directory.rglob(ext):
            if 'person_crops' not in file.parts:
                image_files.append(file)

    print(f"[blue]Found {len(image_files)} images[/blue]")

    # Collect all label files
    label_dict = {}
    for label_file in tqdm(directory.rglob('*.txt'), desc="Collecting labels"):
        if 'person_crops' not in label_file.parts:
            # Store mapping of image name to label path
            label_dict[label_file.stem] = label_file

    print(f"[blue]Found {len(label_dict)} label files[/blue]")

    # Filter images that have matching labels
    valid_images = []
    for img_path in image_files:
        if img_path.stem in label_dict:
            valid_images.append(img_path)

    print(f"[blue]Found {len(valid_images)} images with matching labels[/blue]")

    return valid_images, label_dict

def show_all():
    """Show all dataset information."""
    images = collect_files_recursively()
    table = Table(title="Dataset Overview")
    table.add_column("File")
    table.add_column("Dimensions")
    table.add_column("Size (KB)")

    for img_path in images:
        with Image.open(img_path) as img:
            size_kb = img_path.stat().st_size / 1024
            table.add_row(
                str(img_path),
                f"{img.size[0]}x{img.size[1]}",
                f"{size_kb:.1f}"
            )

    print(table)

def show_small_images():
    """Show small images in the dataset."""
    images = collect_files_recursively()
    small_images = []

    for img_path in images:
        with Image.open(img_path) as img:
            if img.size[0] < SMALL_IMAGE_THRESHOLD[0] or img.size[1] < SMALL_IMAGE_THRESHOLD[1]:
                small_images.append((img_path, img.size))

    if small_images:
        table = Table(title="Small Images")
        table.add_column("File")
        table.add_column("Dimensions")

        for img_path, size in small_images:
            table.add_row(str(img_path), f"{size[0]}x{size[1]}")

        print(table)
    else:
        print("[green]No small images found![/green]")

def remove_small_images():
    """Remove small images from the dataset."""
    images = collect_files_recursively()
    removed = 0

    for img_path in images:
        with Image.open(img_path) as img:
            if img.size[0] < SMALL_IMAGE_THRESHOLD[0] or img.size[1] < SMALL_IMAGE_THRESHOLD[1]:
                img_path.unlink()
                removed += 1

    print(f"[green]Removed {removed} small images[/green]")

def load_yolo_labels(label_path: Path) -> list:
    """Load YOLO format labels."""
    if not label_path.exists():
        return []

    labels = []
    with open(label_path, 'r') as f:
        for line in f:
            labels.append(line.strip().split())
    return labels

def save_yolo_labels(labels: list, path: Path):
    """Save YOLO format labels."""
    with open(path, 'w') as f:
        for label in labels:
            f.write(' '.join(map(str, label)) + '\n')

def adjust_bbox_coordinates(bbox, crop_box, orig_size):
    """
    Adjust bounding box coordinates for cropped image.
    Both input and output are in YOLO format (normalized coordinates).

    Args:
        bbox: Original bbox [x_center, y_center, width, height] (normalized)
        crop_box: Crop coordinates [x1, y1, x2, y2] (absolute pixels)
        orig_size: Original image size (width, height)
    """
    orig_w, orig_h = orig_size
    x_center, y_center, width, height = bbox
    crop_x1, crop_y1, crop_x2, crop_y2 = crop_box

    # Get crop dimensions
    crop_w = crop_x2 - crop_x1
    crop_h = crop_y2 - crop_y1

    # Convert normalized bbox to absolute pixels
    abs_x = x_center * orig_w
    abs_y = y_center * orig_h
    abs_w = width * orig_w
    abs_h = height * orig_h

    # Adjust coordinates relative to crop
    new_x = abs_x - crop_x1
    new_y = abs_y - crop_y1

    # Convert back to normalized coordinates relative to cropped image
    new_x_center = new_x / crop_w
    new_y_center = new_y / crop_h
    new_width = abs_w / crop_w
    new_height = abs_h / crop_h

    return [new_x_center, new_y_center, new_width, new_height]

def create_person_crops(padding_percent: int = 20):
    """Create person crops with adjusted annotations."""
    output_dir = Path('person_crops')
    output_dir.mkdir(exist_ok=True)

    print("[blue]Loading YOLOv8 model...[/blue]")
    model = YOLO('yolov8s.pt')

    images, label_dict = collect_files_recursively()

    if not images:
        print("[red]No valid image-label pairs found![/red]")
        return

    processed = 0
    crops_created = 0

    for img_path in tqdm(images, desc="Processing images"):
        label_path = label_dict[img_path.stem]
        img = Image.open(img_path)
        results = model(img, verbose=False)[0]

        # Get person detections
        person_boxes = []
        for r in results.boxes.data:
            if r[5] == 0:  # class 0 is person in COCO
                x1, y1, x2, y2 = map(int, r[:4])
                person_boxes.append((x1, y1, x2, y2))

        if not person_boxes:
            continue

        # Load original annotations
        orig_labels = load_yolo_labels(label_path)
        w, h = img.size

        # Process each person detection
        for i, box in enumerate(person_boxes):
            x1, y1, x2, y2 = box

            # Add padding
            pad_x = int((x2 - x1) * padding_percent / 100)
            pad_y = int((y2 - y1) * padding_percent / 100)

            crop_x1 = max(0, x1 - pad_x)
            crop_y1 = max(0, y1 - pad_y)
            crop_x2 = min(w, x2 + pad_x)
            crop_y2 = min(h, y2 + pad_y)

            # Crop image
            crop = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
            crop_w = crop_x2 - crop_x1
            crop_h = crop_y2 - crop_y1

            # Adjust and filter annotations
            new_labels = []
            for label in orig_labels:
                class_id = int(label[0])
                bbox = list(map(float, label[1:]))  # normalized coordinates

                # Convert to absolute coordinates for containment check
                abs_x = bbox[0] * w
                abs_y = bbox[1] * h
                abs_w = bbox[2] * w
                abs_h = bbox[3] * h

                # Calculate bbox corners
                bbox_x1 = abs_x - (abs_w / 2)
                bbox_y1 = abs_y - (abs_h / 2)
                bbox_x2 = abs_x + (abs_w / 2)
                bbox_y2 = abs_y + (abs_h / 2)

                # Check if bbox center is within crop area
                if (crop_x1 <= abs_x <= crop_x2 and
                    crop_y1 <= abs_y <= crop_y2):
                    # Adjust coordinates
                    new_bbox = adjust_bbox_coordinates(
                        bbox,
                        [crop_x1, crop_y1, crop_x2, crop_y2],
                        (w, h)
                    )
                    new_labels.append([class_id] + new_bbox)

            if new_labels:
                # Save crop and labels
                crop_name = f"{img_path.stem}_person{i}"
                crop.save(output_dir / f"{crop_name}.jpg")
                save_yolo_labels(new_labels, output_dir / f"{crop_name}.txt")
                crops_created += 1

        processed += 1

    print(f"[green]Person crop creation completed![/green]")
    print(f"[blue]Processed {processed} images[/blue]")
    print(f"[blue]Created {crops_created} person crops[/blue]")

def show_person_crops(sort_by_size: bool = False, reverse: bool = False):
    """
    Show details of all person crops.

    Args:
        sort_by_size: Whether to sort by image dimensions
        reverse: Whether to reverse the sorting order (small to large if True)
    """
    person_crops_dir = Path('person_crops')
    if not person_crops_dir.exists():
        print("[red]No person crops found! Run 'modelprep person-crop create' first.[/red]")
        return

    table = Table(title="Person Crops Overview")
    table.add_column("Crop Image")
    table.add_column("Dimensions")
    table.add_column("Objects")
    table.add_column("Size (KB)")

    # Collect image information
    image_info = []
    images = list(person_crops_dir.glob("*.jpg"))
    for img_path in images:
        label_path = img_path.with_suffix('.txt')
        with Image.open(img_path) as img:
            size_kb = img_path.stat().st_size / 1024
            n_objects = len(load_yolo_labels(label_path)) if label_path.exists() else 0
            width, height = img.size
            image_info.append({
                'path': img_path,
                'dimensions': f"{width}x{height}",
                'objects': n_objects,
                'size_kb': size_kb,
                'total_pixels': width * height  # for sorting
            })

    # Sort by size if requested
    if sort_by_size:
        image_info.sort(key=lambda x: x['total_pixels'], reverse=not reverse)  # not reverse because we want largest first by default
        sort_direction = "ascending" if reverse else "descending"
        print(f"[blue]Sorting by size in {sort_direction} order[/blue]")

    # Add rows to table
    for info in image_info:
        table.add_row(
            str(info['path']),
            info['dimensions'],
            str(info['objects']),
            f"{info['size_kb']:.1f}"
        )

    print(table)

def get_small_crops(min_size_kb: float = 10.0, min_pixels: int = 100) -> List[dict]:
    """
    Get list of crops that are smaller than specified thresholds.
    Returns list of dicts with image info.
    """
    person_crops_dir = Path('person_crops')
    if not person_crops_dir.exists():
        print("[red]No person crops found! Run 'modelprep person-crop create' first.[/red]")
        return []

    small_crops = []
    for img_path in person_crops_dir.glob("*.jpg"):
        with Image.open(img_path) as img:
            width, height = img.size
            size_kb = img_path.stat().st_size / 1024

            # Check if image is too small by either criterion
            if size_kb < min_size_kb or width < min_pixels or height < min_pixels:
                small_crops.append({
                    'path': img_path,
                    'dimensions': f"{width}x{height}",
                    'size_kb': size_kb,
                    'label_path': img_path.with_suffix('.txt')
                })

    return small_crops

def show_small_crops(min_size_kb: float = 10.0, min_pixels: int = 100):
    """Show crops that are smaller than specified thresholds."""
    small_crops = get_small_crops(min_size_kb, min_pixels)

    if not small_crops:
        print("[green]No small crops found![/green]")
        return

    table = Table(title=f"Small Crops (< {min_size_kb}KB or < {min_pixels}x{min_pixels})")
    table.add_column("Crop Image")
    table.add_column("Dimensions")
    table.add_column("Size (KB)")

    for crop in small_crops:
        table.add_row(
            str(crop['path']),
            crop['dimensions'],
            f"{crop['size_kb']:.1f}"
        )

    print(table)
    print(f"[yellow]Found {len(small_crops)} images that would be deleted[/yellow]")

def remove_small_crops(min_size_kb: float = 10.0, min_pixels: int = 100):
    """Remove crops that are smaller than specified thresholds."""
    small_crops = get_small_crops(min_size_kb, min_pixels)

    if not small_crops:
        print("[green]No small crops found![/green]")
        return

    print(f"[yellow]About to delete {len(small_crops)} images and their label files:[/yellow]")

    # Show what will be deleted
    table = Table(title=f"Files to be deleted (< {min_size_kb}KB or < {min_pixels}x{min_pixels})")
    table.add_column("Crop Image")
    table.add_column("Dimensions")
    table.add_column("Size (KB)")

    for crop in small_crops:
        table.add_row(
            str(crop['path']),
            crop['dimensions'],
            f"{crop['size_kb']:.1f}"
        )

    print(table)

    # Ask for confirmation
    confirm = input("Are you sure you want to delete these files? (yes/no): ")

    if confirm.lower() == 'yes':
        for crop in tqdm(small_crops, desc="Deleting files"):
            # Delete image and label file if it exists
            crop['path'].unlink()
            if crop['label_path'].exists():
                crop['label_path'].unlink()
        print(f"[green]Successfully deleted {len(small_crops)} images and their label files[/green]")
    else:
        print("[yellow]Deletion cancelled[/yellow]")

def get_or_prompt_api_key() -> str:
    """Get API key from .env or prompt user."""
    load_dotenv()
    api_key = os.getenv('ROBOFLOW_API_KEY')

    if not api_key:
        api_key = input("Please enter your Roboflow API Key: ")
        # Store in .env file
        env_path = Path('.env')
        set_key(str(env_path), 'ROBOFLOW_API_KEY', api_key)
        print("[green]API key stored in .env file[/green]")

    return api_key

def create_roboflow_project(
    api_key: str,
    project_name: str,
    project_type: str = "object-detection",
    project_license: str = "CC BY 4.0",
    annotation: str = "object-detection"  # or "classification" depending on project type
) -> Optional[str]:
    """
    Create a new project on Roboflow.
    Returns project ID if successful.
    """
    try:
        print("[blue]Connecting to Roboflow...[/blue]")
        rf = Roboflow(api_key=api_key)

        # Get workspace first, then create project
        print(f"[blue]Creating project '{project_name}'...[/blue]")
        workspace = rf.workspace()
        project = workspace.create_project(
            project_name=project_name,
            project_type=project_type,
            project_license=project_license,
            annotation=annotation
        )

        print(f"[green]Successfully created project '{project_name}'![/green]")
        print(f"[blue]Project ID: {project.id}[/blue]")
        return project.id

    except Exception as e:
        print(f"[red]Error creating project: {str(e)}[/red]")
        return None

def validate_yolo_annotation(content: str) -> bool:
    """
    Validate YOLO annotation format.
    Each line should be: class_id x_center y_center width height
    All values should be between 0 and 1.
    """
    try:
        lines = content.strip().split('\n')
        for line in lines:
            values = line.strip().split()
            if len(values) != 5:
                return False

            # Check if class_id is integer
            class_id = int(values[0])

            # Check if coordinates are floats between 0 and 1
            x, y, w, h = map(float, values[1:])
            if not all(0 <= val <= 1 for val in [x, y, w, h]):
                return False
        return True
    except:
        return False

def normalize_yolo_annotation(annotation: str, img_width: int, img_height: int) -> str:
    """
    Normalize YOLO annotation coordinates to be between 0 and 1.
    """
    normalized_lines = []
    for line in annotation.strip().split('\n'):
        values = line.strip().split()
        if len(values) == 5:
            class_id = values[0]
            x_center = float(values[1]) / img_width
            y_center = float(values[2]) / img_height
            width = float(values[3])  # width and height are already normalized
            height = float(values[4])
            normalized_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    return '\n'.join(normalized_lines)

def upload_to_roboflow(
    api_key: str,
    project_name: str,
    dataset_name: str = "person-crops"
):
    """Upload person crops to Roboflow project."""
    person_crops_dir = Path('person_crops')
    if not person_crops_dir.exists():
        print("[red]No person crops found! Run 'modelprep person-crop create' first.[/red]")
        return

    try:
        print("[blue]Connecting to Roboflow...[/blue]")
        rf = Roboflow(api_key=api_key)
        workspace = rf.workspace()
        project = workspace.project(project_name)

        print("[blue]Preparing files for upload...[/blue]")
        images = list(person_crops_dir.glob("*.jpg"))

        if not images:
            print("[red]No images found in person_crops directory![/red]")
            return

        print(f"[blue]Uploading {len(images)} images and annotations...[/blue]")
        for img_path in tqdm(images, desc="Uploading"):
            label_path = img_path.with_suffix('.txt')

            if not label_path.exists():
                print(f"[yellow]Warning: No label file found for {img_path.name}[/yellow]")
                continue

            try:
                # Get image dimensions
                with Image.open(img_path) as img:
                    img_width, img_height = img.size

                # Read and normalize annotation
                with open(label_path, 'r') as f:
                    annotation_content = f.read()

                if not annotation_content.strip():
                    print(f"[yellow]Warning: Empty annotation file for {img_path.name}[/yellow]")
                    continue

                # Normalize coordinates
                normalized_annotation = normalize_yolo_annotation(annotation_content, img_width, img_height)

                # Save normalized annotation to a temporary file
                temp_label_path = label_path.with_suffix('.temp.txt')
                with open(temp_label_path, 'w') as f:
                    f.write(normalized_annotation)

                try:
                    # Upload with normalized annotations
                    project.upload(
                        image_path=str(img_path),
                        annotation_path=str(temp_label_path),
                        split="train"
                    )
                except Exception as upload_error:
                    print(f"[red]Upload error for {img_path.name}:[/red]")
                    print(f"Error message: {str(upload_error)}")
                finally:
                    # Clean up temporary file
                    if temp_label_path.exists():
                        temp_label_path.unlink()

            except Exception as e:
                print(f"[red]Error processing {img_path.name}: {str(e)}[/red]")
                continue

        print("[green]Upload completed![/green]")
        print(f"[blue]Dataset name: {dataset_name}[/blue]")
        print("[blue]You can now access your dataset on Roboflow's website.[/blue]")

    except Exception as e:
        print(f"[red]Error uploading to Roboflow: {str(e)}[/red]")

def add_person_crops_to_dataset(train_split: float = 0.7, valid_split: float = 0.2, test_split: float = 0.1):
    """Add person crops to dataset with train/valid/test split."""
    person_crops_dir = Path('person_crops')
    dataset_dir = Path('dataset')

    if not person_crops_dir.exists():
        print("[red]No person crops found! Run 'modelprep person-crop create' first.[/red]")
        return

    if not dataset_dir.exists():
        print("[red]Dataset directory not found![/red]")
        return

    # Create split directories if they don't exist
    splits = ['train', 'valid', 'test']
    for split in splits:
        (dataset_dir / split / 'images').mkdir(parents=True, exist_ok=True)
        (dataset_dir / split / 'labels').mkdir(parents=True, exist_ok=True)

    # Get all person crop images and their labels
    images = list(person_crops_dir.glob('*.jpg'))
    if not images:
        print("[red]No person crop images found![/red]")
        return

    # Shuffle images
    np.random.shuffle(images)

    # Calculate split indices
    n_images = len(images)
    n_train = int(n_images * train_split)
    n_valid = int(n_images * valid_split)

    # Split images
    train_images = images[:n_train]
    valid_images = images[n_train:n_train + n_valid]
    test_images = images[n_train + n_valid:]

    # Function to copy files with person_crop_ prefix
    def copy_files(image_list, split_name):
        for img_path in tqdm(image_list, desc=f"Copying {split_name} files"):
            # Add person_crop_ prefix if not already present
            new_name = f"person_crop_{img_path.name}" if not img_path.name.startswith('person_crop_') else img_path.name

            # Copy image
            shutil.copy2(
                img_path,
                dataset_dir / split_name / 'images' / new_name
            )

            # Copy label if exists
            label_path = img_path.with_suffix('.txt')
            if label_path.exists():
                shutil.copy2(
                    label_path,
                    dataset_dir / split_name / 'labels' / new_name.replace('.jpg', '.txt')
                )

    # Copy files to respective splits
    print("[blue]Adding person crops to dataset...[/blue]")
    copy_files(train_images, 'train')
    copy_files(valid_images, 'valid')
    copy_files(test_images, 'test')

    print(f"[green]Successfully added {len(images)} person crops to dataset![/green]")
    print(f"[blue]Train: {len(train_images)} images[/blue]")
    print(f"[blue]Valid: {len(valid_images)} images[/blue]")
    print(f"[blue]Test: {len(test_images)} images[/blue]")

def remove_person_crops_from_dataset():
    """Remove all person crops from the dataset."""
    dataset_dir = Path('dataset')
    if not dataset_dir.exists():
        print("[red]Dataset directory not found![/red]")
        return

    removed_count = 0

    # Remove from each split
    for split in ['train', 'valid', 'test']:
        images_dir = dataset_dir / split / 'images'
        labels_dir = dataset_dir / split / 'labels'

        if not images_dir.exists() or not labels_dir.exists():
            continue

        # Remove images and labels that start with person_crop_
        for img_path in tqdm(list(images_dir.glob('person_crop_*.jpg')),
                           desc=f"Removing from {split}"):
            img_path.unlink()
            label_path = labels_dir / img_path.name.replace('.jpg', '.txt')
            if label_path.exists():
                label_path.unlink()
            removed_count += 1

    print(f"[green]Successfully removed {removed_count} person crops from dataset![/green]")

def create_dataset_yaml():
    """Create dataset.yaml file for training."""
    dataset_config = {
        'path': str(Path.cwd()),  # dataset root dir
        'train': 'dataset/train/images',  # train images
        'val': 'dataset/valid/images',    # val images
        'test': 'dataset/test/images',    # test images (optional)

        # Classes
        'names': {
            0: 'person',
            1: 'mobile_phone',
            # add other classes as needed
        }
    }

    # Save yaml file
    with open('dataset.yaml', 'w') as f:
        yaml.dump(dataset_config, f, sort_keys=False)

    return 'dataset.yaml'

def get_training_config(
    model_size: str,
    epochs: int,
    batch_size: int,
    image_size: int,
    device: str,
    project_name: str,
    name: str,
    resume: bool,
) -> dict:
    """Get optimized training configuration for small object detection on A100."""
    return {
        # Basic training params
        'data': 'dataset.yaml',
        'epochs': epochs,
        'batch': batch_size,      # A100 can handle large batches
        'imgsz': image_size,      # 640 as requested
        'device': device if device else None,
        'project': project_name,
        'name': name,
        'resume': resume,

        # Optimizer settings - optimized for A100
        'optimizer': 'AdamW',     # Better than SGD for small objects
        'lr0': 0.002,            # Higher initial LR for large batch
        'lrf': 0.002,            # Higher final LR
        'momentum': 0.937,
        'weight_decay': 0.0005,
        'warmup_epochs': 3.0,     # Shorter warmup for large batch
        'warmup_momentum': 0.8,
        'warmup_bias_lr': 0.1,

        # Loss coefficients - optimized for small objects
        'box': 15.0,             # Increased box loss for better small object localization
        'cls': 0.2,              # Reduced classification weight
        'dfl': 3.0,              # Increased DFL for better localization

        # Augmentation strategy for small objects
        'mosaic': 1.0,           # Maximum mosaic for more small object instances
        'mixup': 0.3,            # Moderate mixup
        'copy_paste': 0.4,       # Enabled copy-paste for more small objects

        # Color/brightness augmentation - helps with phone detection
        'hsv_h': 0.015,          # Slight hue variation
        'hsv_s': 0.6,            # Moderate saturation
        'hsv_v': 0.5,            # Moderate brightness

        # Geometric augmentation - careful with small objects
        'degrees': 10.0,         # Moderate rotation
        'translate': 0.2,        # Moderate translation
        'scale': 0.7,            # Aggressive scaling for size variation
        'shear': 0.0,            # No shear (preserves small objects)
        'perspective': 0.0,      # No perspective (preserves small objects)
        'flipud': 0.0,           # No vertical flip
        'fliplr': 0.5,           # Horizontal flip

        # Data loading - optimized for A100
        'workers': 16,           # Maximum workers for A100
        'rect': False,           # Disabled for better augmentation
        'close_mosaic': 10,      # Disable mosaic in final epochs

        # Advanced training settings
        'save': True,
        'save_period': 50,
        'plots': True,
        'label_smoothing': 0.0,  # Disabled for small objects
        'patience': 100,         # More patience for convergence
        'cos_lr': True,          # Cosine LR scheduler
        'overlap_mask': True,    # Better mask overlap
        'mask_ratio': 4,         # Mask downsample ratio
        'single_cls': False,     # Multi-class training
        'nbs': 64,              # Nominal batch size

        # Validation settings
        'val': True,            # Run validation
        'iou': 0.5,             # IoU threshold
        'conf': 0.001,          # Lower confidence threshold for small objects
        'max_det': 300,         # Maximum detections per image
    }

def train_yolo_model(
    model_size: str = "small",
    epochs: int = 300,
    batch_size: int = 256,
    image_size: int = 640,
    device: str = "",
    project_name: str = "runs/train",
    name: str = None,
    resume: bool = False,
    validation_only: bool = False,
    nohup: bool = False,
    weights: str = ""
):
    """Train YOLOv8 model optimized for small object detection."""
    # Model size mapping
    model_map = {
        "nano": "yolov8n.pt",
        "small": "yolov8s.pt",
        "medium": "yolov8m.pt",
        "large": "yolov8l.pt",
        "xlarge": "yolov8x.pt"
    }

    # Get unified training configuration
    config = get_training_config(
        model_size=model_size,
        epochs=epochs,
        batch_size=batch_size,
        image_size=image_size,
        device=device,
        project_name=project_name,
        name=name,
        resume=resume
    )

    # Initialize model
    if weights:
        model = YOLO(weights)
    else:
        model = YOLO(model_map[model_size])

    # If validation only
    if validation_only:
        print("[blue]Running validation only...[/blue]")
        try:
            results = model.val(**config)
            # ... validation code ...
            return
        except Exception as e:
            print(f"[red]Error during validation: {str(e)}[/red]")
            return

    # If nohup, create a script and run with nohup
    if nohup:
        # Create nohup-specific filenames
        script_name = f"nohup_train_{name}.py"
        log_name = f"nohup_train_{name}.log"

        script_path = Path(script_name)
        log_file = Path(log_name)

        script_content = f"""
import sys
from ultralytics import YOLO

model = YOLO({'weights' if weights else f"'{model_map[model_size]}'"})

# Using same configuration as direct training
config = {config}
model.train(**config)
"""
        # Save script
        with open(script_path, 'w') as f:
            f.write(script_content)

        print(f"[blue]Starting training with nohup. Check {log_file} for progress.[/blue]")
        subprocess.Popen(['nohup', sys.executable, str(script_path), '>', str(log_file), '2>&1', '&'])
        return

    # Normal training
    print(f"[blue]Starting training with YOLOv8 {model_size} model...[/blue]")
    print(f"[blue]Image size: {image_size}[/blue]")
    print(f"[blue]Batch size: {batch_size}[/blue]")
    print(f"[blue]Epochs: {epochs}[/blue]")

    try:
        results = model.train(**config)
        # ... rest of training code ...
    except Exception as e:
        print(f"[red]Error during training: {str(e)}[/red]")

def get_training_status(name: str = None, follow: bool = False, lines: int = 50):
    """Get status of training from log files."""
    # Find the relevant log file
    if name:
        log_file = Path(f"nohup_train_{name}.log")
    else:
        # Find most recent log file
        log_files = list(Path().glob("nohup_train_*.log"))
        if not log_files:
            print("[red]No training log files found![/red]")
            return
        log_file = max(log_files, key=lambda x: x.stat().st_mtime)

    if not log_file.exists():
        print(f"[red]Log file {log_file} not found![/red]")
        return

    def display_logs():
        table = Table(title=f"Training Status - {log_file.name}")
        table.add_column("Time")
        table.add_column("Log")

        with open(log_file) as f:
            latest_lines = f.readlines()[-lines:]
            for line in latest_lines:
                if line.strip():  # Skip empty lines
                    table.add_row(
                        datetime.now().strftime("%H:%M:%S"),
                        line.strip()
                    )
        return table

    if follow:
        print(f"[blue]Following {log_file}. Press Ctrl+C to stop.[/blue]")
        try:
            with Live(display_logs(), refresh_per_second=1) as live:
                while True:
                    live.update(display_logs())
                    time.sleep(1)
        except KeyboardInterrupt:
            print("\n[blue]Stopped following log file.[/blue]")
    else:
        # Just show current status
        print(display_logs())

def check_existing_training(name: str) -> bool:
    """Check if training with given name is already running."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.cmdline()
            if f"nohup_train_{name}.py" in ' '.join(cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False