# cucumber-sublime2-bundle

A bundle for [Sublime Text 2](http://www.sublimetext.com/2) that provides syntax coloring and snippets for [Cucumber](http://cukes.info/) and its [Gherkin](https://github.com/cucumber/cucumber/wiki/Gherkin) language.

## Installation

### Mac OSX
    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages
    git clone git://github.com/drewda/cucumber-sublime2-bundle.git Cucumber
### Linux
    cd ~/.config/sublime-text-2/Packages
    git clone git://github.com/drewda/cucumber-sublime2-bundle.git Cucumber
### Windows
    cd Users/<user>/AppData/Roaming/Sublime\ Text\ 2/Packages/
    git clone git://github.com/drewda/cucumber-sublime2-bundle.git Cucumber

Restart Sublime Text 2

## Table Cleaner

Aligns and cleans the tables for a prettier output. Useful for programming languages like Cucumber or LaTex.

### Before

![Table Cleaner Before](https://dl.dropbox.com/u/8314245/TableCleanerBefore.png)

### After

![Table Cleaner After](https://dl.dropbox.com/u/8314245/TableCleanerAfter.png)

### Usage
Select the table you want to clean, and press *alt + ;* and the table gets cleaned instantly.

### Settings
These settings can be found in Base File.sublime-settings
- **table_cleaner_delimiters** - Delimiters between two cells of the table - default: **["|", "&", "\\\\"]**
- **table_cleaner_align_to_middle** - Align the text of each cell to middle (if set to false, the text will be alligned to left) - default: **false**
- **table_cleaner_delimiters_white_spaces** - The number of whitespaces between the text of a cell and the delimiters - default: **1**

## Credits
Created by the Github user @sagework, who pulled his/her repo from https://github.com/sagework/cucumber-sublime2-bundle

The Table Cleaner plug-in has been kindly contributed by [@mishu91](https://github.com/mishu91). If you'd like just the plug-in, without the rest of this Cucumber bundle, see his repository at https://github.com/mishu91/Sublime-Text-2-Table-Cleaner

I host this project at https://github.com/drewda/cucumber-sublime2-bundle for those who use Sublime Package Control.
