# Author: Andrei Misarca

import sublime, sublime_plugin
import re, os, sys

class TableCleanerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.get_settings()

        lines, separator = self.get_separator(self.selected_lines())

        # If no separator has been found, then do not perform any changes
        if separator:
            lines, front_whites = self.front_whitespaces(lines)

            self.align(edit, lines, separator, front_whites)

    # Retrieve all the settings from the settings file and store them in
    # instance variables
    def get_settings(self):
        self.separators = self.view.settings() \
            .get('table_cleaner_delimiters', ['|', '&'])
        self.align_to_middle = self.view.settings() \
            .get('table_cleaner_align_to_middle', False)
        self.delimiters_white_spaces = self.view.settings() \
            .get('table_cleaner_delimiters_white_spaces', 1)

    # Replace the line with the index line_num with string
    def replace_line(self, edit, line_num, string):
        region = self.view.full_line(self.view.text_point(line_num, 0))
        self.view.replace(edit, region, string)

    # Trim the left whitespaces from each line, and retrieve the whitespace
    # characters that appear at the beginning of each line
    def front_whitespaces(self, lines):
        # The number of whitespaces at the beginning of the lines, it is set to
        # a very high value
        front_indent_size = 120
        front_whites = ""

        for line in lines:
            # Get the stripped version of the line, and find how many whitespaces
            # there are at the beginning of the line
            stripped_line = line[1].lstrip()
            front_whites_size = len(line[1]) - len(stripped_line)

            # Find the length of the shortest whitespace, and store that whitespace
            if front_indent_size > front_whites_size:
                front_indent_size = front_whites_size
                front_whites = line[1][0:front_whites_size]

            # The line gets stripped
            line[1] = stripped_line

        return lines, front_whites

    # Find the separator for the selected table, and delete from the lines set
    # the lines that do not contain the separator
    def get_separator(self, lines):
        separator = None

        for line in lines[:]:
            separator_found = False

            for sep in self.separators:
                if sep in line[1]:
                    separator_found = True

                    if separator == None:
                        separator = sep

            if not separator_found:
                lines.remove(line)

        return lines, separator

    # Return a string containing the line given as parameter
    def get_line(self, line_num):
        return self.view.substr(self.view.full_line(self.view.text_point(line_num, 0)))

    # Return an array containing the selected lines
    def selected_lines(self):
        view = self.view
        sel = view.sel()
        line_nums = [view.rowcol(line.a)[0] for line in view.lines(sel[0])]
        return [[line, self.get_line(line)] for line in line_nums]

    # Split the lines by a separator
    def split_lines(self, lines, separator):
        for line in lines:
            line[1] = line[1].split(separator)

        return lines

    # Replace the old lines with the new ones, containing the cleaned table
    def render_lines(self, edit, lines, separator, front_whites):
        for line in lines:
            new_line = front_whites + separator.join(line[1]) + "\n"
            self.replace_line(edit, line[0], new_line)

    # Perform the alignment
    def align(self, edit, lines, separator, front_whites):
        lines = self.split_lines(lines, separator)

        # Find the sizes of the table
        rows_size = len(lines)
        cols_size = min([len(line[1]) for line in lines])

        for col in xrange(0, cols_size):
            max_len = 0

            # Find the largest cell on the current column
            for row in xrange(0, rows_size):
                max_len = max(max_len, len(lines[row][1][col].strip()))

            for row in xrange(0, rows_size):
                cell = lines[row][1][col].strip()

                diff = max_len - len(cell)

                if self.align_to_middle:
                    # Determine the number of characters that need to be inserted
                    # to left and to right
                    l_diff = diff / 2
                    r_diff = diff - l_diff

                    # If the current column is the first column, do not insert
                    # the delimiters white spaces to the left
                    if col == 0:
                        cell = (l_diff * " ") + cell + (" " * r_diff) + \
                            (self.delimiters_white_spaces * " ")

                        # If the column only contains a whitespace, then remove it
                        if cell == " ":
                            cell = ""
                    else:
                        cell = (self.delimiters_white_spaces * " ") + \
                            (l_diff * " ") + cell + (" " * r_diff) + \
                            (self.delimiters_white_spaces * " ")

                else:
                    if col == 0:
                        cell = cell + (" " * diff) + self.delimiters_white_spaces * " "

                        if cell == " ":
                            cell = ""
                    else:
                        cell = " " + cell + (" " * diff) + self.delimiters_white_spaces * " "

                lines[row][1][col] = cell

        self.render_lines(edit, lines, separator, front_whites)
