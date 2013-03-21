# Author: Andrei Misarca

import sublime_plugin


class TextCommand(sublime_plugin.TextCommand):

    # Return an array containing the number of the selected lines
    def selected_line_numbers(self):
        view = self.view
        sels = view.sel()

        line_nums = []
        for sel in sels:
            line_nums += [view.rowcol(line.a)[0] for line in view.lines(sel)]
        return line_nums

    # Return an array containing the selected lines, and the line number
    def selected_lines(self):
        line_nums = self.selected_line_numbers()
        return [[line, self.get_line(line)] for line in line_nums]

    # Return a string containing the line given as parameter
    def get_line(self, line_num):
        return self.view.substr(self.view.full_line(
            self.view.text_point(line_num, 0)))

    # Trim the left whitespaces from each line, and retrieve the whitespace
    # characters that appear at the beginning of each line
    def front_whitespaces(self, lines):
        # The number of whitespaces at the beginning of the lines, it is set to
        # a very high value
        front_indent_size = 120
        front_whites = ""

        for line in lines:
            # Get the stripped version of the line, and find how many
            # whitespaces there are at the beginning of the line
            stripped_line = line[1].lstrip()
            front_whites_size = len(line[1]) - len(stripped_line)

            # Find the length of the shortest whitespace, and store that
            # whitespace
            if front_indent_size > front_whites_size:
                front_indent_size = front_whites_size
                front_whites = line[1][0:front_whites_size]

            # The line gets stripped
            line[1] = stripped_line

        return lines, front_whites

    # Replace the line with the index line_num with string
    def replace_line(self, edit, line_num, string):
        region = self.view.full_line(self.view.text_point(line_num, 0))
        self.view.replace(edit, region, string)
