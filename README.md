# SublimeRJS
###An easier way to import, remove and create modules for the RequireJS module loader.

Based on settings in a configuration file the plugin will parse your source folders and index your modules, enabeling it to automize basic parts of your module handeling.

Importing modules is done through a quick search among the indexed modules. When selected for import the modules path as well as reference variable is automatically added to the ‘define’ statement.

Creating new modules is made easier by quick search of packages(folders), adding custom module templates and auto import of predefined modules.

SublimeRJS supports script as well as text modules.
## Demonstration
Please see the following screencast for a quick feature demonstration.
http://www.youtube.com/watch?v=HlNTheck1Hk
## Usage
* <b>Add to project</b>  
  Right click your project folder and click `Add SublimeRJS`. This will add the configuration file to your project.  
  Edit the configuration acording to your project. Save.
* <b>Menu</b>  
  Press `cmd + m` / `ctrl + m` to open the main menu. This will give you all the options in the quick panel. 
* <b>Open module</b>  
  Press `Cmd+Shift+[7-9])` / `Ctrl+Shift+[7-9]` to open a module in specific column view.


## Configuration
### Example configuration
    {
      "script_folders": [
        "js",
        "libs"
      ],
      "text_folders":[
        "templates"
      ],
      "require_main":"js/main.js",
      "aliases": {
        "jquery":"$",
        "underscore":"_"
      },
      "auto_add":[
        "jquery",
        "underscore",
        "event/eventBus"
      ],
      "script_group":"0",
      "text_group":"1"
    }
### Config elements
#### Source folders
    "script_folders": [
      "js",
      "test"
    ],
    "text_folders":[
      "templates"
    ]
Defines the folders that should be indexed. Relative to the config file.
#### RequireJS main     
    "require_main":"js/main.js"
Refrence to the RequireJS main file. Relative to the config file.
#### Aliases
    "aliases": {
      "jquery":"$",
      "underscore":"_"
    }
Aliases to apply when adding modules to the `define()` statment.
#### Auto add modules
    "auto_add":[
      "jquery",
      "underscore",
      "event/eventBus"
    ]
Modules that will be automatically added when creating a new module.
#### Columns
    "script_group":"0",
    "text_group":"1"
Sets in which column the module type should be opened.
## Install
Download, unzip and move to the `Packages` folder of Sublime Text 2.
## Features to come
* Move / Refactor modules
* Method code hints across modules
* Jump to module definition

## Disclaimer
SublimeRJS is currently at an early stage. It is not recommended to use this for production purpose. All use is at own risk.

Should you choose to look at the source code I should probably advise you that this was my first Python project, and the code will look pretty messy to the experienced Python developer.


