# Python script for removing backgrounds from images

import os
import shutil
from datetime import datetime
from pathlib import Path

from rembg import remove
from PIL import Image


def init_file_structure() -> tuple[Path, Path, Path]:
    """
    Initialize the folder structure:
      - Inputs
      - Outputs
      - Backups
    """
    base_dir = Path(__file__).resolve().parent

    inputs_dir = base_dir / "Inputs"
    outputs_dir = base_dir / "Outputs"
    backups_dir = base_dir / "Backups"

    inputs_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)
    backups_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Inputs folder:  {inputs_dir}")
    print(f"[INFO] Outputs folder: {outputs_dir}")
    print(f"[INFO] Backups folder: {backups_dir}")

    return inputs_dir, outputs_dir, backups_dir


def backup_input_files(input_path: Path, backups_root: Path) -> Path | None:
    """
    Create a timestamped backup of the entire Inputs folder.
    Returns the backup folder path if created successfully.
    """

    if not input_path.is_dir():
        print("[WARN] Inputs folder missing. No backup created.")
        return None

    if not any(input_path.iterdir()):
        print("[INFO] Inputs folder is empty. No backup created.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = backups_root / f"backup_{timestamp}"

    try:
        shutil.copytree(input_path, backup_dir)
        print(f"[OK] Backup created: {backup_dir}")
        return backup_dir
    except Exception as e:
        print(f"[ERROR] Backup failed: {e}")
        return None


def clear_inputs_folder(input_path: Path) -> None:
    """
    Deletes all files inside the Inputs folder
    but preserves the Inputs directory itself.
    """

    print("[INFO] Clearing Inputs folder...")

    for item in input_path.iterdir():
        try:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            print(f"[ERROR] Failed to remove {item}: {e}")

    print("[OK] Inputs folder cleared.")


def process_images(input_path: Path, output_path: Path) -> None:
    """
    Remove background from each image in Inputs
    and save as rmbg_<original_name>.png in Outputs.
    """

    valid_exts = {".png", ".jpg", ".jpeg", ".webp"}
    count = 0

    for file in input_path.iterdir():
        if not file.is_file() or file.suffix.lower() not in valid_exts:
            continue

        output_file = output_path / f"rmbg_{file.stem}.png"
        print(f"[INFO] Processing: {file.name}")

        try:
            with Image.open(file) as inp:
                result = remove(inp)
                result.save(output_file)

            count += 1
            print(f"[OK] Saved: {output_file.name}")

        except Exception as e:
            print(f"[ERROR] Failed on {file.name}: {e}")

    print(f"[DONE] Processed {count} image(s).")


def main():
    inputs_dir, outputs_dir, backups_dir = init_file_structure()

    # 1) Backup originals
    backup_dir = backup_input_files(inputs_dir, backups_dir)

    # 2) Only continue if backup succeeded or Inputs was empty
    if backup_dir is not None or not any(inputs_dir.iterdir()):
        process_images(inputs_dir, outputs_dir)

        # 3) Clear Inputs ONLY after successful backup
        if backup_dir is not None:
            clear_inputs_folder(inputs_dir)
    else:
        print("[ABORT] Inputs NOT cleared because backup failed.")


if __name__ == "__main__":
    main()
