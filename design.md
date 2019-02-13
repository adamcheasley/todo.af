# Untitled CLI Todo Manager

## Features

All tasks are stored in a text file. They are grouped into current tasks and
an archive.

When tasks are added, they go into the current list. When they are completed,
they go into the archive. Archive can be purged.

Tasks can be moved up and down the current list.

## Interaction

- add <task>
- list (this is the default)
- complete <task number>
- delete <task number>
- up <task number>
- down <task number>

## File format

A machine detectable block for current tasks and one for archive.
Possibly something like:
```
==========
TASKS
==========
...

==========
ARCHIVE
==========
...

```

Tasks are listed one per line. Each task has a 'score' which can be
incremented/decremented. This determines the order of tasks in current.
