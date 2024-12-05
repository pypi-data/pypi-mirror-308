import os
import subprocess
import argparse
import shutil
import sys
from pathlib import Path
import platform

def run_command(command, cwd=None):
    """
    Executes a shell command.
    """
    try:
        subprocess.run(command, check=True, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

def check_dependencies():
    """
    Checks if FFmpeg and Python are installed and accessible.
    """
    # Check FFmpeg
    try:
        subprocess.run('ffmpeg -version', check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print("Error: FFmpeg is not installed or not found in PATH. Please install FFmpeg from https://ffmpeg.org/download.html.")
        sys.exit(1)
    
    # Check Python
    if not shutil.which("python"):
        print("Error: Python is not installed or not found in PATH.")
        sys.exit(1)

def get_videos_directory():
    """
    Returns the path to the default Videos directory based on the operating system.
    """
    home = Path.home()
    system = platform.system()
    
    if system == "Windows":
        # Use the built-in Videos folder in Windows
        return home / "Videos"
    elif system == "Darwin":
        # Use the Movies folder in macOS
        return home / "Movies"
    else:
        # For Linux and other OSes, default to Videos in home
        return home / "Videos"

def main():
    parser = argparse.ArgumentParser(description="RIFEX CLI Tool for Video Frame Interpolation")
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to the input video file')
    parser.add_argument('-o', '--output', type=str, help='Path to save the output video. Defaults to <Videos Directory>/<input_filename>_rifex.<extension>')
    parser.add_argument('-f', '--factor', type=int, choices=[2, 3, 4], default=2, help='Interpolation factor (2x, 3x, 4x)')
    parser.add_argument('-s', '--scale', type=float, choices=[0.25, 0.5, 1.0, 2.0, 4.0], default=0.5, help='Scale factor for RIFE. Choose from [0.25, 0.5, 1.0, 2.0, 4.0]. Lower values may increase speed')
    
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    factor = args.factor
    scale = args.scale

    # Check for external dependencies
    check_dependencies()

    if not os.path.isfile(input_path):
        print(f"Error: Input file does not exist: {input_path}")
        sys.exit(1)

    # Set default output path if not specified
    if not output_path:
        input_filename = Path(input_path).stem
        input_extension = Path(input_path).suffix
        videos_dir = get_videos_directory()
        videos_dir.mkdir(parents=True, exist_ok=True)  # Create Videos directory if it doesn't exist
        output_path = videos_dir / f"{input_filename}_rifex{input_extension}"

    # Locate the ECCV2022-RIFE directory within the package
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rife_dir = os.path.join(script_dir, "ECCV2022-RIFE")
    rife_script = os.path.join(rife_dir, "inference_video.py")
    rife_model_dir = os.path.join(rife_dir, "train_log")

    if not os.path.exists(rife_dir):
        print("Error: RIFE directory is missing from the installation.")
        sys.exit(1)

    if not os.path.isfile(rife_script):
        print("Error: RIFE inference script is missing.")
        sys.exit(1)

    if not os.path.isdir(rife_model_dir):
        print("Error: RIFE model directory is missing.")
        sys.exit(1)

    # Run RIFE interpolation
    print(f"Running RIFE interpolation with factor {factor}x and scale {scale}...")

    rife_command = (
        f'python "{rife_script}" '
        f'--exp={factor - 1} '
        f'--video="{input_path}" '
        f'--output="{output_path}" '
        f'--model="{rife_model_dir}" '
        f'--scale={scale}'
    )
    run_command(rife_command)

    print("\nProcess complete!")
    print(f"Output Video: {output_path}")

if __name__ == "__main__":
    main()
