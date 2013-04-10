# Author: Andrei Misarca

import table_commons


class TableImportCommand(table_commons.TextCommand):
    def run(self, edit):
        self.edit = edit
        self.get_settings()

        lines = self.selected_lines()

        # Replace the tabs with separators, and then run the command that
        # cleans and allings the table.
        self.replace_tabs_with_separators(lines)
        self.view.run_command("table_cleaner")

    def get_settings(self):
        self.separator = (self.view.settings()
                              .get('table_import_separator', '|'))
        self.sorround = (self.view.settings()
                             .get('table_import_sorround_with_separator',
                                  True))

    def insert_separator_at(self, line, col):
        point = self.view.text_point(line, col)
        self.view.insert(self.edit, point, self.separator)

    # Replace all the tabs with separators.
    def replace_tabs_with_separators(self, lines):
        for line in lines:
            # Count the separators, in order to compute the new length of the
            # line.
            seps_no = 0
            for j in xrange(len(line[1])):
                if line[1][j].startswith('\t'):
                    seps_no += 1
                    self.insert_separator_at(line[0], j+1)

            # If the sorround setting is set to true, then put a separator at
            # the beginning and at the end of the line.
            if self.sorround:
                self.insert_separator_at(line[0], 0)
                self.insert_separator_at(line[0],
                                         (len(line[1]) +
                                         seps_no * len(self.separator)))
