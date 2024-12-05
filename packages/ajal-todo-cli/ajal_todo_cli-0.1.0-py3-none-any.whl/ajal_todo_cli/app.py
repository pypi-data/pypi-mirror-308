#!/usr/bin/env python3
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import typer

cli = typer.Typer()
base_dir = Path(__file__).absolute().parent


# == Helper classes and functions ==


@dataclass
class LeafTask:
    completed: bool = False


@dataclass
class RootTask(LeafTask):
    tasks: dict[str, LeafTask] = field(default_factory=dict)


def todo_parse(todo_file: Path) -> dict[str, RootTask]:
    root_task = None
    tasks = {}
    for line in todo_file.read_text().splitlines():
        if matches := re.match(r"^-\s+(\[(?P<status>[x ])]\s+)?(?P<task>.+)$", line.rstrip()):
            task_name = matches.group("task")
            root_task = RootTask(completed=matches.group("status") == "x")
            tasks[task_name] = root_task
        elif matches := re.match(r"^\s+-\s+(\[(?P<status>[x ])]\s+)?(?P<task>.+)$", line.rstrip()):
            root_task.tasks[matches.group("task")] = LeafTask(completed=matches.group("status") == "x")
    return tasks


def todo_render(tasks: dict[str, RootTask]) -> str:
    lines = ["# A ToDo list", ""]
    for root_task_name, root_task in tasks.items():  # type: str, RootTask
        lines.append(f"- [{'x' if root_task.completed else ' '}] {root_task_name}")
        for leaf_task_name, task in root_task.tasks.items():
            lines.append(f"  - [{'x' if task.completed else ' '}] {leaf_task_name}")
    lines += [""]
    return "\n".join(lines)


def todo_write(todo_file: Path, todo: dict[str, RootTask]):
    todo_file.write_text(todo_render(tasks=todo))


# == CLI helpers ==


def root_callback(ctx: typer.Context, root: str = None) -> str | None:
    if root is None:
        return root

    if root not in ctx.obj["tasks"]:
        typer.echo(f"Root task '{root}' does not exist", err=True)
        raise typer.Exit(1)
    else:
        ctx.obj.update({
            "tasks_root": ctx.obj["tasks"][root].tasks,
            "tasks_class": LeafTask,
        })

    return root


@cli.callback()
def main_callback(
        ctx: typer.Context,
        todo_file: Path = lambda: base_dir / "todo.md",
        verbose: bool = typer.Option(False, "--verbose", "-v", help="Set verbosity"),
):
    ctx.obj = dict(ctx.params)
    if not todo_file.exists():
        typer.echo(f"--todo-file '{todo_file}' does not exist", err=True)
        raise typer.Exit(1)
    tasks = todo_parse(todo_file)
    ctx.obj.update({
        "tasks": tasks,
        "tasks_root": tasks,
        "task_class": RootTask,
    })


# == CLI definitions ==


@cli.command(name="list")
def task_list(
        ctx: typer.Context,
        root: Optional[str] = typer.Option(None, "--root", "-r", help="Root task", callback=root_callback),
):
    """
    List all tasks in todo.md

    Returns all tasks if no root task is passed, otherwise only the root task and subtasks
    """
    ctx.obj["verbose"] and typer.echo(f"Listing tasks in '{root if root else 'root'}'")
    if root is None:
        typer.echo(todo_render(ctx.obj["tasks"]))
    else:
        typer.echo(todo_render({root: ctx.obj["tasks"][root]}))


@cli.command(name="add")
def task_add(
        ctx: typer.Context,
        task: str = typer.Argument(..., help="Task name"),
        root: Optional[str] = typer.Option(None, "--root", "-r", help="Root task", callback=root_callback),
):
    """
    Add a task to todo.md
    """
    ctx.obj["verbose"] and typer.echo(f"Adding task '{task}' to '{root if root else 'root'}'")
    ctx.obj["tasks_root"][task] = ctx.obj["task_class"]()
    todo_write(ctx.obj["todo_file"], ctx.obj["tasks"])
    typer.echo(todo_render(ctx.obj["tasks"]))


@cli.command(name="complete")
def task_complete(
        ctx: typer.Context,
        task: str = typer.Argument(..., help="Task name"),
        root: Optional[str] = typer.Option(None, "--root", "-r", help="Root task", callback=root_callback),
):
    """
    Mark a task in todo.md as completed
    """
    ctx.obj["verbose"] and typer.echo(f"Marking task '{task}' in '{root if root else 'root'}' as completed")
    ctx.obj["tasks_root"][task].completed = True
    todo_write(ctx.obj["todo_file"], ctx.obj["tasks"])
    typer.echo(todo_render(ctx.obj["tasks"]))


@cli.command(name="remove")
def task_remove(
        ctx: typer.Context,
        task: str = typer.Argument(..., help="Task name"),
        root: Optional[str] = typer.Option(None, "--root", "-r", help="Root task", callback=root_callback),
):
    """
    Remove a task from todo.md
    """
    ctx.obj["verbose"] and typer.echo(f"Removing task '{task}' from '{root if root else 'root'}'")
    del ctx.obj["tasks_root"][task]
    todo_write(ctx.obj["todo_file"], ctx.obj["tasks"])
    typer.echo(todo_render(ctx.obj["tasks"]))


if __name__ == "__main__":
    cli()
