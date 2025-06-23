import os
import subprocess
from pathlib import Path
from shutil import copyfile

def run(command):
    print(f"🔧 Running: {' '.join(command)}")
    subprocess.run(command, check=True)

def main():
    print("📦 Installing dependencies with Poetry...")
    run(["poetry", "install"])

    env_path = Path(".env")
    if not env_path.exists():
        if Path(".env.example").exists():
            print("📁 Creating .env from .env.example...")
            copyfile(".env.example", ".env")
        else:
            print("⚠️  No .env or .env.example found. Skipping .env creation.")

    print("🔐 Initializing APP_KEY...")
    run(["poetry", "run", "key_generate"])

    print("✅ All set up! You can now run the app.")

if __name__ == "__main__":
    main()
