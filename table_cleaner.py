# Author: Andrei Misarca

import table_commons
import copy


class TableCleanerCommand(table_commons.TextCommand):
    # Default separator, all the recognised separators being replaced with this
    # one, before aligning the tables, acting as an intermediate.
    SEPARATOR = "&"

    def run(self, edit):
        self.edit = edit
        self.get_settings()

        orig_lines = self.filter_lines(self.selected_lines())
        lines, separator = self.replace_separator(orig_lines), self.SEPARATOR

        # If no separator has been found, then do not perform any changes
        if lines:
            lines, front_whites = self.front_whitespaces(lines)
            self.align(lines, orig_lines, front_whites)

    # Select only the lines that contain at least one separator.
    def filter_lines(self, lines):
        new_lines = []

        for line in lines:
            sep_found = False

            # If at least one separator can be found on the current line, add
            # it to the list of lines that will be arranged.
            for sep in self.separators:
                if sep in line[1]:
                    sep_found = True

            if sep_found:
                new_lines.append(line)

        return new_lines

    # Replace all separators with the default one.
    def replace_separator(self, lines):
        new_lines = []
        for line in lines:
            new_line = copy.deepcopy(line)

            # Replace the separators with the default one.
            for sep in self.separators:
                new_line[1] = new_line[1].replace(sep, self.SEPARATOR)
            new_lines.append(new_line)

        return new_lines

    # Retrieve all the settings from the settings file and store them in
    # instance variables
    def get_settings(self):
        self.separators = (self.view.settings()
                               .get('table_cleaner_delimiters', ['|', '&']))
        self.align_to_middle = (self.view.settings()
                                    .get('table_cleaner_align_to_middle',
                                         False))
        self.delimiter_spaces = (self.view.settings()
                                     .get('table_cleaner_delimiter_spaces', 1))

    # Split the lines by a separator
    def split_lines(self, lines, separator):
        for line in lines:
            line[1] = line[1].split(separator)

        return lines

    # Replace the old lines with the new ones, containing the cleaned table
    def render_lines(self, lines, front_whites):
        for line in lines:
            new_line = front_whites + line[1] + "\n"
            self.replace_line(self.edit, line[0], new_line)

    # Create a generator that yields the separators from a line
    def orig_separators(self, line):
        for i in xrange(len(line)):
            for sep in self.separators:
                if line[i:].startswith(sep):
                    yield sep

    # Restore the separators of a line, given the original line. The separators
    # are going to be restored in the order they appeared in the original
    # string.
    def restore_line(self, line, orig_line):
        it = self.orig_separators(orig_line)
        new_line = list(line)

        for i in xrange(len(new_line)):
            if new_line[i] == self.SEPARATOR:
                new_line = new_line[:i] + [it.next()] + new_line[i+1:]

        return "".join(new_line)

    def restore_lines(self, lines, orig_lines):
        # print(orig_lines)
        for i in xrange(len(lines)):
            lines[i][1] = self.restore_line(self.SEPARATOR.join(lines[i][1]),
                                            orig_lines[i][1])
        return lines

    # Perform the alignment
    def align(self, lines, orig_lines, front_whites):
        lines = self.split_lines(lines, self.SEPARATOR)

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
                    # Determine the number of characters that need to be
                    # inserted to left and to right
                    l_diff = diff / 2
                    r_diff = diff - l_diff

                    # If the current column is the first column, do not insert
                    # the delimiters white spaces to the left
                    if col == 0:
                        cell = ((l_diff * " ") + cell + (" " * r_diff) +
                                (self.delimiter_spaces * " "))

                        # If the column only contains a whitespace,
                        # then remove it
                        if cell == " ":
                            cell = ""
                    else:
                        cell = ((self.delimiter_spaces * " ") +
                                (l_diff * " ") + cell + (" " * r_diff) +
                                (self.delimiter_spaces * " "))

                else:
                    if col == 0:
                        cell = (cell + (" " * diff) +
                                self.delimiter_spaces * " ")

                        if cell == " ":
                            cell = ""
                    else:
                        cell = (" " + cell + (" " * diff) +
                                self.delimiter_spaces * " ")

                lines[row][1][col] = cell

        lines = self.restore_lines(lines, orig_lines)
        self.render_lines(lines, front_whites)
