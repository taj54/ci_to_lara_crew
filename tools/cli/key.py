import os
import base64
from dotenv import load_dotenv, set_key
import typer

app = typer.Typer()

# Constants
ENV_PATH = ".env"
ENV_KEY = "APP_KEY"


def load_env():
    """Load environment variables from the .env file."""
    load_dotenv(ENV_PATH, override=True)


def generate_base64_key(length: int = 32) -> str:
    """Generate a base64-encoded secure key with a prefix."""
    raw_key = base64.urlsafe_b64encode(os.urandom(length)).decode()
    return f"base64:{raw_key}"


@app.command()
def generate():
    """
    Generate and store a new APP_KEY in the .env file.
    """
    load_env()
    new_key = generate_base64_key()
    set_key(ENV_PATH, ENV_KEY, new_key)
    typer.secho(f"✅ APP_KEY set in {ENV_PATH}:\n{new_key}", fg=typer.colors.GREEN)


@app.command()
def show():
    """
    Show the current APP_KEY from the .env file.
    """
    load_env()
    current_key = os.getenv(ENV_KEY)
    if current_key:
        typer.secho(f"🔑 Current APP_KEY:\n{current_key}", fg=typer.colors.CYAN)
    else:
        typer.secho("❌ APP_KEY not found in .env", fg=typer.colors.RED)

@app.command()
def verify():
    """
    Verify if the current APP_KEY is valid.
    """
    load_env()
    key = os.getenv(ENV_KEY)
    if not key:
        typer.secho("❌ APP_KEY not found in .env", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    if key.startswith("base64:"):
        key = key[len("base64:"):]

    try:
        decoded = base64.urlsafe_b64decode(key)
        if len(decoded) < 16:
            raise ValueError("Key too short")
        typer.secho("✅ APP_KEY is a valid base64-encoded key.", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"❌ Invalid APP_KEY format: {e}", fg=typer.colors.RED)




if __name__ == "__main__":
    app()
