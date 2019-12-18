# ✨TODO AF✨

A todo app for people who spend time in the terminal.

## Install

todo.af runs on python3. I usually install via brew (on macOS):

```
brew install python3
```

Once you have python, you'll need to touch a blank todo file, then tell todo.af
where this file is. Create a config file in your home folder:

```
touch ~/.todo.cfg
```

Edit the file and enter something like the following:

```
[default]
todofile = ~/todo
```

You can add an alias to .bash_profile like so:
```
alias todo='$HOME/path/to/python3 $HOME/path/to/todo/todo.py'
```

## Usage

The main commands are;

- `todo` show your todo list.
- `todo add <your task here>` add a task to the end of the list.
- `todo delete <task number>` delete a task completely.
- `todo complete <task number>` move a task to the archive.
- `todo use <path to todo file>` switch todo files
