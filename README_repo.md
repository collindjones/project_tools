Based very heavily on Jeremy Bejarano's excellent blank_project repo: https://github.com/jmbejara/blank_project/tree/main

# Cloning Instructions
1. Clone the git repo, with the submodule recurse option: `git clone --recurse-submodules git@github.com:...`
2. Create the symlink structure in the sphinx documentation. In the top-level directory,

```
ln -s reports docs/source/reports
ln -s notes docs/source/notes
```

3. Run doit in the top-level directory

# General Directory Structure
* The assets folder is used for things like hand-drawn figures or other pictures that were not generated from code. These things cannot be easily recreated if they are deleted.
* The _output folder, on the other hand, contains dataframes and figures that are generated from code. The entire folder should be able to be deleted, because the code can be run again, which would again generate all of the contents.
* The data_manual is for data that cannot be easily recreated. This data should be version controlled. Anything in the _data folder or in the _output folder should be able to be recreated by running the code and can safely be deleted.
* I'm using the doit Python module as a task runner. It works like make and the associated Makefiles. To rerun the code, install doit (https://pydoit.org/) and execute the command doit from the src directory. Note that doit is very flexible and can be used to run code commands from the command prompt, thus making it suitable for projects that use scripts written in multiple different programming languages.
* I'm using the .env file as a container for absolute paths that are private to each collaborator in the project. You can also use it for private credentials, if needed. It should not be tracked in Git.

# Data and Output Storage
* I'll often use a separate folder for storing data. Any data in the data folder can be deleted and recreated by rerunning the PyDoit command (the pulls are in the dodo.py file). Any data that cannot be automatically recreated should be stored in the "data_manual" folder. Because of the risk of manually-created data getting changed or lost, I prefer to keep it under version control if I can. Thus, data in the "_data" folder is excluded from Git (see the .gitignore file), while the "data_manual" folder is tracked by Git.
* Output is stored in the "_output" directory. This includes dataframes, charts, and rendered notebooks. When the output is small enough, I'll keep this under version control. I like this because I can keep track of how dataframes change as my analysis progresses, for example.
* Of course, the _data directory and _output directory can be kept elsewhere on the machine. To make this easy, I always include the ability to customize these locations by defining the path to these directories in environment variables, which I intend to be defined in the .env file, though they can also simply be defined on the command line or elsewhere. The settings.py is reponsible for loading these environment variables and doing some like preprocessing on them. The settings.py file is the entry point for all other scripts to these definitions. That is, all code that references these variables and others are loading by importing config.

# Naming Conventions
* pull_ vs load_: Files or functions that pull data from an external data source are prepended with "pull_", as in "pull_fred.py". Functions that load data that has been cached in the "data" folder are prepended with "load". For example, inside of the pull_CRSP_Compustat.py file there is both a pull_compustat function and a load_compustat function. The first pulls from the web, whereas the other loads cached data from the "_data" directory.