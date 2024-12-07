"""
Bucket Dependency Manager by Astridot as part of Makoschin Free Software Distributions

This program is free software: you can redistribute it and/or modify
it under the terms of the Makoschin Free Software License (MFSL),
either version 1.0 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
Makoschin Free Software License for more details.
"""

import argparse
from .core import Bucket

def main():
    parser = argparse.ArgumentParser(description="Bucket CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Initialize, Destroy, Run, Set, and Web Commands
    subparsers.add_parser("init", help="Initialize a new Bucket")
    subparsers.add_parser("destroy", help="Destroy an existing Bucket")
    run_parser = subparsers.add_parser("run", help="Run the Bucket entrypoint command")
    run_parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments for the entrypoint")

    set_parser = subparsers.add_parser("set", help="Set Bucket properties")
    set_parser.add_argument("property", choices=["entrypoint", "author"], help="Property to set")
    set_parser.add_argument("value", nargs="+", help="Value to set")

    web_parser = subparsers.add_parser("web", help="Manage Bucket web interface")
    web_parser.add_argument("subcommand", choices=["update", "open"], help="Subcommand for web interface")

    # Dependency Command
    dep_parser = subparsers.add_parser("dep", help="Manage Bucket dependencies")
    dep_subparsers = dep_parser.add_subparsers(dest="subcommand", required=True)

    for cmd in ["add", "edit"]:
        sub = dep_subparsers.add_parser(cmd)
        sub.add_argument("name")
        sub.add_argument("source")
        sub.add_argument("version", nargs="?", default="latest")
        sub.add_argument("install_command", nargs="?", default=None)

    dep_subparsers.add_parser("list", help="List all dependencies")
    install_parser = dep_subparsers.add_parser("install", help="Install dependencies")
    install_parser.add_argument("name", nargs="?", default="*")
    rm_parser = dep_subparsers.add_parser("rm", help="Remove dependencies")
    rm_parser.add_argument("name", help="Dependency name or '*' to remove all")

    version_parser = subparsers.add_parser("vs", help="Manage Bucket versions")
    version_subparsers = version_parser.add_subparsers(dest="subcommand", required=True)
    version_subparsers.add_parser("commit", help="Save a version snapshot")
    rollback_parser = version_subparsers.add_parser("rollback", help="Rollback to a specific version")
    rollback_parser.add_argument("timestamp", help="Version timestamp to rollback to")
    rollback_parser.add_argument("timestamp2", help="Second part of the version timestamp to rollback to")
    version_subparsers.add_parser("history", help="List all saved versions")

    pr_parser = subparsers.add_parser("pr", help="Manage pull requests")
    pr_subparsers = pr_parser.add_subparsers(dest="subcommand", required=True)
    pr_create = pr_subparsers.add_parser("create", help="Create a new pull request")
    pr_create.add_argument("source")
    pr_create.add_argument("target")
    pr_create.add_argument("description")
    pr_approve = pr_subparsers.add_parser("approve", help="Approve and merge a pull request")
    pr_approve.add_argument("id")
    pr_approve.add_argument("id2")
    pr_subparsers.add_parser("list", help="List all pull requests")
    pr_info = pr_subparsers.add_parser("info", help="Get the diagnosis of a pull request")
    pr_info.add_argument("id")
    pr_info.add_argument("id2")

    branch_parser = subparsers.add_parser("branch", help="Manage branches")
    branch_subparsers = branch_parser.add_subparsers(dest="subcommand", required=True)
    branch_create = branch_subparsers.add_parser("create", help="Create a new branch")
    branch_create.add_argument("name")

    branch_switch = branch_subparsers.add_parser("switch", help="Switch to an existing branch")
    branch_switch.add_argument("name")

    branch_rm = branch_subparsers.add_parser("rm", help="Remove an existing branch")
    branch_rm.add_argument("name")

    branch_subparsers.add_parser("list", help="List all branches")

    # Execute parsed arguments
    args = parser.parse_args()
    bucket = Bucket(directory=args.dir if 'dir' in args else ".")

    match args.command:
        case "init": bucket.init()
        case "destroy": bucket.destroy()
        case "vs":
            match args.subcommand:
                case "commit":
                    bucket.commit_version()
                case "rollback":
                    bucket.rollback_version(f"{args.timestamp} {args.timestamp2}")
                case "history":
                    bucket.list_versions()
        case "run": bucket.run(args.args)
        case "set": bucket.set_property(args.property, " ".join(args.value))
        case "web": bucket.manage_web(args.subcommand)
        case "dep":
            match args.subcommand:
                case "add": bucket.add_or_edit_dependency(args.name, args.source, args.version, args.install_command)
                case "edit": bucket.add_or_edit_dependency(args.name, args.source, args.version, args.install_command, edit=True)
                case "list": bucket.list_dependencies()
                case "install": bucket.install_dependencies(args.name)
                case "rm": bucket.remove_dependency(args.name)
        case "branch":
            match args.subcommand:
                case "create": bucket.create_branch(args.name)
                case "switch": bucket.switch_branch(args.name)
                case "list": bucket.list_branches()
                case "rm": bucket.delete_branch(args.name)
        case "pr":
            match args.subcommand:
                case "create": bucket.create_pull_request(args.source, args.target, args.description)
                case "list": bucket.list_pull_requests()
                case "approve": bucket.approve_pull_request(f"{args.id} {args.id2}")
                case "info": bucket.get_pull_request_description(f"{args.id} {args.id2}")