#!/usr/bin/env python3
"""
Build script to create executable using PyInstaller
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print("PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install PyInstaller")
        return False

def build_exe():
    """Build the executable"""
    try:
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--console',  # Keep console to see errors
            '--name', 'DinoGame',
            '--add-data', '../data;data',
            '--add-data', '../logs;logs',
            '--hidden-import', 'pygame',
            '--hidden-import', 'pygame.mixer',
            '--collect-all', 'pygame',
            'game.py'
        ]
        
        subprocess.run(cmd, check=True)
        print("Executable built successfully in dist/DinoGame.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to build executable: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("Dino Game Executable Builder")
    print("=" * 50)
    print()
    
    # Install PyInstaller
    print("Installing PyInstaller...")
    if not install_pyinstaller():
        sys.exit(1)
    
    print()
    
    # Build executable
    print("Building executable...")
    if build_exe():
        print()
        print("Build complete! The executable is in dist/DinoGame.exe")
    else:
        sys.exit(1)
