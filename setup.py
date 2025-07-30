#!/usr/bin/env python3
"""
SpotiPi Setup Script

This script helps set up SpotiPi on your Raspberry Pi.
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_raspberry_pi():
    """Check if running on Raspberry Pi."""
    if os.path.exists('/proc/cpuinfo'):
        with open('/proc/cpuinfo', 'r') as f:
            content = f.read()
            if 'Raspberry Pi' in content:
                return True
    return False

def install_dependencies():
    """Install system dependencies."""
    print("📦 Installing system dependencies...")
    
    # Update package list
    if not run_command("sudo apt update", "Updating package list"):
        return False
    
    # Install required packages
    packages = [
        "python3-pip",
        "python3-dev",
        "python3-pil",
        "python3-pil.imagetk",
        "libjpeg-dev",
        "zlib1g-dev",
        "libfreetype6-dev",
        "liblcms2-dev",
        "libopenjp2-7-dev",
        "libtiff5-dev",
        "libwebp-dev",
        "libharfbuzz-dev",
        "libfribidi-dev",
        "libxcb1-dev",
        "pkg-config"
    ]
    
    for package in packages:
        if not run_command(f"sudo apt install -y {package}", f"Installing {package}"):
            return False
    
    return True

def install_python_packages():
    """Install Python packages."""
    print("🐍 Installing Python packages...")
    
    # Upgrade pip
    if not run_command("python3 -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command("pip3 install -r requirements.txt", "Installing Python requirements"):
        return False
    
    return True

def setup_rgb_matrix():
    """Setup RGB matrix library."""
    print("📺 Setting up RGB matrix library...")
    
    # Clone rpi-rgb-led-matrix repository
    if not os.path.exists("rpi-rgb-led-matrix"):
        if not run_command("git clone https://github.com/hzeller/rpi-rgb-led-matrix.git", "Cloning RGB matrix library"):
            return False
    
    # Build and install
    os.chdir("rpi-rgb-led-matrix")
    
    if not run_command("make build-python PYTHON=$(which python3)", "Building RGB matrix library"):
        return False
    
    if not run_command("sudo make install-python PYTHON=$(which python3)", "Installing RGB matrix library"):
        return False
    
    os.chdir("..")
    return True

def setup_service():
    """Setup systemd service."""
    print("🔧 Setting up systemd service...")
    
    # Copy service file
    if not run_command("sudo cp spotipi.service /etc/systemd/system/", "Copying service file"):
        return False
    
    # Reload systemd
    if not run_command("sudo systemctl daemon-reload", "Reloading systemd"):
        return False
    
    # Enable service
    if not run_command("sudo systemctl enable spotipi.service", "Enabling SpotiPi service"):
        return False
    
    return True

def create_cache_directory():
    """Create cache directory."""
    print("📁 Creating cache directory...")
    
    try:
        os.makedirs("cache", exist_ok=True)
        print("✅ Cache directory created")
        return True
    except Exception as e:
        print(f"❌ Failed to create cache directory: {e}")
        return False

def main():
    """Main setup function."""
    print("🎵 SpotiPi Setup")
    print("=" * 30)
    
    # Check if running on Raspberry Pi
    if not check_raspberry_pi():
        print("⚠️  Warning: This doesn't appear to be a Raspberry Pi.")
        print("   Some features may not work correctly.")
        print()
    
    # Check if running as root
    if os.geteuid() == 0:
        print("❌ Please don't run this script as root!")
        print("   Run it as a regular user (pi).")
        return
    
    # Install system dependencies
    if not install_dependencies():
        print("❌ Failed to install system dependencies")
        return
    
    # Install Python packages
    if not install_python_packages():
        print("❌ Failed to install Python packages")
        return
    
    # Setup RGB matrix (only on Raspberry Pi)
    if check_raspberry_pi():
        if not setup_rgb_matrix():
            print("❌ Failed to setup RGB matrix")
            return
    
    # Create cache directory
    if not create_cache_directory():
        print("❌ Failed to create cache directory")
        return
    
    # Setup service
    if not setup_service():
        print("❌ Failed to setup systemd service")
        return
    
    print()
    print("🎉 SpotiPi setup completed successfully!")
    print()
    print("Next steps:")
    print("1. Edit config.py with your Spotify credentials")
    print("2. Run: python3 auth_spotify.py")
    print("3. Start the service: sudo systemctl start spotipi")
    print("4. Check status: sudo systemctl status spotipi")
    print()
    print("For manual testing, run: python3 main.py")

if __name__ == "__main__":
    main() 