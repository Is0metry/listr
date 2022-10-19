# YO DAWG I HEARD YOU LIKE LISTS
---
Listr is a simple to-do list application written in Python with a SQLite backend, where every list item can have its own list underneath it. There are (currently) no restrictions on how many lists you can have! This was largely inspired by the now-defunct to do list app Clear, which allowed you to keep a single list of lists. The current UI works much like a REPL for a programing language, though I may work on a GUI later. 

## Using
- To launch the application once installed, enter `python /path/to/repo/repl.py`
- entering a number will move to the appropriately numbered sublist
- `<` will move you to the current list's parent
- `!\d` will complete that list item
- `-\d` will delete a list item and all sublists
- `quit` saves and quits
- typing anything else creates a new list in the currently selected sublist
## TODO:
---
- More than the barest minimum of error handling
- Change how to launch
- Cascading completes, so completing a list will automatically complete all sublists (trying to find a way to do it in SQLite, but it's not easy)
- Better navigation (multiple commands at once,)
