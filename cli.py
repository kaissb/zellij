# Zellij/cli.py
import click
import os
import secrets


@click.group()
def cli():
    pass


@click.command()
@click.argument("project_name")
def startproject(project_name):
    base_path = os.path.join(os.getcwd(), project_name)
    os.makedirs(base_path, exist_ok=True)

    # Generate a simple secret token
    secret_token = secrets.token_urlsafe(32)

    # Default settings content
    settings_content = f"""
app:
  debug: True
  secret_key: "{secret_token}"
  database_url: "sqlite:///{project_name}.db"
  port: 8000
"""
    # Create settings.yaml with the default settings
    with open(os.path.join(base_path, "settings.yaml"), "w") as f:
        f.write(settings_content.strip())

    # Create other scaffold files (as previously defined)
    with open(os.path.join(base_path, "models.py"), "w") as f:
        f.write(
            "from zellij import db\n\nclass Models(db.Model):\n    user = {}\n    account = {}\n"
        )
    with open(os.path.join(base_path, "controllers.py"), "w") as f:
        f.write("class Controllers:\n    pass\n")
    with open(os.path.join(base_path, "urls.py"), "w") as f:
        f.write("class URLs:\n    pass\n")


cli.add_command(startproject)

if __name__ == "__main__":
    cli()
