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
    example_path = Path(".env.example")

    if not env_path.exists() and example_path.exists():
        print("📁 Copying .env.example to .env...")
        copyfile(example_path, env_path)
    elif not example_path.exists():
        print("⚠️  No .env.example found. Skipping .env creation.")
    else:
        print("✅ .env already exists.")

    print("🔐 Initializing APP_KEY...")
    run(["poetry", "run", "key_generate"])

    print("✅ All set up! You can now run the app.")

if __name__ == "__main__":
    main()
