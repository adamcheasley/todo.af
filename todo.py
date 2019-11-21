import configparser
import operator
import os
import sys
from pathlib import Path

END_CODE = '\033[0m'
GREEN = '\033[1;32;40m'
RED = '\033[1;31;40m'
TASKS_BLOCK = '===TASKS==='
ARCHIVE_BLOCK = '===ARCHIVE==='
VERSION = '0.1'


def print_to_terminal(colour_code, message):
    """Print to console using colour codes."""
    print(f'{colour_code} {message}{END_CODE}')


def help():
    """Print out the help docs"""
    print(f'todo as fuck. version {VERSION}')
    print(
        'Usage: todo '
        '[ add <task> ] [ delete <num> ] [ complete <num> ]'
        ' [ up <task> ] [ down <num> ]'
    )


def config_data():
    """Get config"""
    config = configparser.ConfigParser()
    config.read(f'{Path.home()}/.todo.cfg')
    return config


def list(todo_data):
    """List todos."""
    if not todo_data['current']:
        print_to_terminal(GREEN, 'Nothing todo!')
        sys.exit(0)

    print_to_terminal(GREEN, '\nTODO:')
    for i, task in enumerate(todo_data['current']):
        print(f'{i + 1}. {task}')
    print()
    sys.exit(0)


def add(todo_data, task):
    """Add a task."""
    todo_data['current'].append(task)
    print_to_terminal(GREEN, 'Task added.')
    return todo_data


def delete(todo_data, num):
    """Remove task by task number"""
    deleted = todo_data['current'][int(num) - 1]
    del todo_data['current'][int(num) - 1]
    print_to_terminal(GREEN, f'Deleted task - {deleted}.')
    return todo_data


def complete(todo_data, num):
    """Move the task from current to archive"""
    completed = todo_data['current'][int(num) - 1]
    del todo_data['current'][int(num) - 1]
    todo_data['archive'].append(completed)
    print_to_terminal(GREEN, f'Completed task - {completed}.')
    return todo_data


def move(todo_data, num, op):
    """Move task up or down"""
    i = int(num) - 1
    current = todo_data['current']
    current.insert(op(i, 1), current.pop(i))
    return todo_data


def up(todo_data, num):
    """Move task num up one place"""
    todo_data = move(todo_data, num, operator.sub)
    print_to_terminal(GREEN, 'Task bumped up the list.')
    return todo_data


def down(todo_data, num):
    """Move task num down one place"""
    todo_data = move(todo_data, num, operator.add)
    print_to_terminal(GREEN, 'Task knocked down the list.')
    return todo_data


def save_tasks(todo_data, todo_file):
    """Serialse the todos and save the file."""
    raw_data = serialise(todo_data)
    todo_file.seek(0)
    todo_file.write(raw_data)
    todo_file.truncate()
    todo_file.close()


def serialise(data):
    """Serialse the data for writing out to file."""
    out = f'{TASKS_BLOCK}\n'
    for i, task in enumerate(data['current']):
        out += f'{task}\n'
    out += f'{ARCHIVE_BLOCK}\n'
    for task in data['archive']:
        out += f'{task}\n'
    return out


def deserialise(data):
    """Convert raw data into a python object."""
    out = {'current': [], 'archive': []}
    if len(data) == 0:
        # No todos have ever been added. Setup the data.
        return out

    lines = data.split('\n')
    task_start = None
    archive_start = None

    for i, line in enumerate(lines):
        if i == len(lines) - 1:
            return out
        if line == TASKS_BLOCK:
            task_start = i + 1
        if line == ARCHIVE_BLOCK:
            task_start = None
            archive_start = i + 1
        if task_start and i >= task_start:
            # TODO: These need to be turned into task objects (dicts)
            out['current'].append(line)
        elif archive_start and i >= archive_start:
            # TODO: These need to be turned into task objects (dicts)
            out['archive'].append(line)


config = config_data()
todo_file_location = os.path.expanduser(config['default']['todofile'])
try:
    todo_file = open(todo_file_location, 'r+')
except FileNotFoundError:  # noqa
    print_to_terminal(RED, 'Could not find todo file.\n')
    sys.exit(1)
todo_data_raw = todo_file.read()
tasks = deserialise(todo_data_raw)

cli_args = sys.argv
if len(cli_args) == 1:
    # list todos
    list(tasks)
    sys.exit(0)
elif cli_args[1] == 'add':
    todo_data = add(tasks, ' '.join(cli_args[2:]))
elif cli_args[1] == 'help':
    help()
    sys.exit(0)
elif cli_args[1] in {'delete', 'complete', 'up', 'down'}:
    try:
        todo_data = globals()[cli_args[1]](tasks, cli_args[-1])
    except (IndexError, ValueError):
        print_to_terminal(RED, 'Could not find task.')
        todo_data = tasks
elif cli_args[1] == 'which':
    print_to_terminal(GREEN, f'You are using the todo file: {todo_file_location}')
    sys.exit(0)
else:
    print_to_terminal(RED, 'Unknown command.')
    sys.exit(1)

save_tasks(todo_data, todo_file)
