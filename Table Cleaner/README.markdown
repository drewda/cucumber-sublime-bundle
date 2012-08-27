# Table Cleaner for Sublime Text 2

## What it does?

Aligns and cleans the tables for a prettier output. Useful for programming languages like Cucumber or LaTex.

## Before

![Table Cleaner Before](https://dl.dropbox.com/u/8314245/TableCleanerBefore.png)

## After

![Table Cleaner After](https://dl.dropbox.com/u/8314245/TableCleanerAfter.png)

## Installation

### Using Sublime Package Control

If you are using Will Bond's excellent [Sublime Package Control](http://wbond.net/sublime_packages/package_control), you can easily install the Table Cleaner package via the `Package Control: Install Package` menu item.

### Using Git

Alternatively, if you are a git user, you can install the package and keep up to date by cloning the repo directly into your `Packages` directory in the Sublime Text 2 application settings area.

Go to your Sublime Text 2 `Packages` directory and clone the package repository using the command below:

    https://github.com/mishu91/Sublime-Text-2-Table-Cleaner "Table Cleaner"

### Download Manually

* Download the files using the GitHub .zip download option
* Unzip the files and rename the folder to `Table Cleaner`
* Copy the folder to your Sublime Text 2 `Packages` directory

## Settings
These settings can be found in Base File.sublime-settings
- **table_cleaner_delimiters** - Delimiters between two cells of the table - default: **["|", "&"]**
- **table_cleaner_align_to_middle** - Align the text of each cell to middle (if set to false, the text will be alligned to left) - default: **true**
- **table_cleaner_delimiters_white_spaces** - The number of whitespaces between the text of a cell and the delimiters - default: **1**

## How it works
Select the table you want to clean, and press *alt + ;* and the table gets cleaned instantly.

## Contributing
Did you spot any bug or think of a great improvement? Create a new issue, or submit a pull request.

# Changelog
- 0.1.0 Added better support for LaTex tables; added more settings to make it more configurable
- 0.0.1 Initial release
