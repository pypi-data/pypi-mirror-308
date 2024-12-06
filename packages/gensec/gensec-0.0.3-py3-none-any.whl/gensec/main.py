import click
from InquirerPy import inquirer
from gensec.commands.set_dockerfile_template import main_dockerfile
from gensec.commands.set_helm_template import main_helmchart

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """Generate a secure resource based on the specified type."""
    # Check if no command was invoked
    if ctx.invoked_subcommand is None:
        click.echo("Error: No command provided. Use '--help' to see available commands.", err=True)
        ctx.exit(1)
    
@main.command(name='dockerfile')
@click.option(
    '--langugaue',
    type=str,
    help='Programming language to use. example: python.')
@click.option(
    '--port',
    type=int,
    help='Port number to expose. example: 8080.')
@click.option(
    '--entrypoint',
    help='Entrypoint for the application. example: main.py.')
@click.help_option(
    help="Show help information for this command.")
def dockerfile(langugaue, port, entrypoint):
    """Generate a Dockerfile."""
    if langugaue == None:
        langugaue = inquirer.select(
            message="Please select a programming language:",
            choices=["python"],
            default="python"
        ).execute()

    if entrypoint == None:
        entrypoint = inquirer.text(
            message="Please enter app entry point:",
            default="main.py"
        ).execute()

    if port == None:
        port = inquirer.text(
            message="Please enter the port number:",
            default="8080"
        ).execute()

    new_dockerfile_name = f"{langugaue}_dockerfile"
    dockerfile_template = f"templates/{langugaue}_dockerfile"
    main_dockerfile(new_dockerfile_name, dockerfile_template, port, entrypoint)

@main.command(name='helmchart')
@click.option(
    '--name',
    help='name of the service. example: dummy-app')
@click.help_option(
    help="Show help information for this command.")
def helmchart(name):
    """Generate a HelmChart."""
    if name == None:
        name = inquirer.text(
            message="Please enter a name for the helmchart:",
            default="dummy-app"
        ).execute()
    main_helmchart(name)

@main.command(name='list')
def list_commands():
    """List available commands."""
    click.echo("Available commands:")
    click.echo("  - dockerfile: Generate a Dockerfile.")
    click.echo("  - helmchart: Generate a Helm chart.")
    click.echo("Use '--help' with each command for more details.")

if __name__ == "__main__":
    main()