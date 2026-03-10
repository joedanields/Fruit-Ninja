"""
Build script for AI Fruit Ninja package
Run with: python build_package.py
"""
import subprocess
import shutil
import sys
from pathlib import Path


def clean_build_artifacts():
    """Remove previous build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_remove = ['build', 'dist', 'ai_fruit_ninja.egg-info']
    for dir_name in dirs_to_remove:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"   Removed {dir_name}/")
    
    print("✅ Clean complete\n")


def build_package():
    """Build the package using python -m build"""
    print("📦 Building package...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "build"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print("✅ Build complete\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed:")
        print(e.stderr)
        return False


def list_distributions():
    """List created distribution files"""
    dist_path = Path('dist')
    if dist_path.exists():
        print("📋 Created distributions:")
        for file in dist_path.iterdir():
            size = file.stat().st_size / 1024  # KB
            print(f"   {file.name} ({size:.1f} KB)")
        print()


def show_install_instructions():
    """Show installation instructions"""
    print("=" * 60)
    print("🎉 Package built successfully!")
    print("=" * 60)
    print("\n📝 Installation options:")
    print("\n1. Install locally:")
    print("   pip install dist/ai_fruit_ninja-1.0.0-py3-none-any.whl")
    print("\n2. Install in editable mode (development):")
    print("   pip install -e .")
    print("\n3. Test PyPI upload:")
    print("   python -m twine upload --repository testpypi dist/*")
    print("\n4. PyPI upload:")
    print("   python -m twine upload dist/*")
    print("\n5. Run the game:")
    print("   ai-fruit-ninja")
    print("=" * 60)


def main():
    """Main build process"""
    print("\n" + "=" * 60)
    print("🥷 AI Fruit Ninja - Package Builder")
    print("=" * 60 + "\n")
    
    # Check if build module is installed
    try:
        import build
    except ImportError:
        print("❌ 'build' module not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "build"], check=True)
        print("✅ 'build' installed\n")
    
    # Clean previous builds
    clean_build_artifacts()
    
    # Build package
    if build_package():
        list_distributions()
        show_install_instructions()
        return 0
    else:
        print("\n❌ Build process failed. Please check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
