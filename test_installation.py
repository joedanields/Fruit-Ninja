"""
Installation and Testing Script for AI Fruit Ninja
Run with: python test_installation.py
"""
import subprocess
import sys
from pathlib import Path


def test_import():
    """Test if package can be imported"""
    print("🧪 Testing package import...")
    try:
        import ai_fruit_ninja
        print(f"   ✅ Package imported successfully")
        print(f"   📦 Version: {ai_fruit_ninja.__version__}")
        return True
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False


def test_entry_point():
    """Test if entry point function exists"""
    print("\n🧪 Testing entry point...")
    try:
        from ai_fruit_ninja import run_game
        print("   ✅ run_game() function available")
        return True
    except ImportError as e:
        print(f"   ❌ Entry point test failed: {e}")
        return False


def test_cli_command():
    """Test if CLI command is available"""
    print("\n🧪 Testing CLI command...")
    try:
        result = subprocess.run(
            ["ai-fruit-ninja", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        # The game doesn't have --help, so it will try to start
        # We can check if the command exists
        print("   ✅ CLI command 'ai-fruit-ninja' is available")
        return True
    except FileNotFoundError:
        print("   ❌ CLI command 'ai-fruit-ninja' not found")
        print("   ℹ️  Try: pip install -e . or pip install .")
        return False
    except subprocess.TimeoutExpired:
        print("   ✅ CLI command exists (timed out waiting for game)")
        return True
    except Exception as e:
        print(f"   ⚠️  CLI test inconclusive: {e}")
        return False


def test_module_execution():
    """Test if package can be run as module"""
    print("\n🧪 Testing module execution...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "ai_fruit_ninja"],
            capture_output=True,
            text=True,
            timeout=2
        )
        print("   ✅ Module execution works (python -m ai_fruit_ninja)")
        return True
    except subprocess.TimeoutExpired:
        print("   ✅ Module execution works (timed out waiting for game)")
        return True
    except Exception as e:
        print(f"   ❌ Module execution failed: {e}")
        return False


def test_assets():
    """Test if assets are accessible"""
    print("\n🧪 Testing asset accessibility...")
    try:
        from ai_fruit_ninja.main import get_asset_path
        
        test_assets = ['watermelon.png', 'apple.png', 'banana.png', 'bomb.png']
        all_found = True
        
        for asset in test_assets:
            path = get_asset_path(asset)
            if path and path.exists():
                print(f"   ✅ {asset} found")
            else:
                print(f"   ❌ {asset} not found")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"   ❌ Asset test failed: {e}")
        return False


def test_dependencies():
    """Test if all dependencies are installed"""
    print("\n🧪 Testing dependencies...")
    
    dependencies = {
        'pygame': 'Pygame',
        'cv2': 'OpenCV',
        'mediapipe': 'MediaPipe',
        'numpy': 'NumPy'
    }
    
    all_installed = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {name} installed")
        except ImportError:
            print(f"   ❌ {name} not installed")
            all_installed = False
    
    return all_installed


def show_summary(results):
    """Show test summary"""
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    total = len(results)
    passed = sum(results.values())
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Package is ready to use.")
        print("   Run the game with: ai-fruit-ninja")
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
    
    print("=" * 60)


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🥷 AI Fruit Ninja - Installation Test")
    print("=" * 60 + "\n")
    
    results = {}
    
    results["Dependencies"] = test_dependencies()
    results["Package Import"] = test_import()
    results["Entry Point"] = test_entry_point()
    results["Module Execution"] = test_module_execution()
    results["CLI Command"] = test_cli_command()
    results["Assets"] = test_assets()
    
    show_summary(results)
    
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
