# Table Cleaner for Sublime Text 2

## What it does?

Aligns and cleans the tables for a prettier output. Useful for programming languages like Cucumber or LaTex.

## Before

![Table Cleaner Before](https://dl.dropbox.com/u/8314245/TableCleanerBefore.png)

## After

![Table Cleaner After](https://dl.dropbox.com/u/8314245/TableCleanerAfter.png)

## Usage
Select the table you want to clean, and press *alt + ;* and the table gets cleaned instantly.

## Settings
These settings can be found in Base File.sublime-settings
- **table_cleaner_delimiters** - Delimiters between two cells of the table - default: **["|", "&"]**
- **table_cleaner_align_to_middle** - Align the text of each cell to middle (if set to false, the text will be alligned to left) - default: **true**
- **table_cleaner_delimiters_white_spaces** - The number of whitespaces between the text of a cell and the delimiters - default: **1**

## Contributing
Did you spot any bug or think of a great improvement? Create a new issue, or submit a pull request.

# Changelog
- 0.1.0 Added better support for LaTex tables; added more settings to make it more configurable
- 0.0.1 Initial release
