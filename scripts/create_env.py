"""
Create a local .env file from .env.example and generate a secure SECRET_KEY.
- Safe to run before dependencies are installed.
- Prompts before overwriting an existing .env.
"""
from __future__ import annotations

import secrets
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_PATH = REPO_ROOT / ".env.example"
ENV_PATH = REPO_ROOT / ".env"
SECRET_PLACEHOLDER = "SECRET_KEY=changeme-with-create_env-script"


def generate_secret_key() -> str:
    """Generate a URL-safe secret key suitable for Django."""
    return secrets.token_urlsafe(64)


def build_env_content(example_text: str, secret_key: str) -> str:
    """Replace the SECRET_KEY placeholder with a generated key."""
    lines = []
    for line in example_text.splitlines():
        if line.startswith("SECRET_KEY="):
            lines.append(f"SECRET_KEY={secret_key}")
        else:
            lines.append(line)
    if SECRET_PLACEHOLDER not in example_text:
        print("Warning: SECRET_KEY placeholder not found; ensured SECRET_KEY is still replaced.")
    return "\n".join(lines) + "\n"


def confirm_overwrite() -> bool:
    """Prompt the user before overwriting an existing .env file."""
    while True:
        choice = input(".env already exists. Overwrite? [y/N]: ").strip().lower()
        if choice in {"y", "yes"}:
            return True
        if choice in {"", "n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def main() -> None:
    if not EXAMPLE_PATH.exists():
        raise SystemExit(".env.example not found. Please ensure you are in the project root.")

    if ENV_PATH.exists() and not confirm_overwrite():
        print("Aborted. Existing .env left unchanged.")
        return

    example_text = EXAMPLE_PATH.read_text(encoding="utf-8")
    secret_key = generate_secret_key()
    env_text = build_env_content(example_text, secret_key)

    ENV_PATH.write_text(env_text, encoding="utf-8")
    print("\nCreated .env with a new SECRET_KEY.")
    print("Next steps:")
    print("  - Fill in any production-only settings (AWS_*, Stripe, Sentry, etc.) if deploying.")
    print("  - Keep .env out of version control; use a secrets manager for production.")
    print("  - Run migrations and start the app: python manage.py migrate && python manage.py runserver")


if __name__ == "__main__":
    main()
