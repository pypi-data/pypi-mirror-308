import click
import requests
import time
import keyring

from brwne_cli.utils.ANSI_Colors import *
from brwne_cli.arts import get_random_artwork
from brwne_cli.commands.auth import login_command, logout_command
from brwne_cli.commands.A1_init import init_command
from brwne_cli.commands.A2_add import add_command
from brwne_cli.commands.A3_commit import commit_command
from brwne_cli.commands.A4_status import status_command
from brwne_cli.commands.A5_map import map_command
from brwne_cli.commands.A6_branch import branch_command 
from brwne_cli.commands.A7_push import push_command
from brwne_cli.commands.A8_get_cautions import get_cautions
from brwne_cli.commands.A9_cascade import cascade_command
from brwne_cli.commands.A10_submit import submit_command
from brwne_cli.commands.A11_clone import clone_command
from brwne_cli.commands.A12_switch import switch_command
from brwne_cli.commands.A13_checkout import checkout_command

from brwne_cli.utils.pre_command_decorator import pre_command

@click.group()
def cli():
    rf"""brwne CLI Tool\n{get_random_artwork()}"""
    pass

@cli.command()
def greet():
    """Say hello"""
    click.echo(PURPLE + get_random_artwork() + RESET)

@cli.command()
def login():
    """Login to the brwne CLI tool"""
    login_command()

@cli.command()
def logout():
    """Logout by removing tokens from keyring"""
    logout_command()

@cli.command()
def init():
    """Initialize the repository with Brownie"""
    init_command()

@cli.command()
@click.argument('files', nargs=-1)
def add(files):
    """Start tracking changes for given files in the current branch."""
    add_command(files)

@cli.command()
@click.argument('args', nargs=-1)
@click.option('-m', '--message', required=True, help='Commit message')
def commit(message, args):
    commit_command(message)

@cli.command()
def status():
    status_command()

@cli.command()
def map():
    map_command()

@cli.command()
def branch():
    branch_command()

@cli.command()
def push():
    push_command()

@cli.command()
def cautions():
    get_cautions()

@cli.command()
def cascade():
    cascade_command()

@cli.command()
def submit():
    submit_command()

@cli.command()
@click.argument('repo_url')
def clone(repo_url):
    clone_command(repo_url)

@cli.command()
@click.argument('branch_name')
def switch(branch_name):
    switch_command(branch_name)

@cli.command()
@click.argument('commit_hash', required=False)
def checkout(commit_hash=None):
    checkout_command()
    
if __name__ == "__main__":
    cli()
