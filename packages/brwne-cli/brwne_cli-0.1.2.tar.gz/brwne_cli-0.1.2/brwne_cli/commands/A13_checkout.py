import click

from brwne_cli.utils.ANSI_Colors import *

def checkout_command():
    click.echo(f"the checkout command has been {RED}deprecated{RESET}.\nPlease use the {BLACK_BG_WHITE_TEXT}`br switch`{RESET} to change branches and {BLACK_BG_WHITE_TEXT}`br branch`{RESET} to create a new branch")