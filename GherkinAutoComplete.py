"""
Gherkin Auto-Complete Sublime Text Plugin.

Copyright 2013, Andy Hitchman
Author: Andy Hitchman
Version: 0.1
License: MIT
Description: Show all existing gherkin phrases within features in folder hierarchy
Based on the work of Elad Yarkoni. Thank you!
See http://www.eladyarkoni.com/2012/09/sublime-text-auto-complete-plugin.html
"""
import sublime
import sublime_plugin
import codecs
import os
import re


class Phrase:

    """Gherkin phrase (step)."""

    def __init__(self, phrase, predicate, feature_name, file_name):
        self.phrase = phrase
        self.predicate = predicate
        self.feature_name = feature_name
        self.file_name = file_name


class GherkinPhrases:

    """Phrase collection."""

    phrases = []

    def clearPhrases(self):
        self.phrases = []

    def clearPhrasesForFeatureFile(self, file_name):
        self.phrases = [
            phrase for phrase in self.phrases if phrase.file_name != file_name]

    def addPhrase(self, predicate, phrase, feature_name, file_name):
        self.phrases.append(Phrase(phrase, predicate, feature_name, file_name))
        self.phrases.sort(key=lambda phrase: phrase.phrase)

    def get_match_on(self, activePredicate):
        continuations = '|and|but'
        return '(?P<given>given' + (continuations if activePredicate == 'given' else '') + ')|\
(?P<when>when' + (continuations if activePredicate == 'when' else '') + ')|\
(?P<then>then' + (continuations if activePredicate == 'then' else '') + ')'

    def get_autocomplete_list(self, word, predicate=None):
        word = word.strip()
        autocomplete_list = []
        phrases = set()
        for phrase in self.phrases:
            if (
                (word in phrase.phrase or not word)
                and (predicate == phrase.predicate if predicate else True)
                and phrase.phrase not in phrases
            ):
                autocomplete_list.append(('{phrase.phrase} \t [{phrase.predicate} in {path}]'.format(
                    phrase=phrase,
                    path=os.path.basename(phrase.feature_name)
                ), phrase.phrase))
                phrases.add(phrase.phrase)
        return autocomplete_list

    def is_feature_file(self, filename):
        return '.feature' in filename if filename else False


class GherkinAutoComplete(GherkinPhrases, sublime_plugin.EventListener):

    """Gherkin autocomplete plugin."""

    all_indexed = False

    def get_feature_folders(self, base_path, open_folders):
        if base_path:
            if not os.path.isdir(base_path):
                base_path = os.path.dirname(base_path)

            def find_feature():
                return any(file for file in os.listdir(base_path) if os.path.splitext(file)[1] == '.feature')
            while find_feature():
                base_path = os.path.dirname(base_path)
                if base_path.endswith('features'):
                    yield base_path

    def on_activated_async(self, view):
        if not self.all_indexed:
            self.all_indexed = True
            self.index_all_features(view)

    def on_post_save_async(self, view):
        if self.is_feature_file(view.file_name()):
            if self.all_indexed:
                self.clearPhrasesForFeatureFile(view.file_name())
                self.index_file(view.file_name())
            else:
                self.all_indexed = True
                self.index_all_features(view)

    def index_all_features(self, view):
        self.clearPhrases()
        for folder in self.get_feature_folders(view.file_name(), view.window().folders()):
            feature_files = self.get_feature_files(folder)
            for file_name in feature_files:
                self.index_file(file_name)
        print('Indexing gherkin phrases done')

    def on_query_completions(self, view, prefix, locations):
        completions = []
        search = None

        if self.is_feature_file(view.file_name()):
            predicate = None
            for sel in view.sel():
                if sel.empty():
                    match = None
                    while not match or sel.b > -1:
                        line = view.substr(view.line(sel.b)).strip()
                        if search is None:
                            search = line
                        match = re.match(r'^(given|when|then)', line, re.IGNORECASE)
                        if match:
                            predicate = match.group(0).lower()
                            break
                        else:
                            row, col = view.rowcol(sel.b)
                            sel.b = view.text_point(row - 1, col)
                    break
            search = re.sub(r'^(given|when|then|and)\s?', '', search, flags=re.IGNORECASE)
            print('Searching for', (prefix or search, predicate))
            completions = self.get_autocomplete_list(
                prefix or search, predicate=predicate)

            return (completions, sublime.INHIBIT_EXPLICIT_COMPLETIONS | sublime.INHIBIT_WORD_COMPLETIONS)

    def index_file(self, file_name):
        print('Indexing gherkin phrases in ' + file_name)
        sublime.status_message('Indexing gherkin phrases in ' + file_name)
        self.index_phrases(
            file_name, codecs.open(file_name, 'rU', encoding='utf-8'))

    def index_phrases(self, file_name, lines):
        feature_name = file_name
        activePredicate = None
        collecting_table_data = False
        phrase = None

        for line in lines:
            line = line.strip()
            match = re.match(r'^\s*feature:\s*(.*)$', line, re.IGNORECASE)
            if match is not None:
                feature_name = match.group(1)

            # Collect table data or emit phrase as soon as we have no match
            if activePredicate is not None:
                if re.match(r'^\s*\|', line) is not None:
                    phrase += ('' if collecting_table_data else '\n') + line
                    collecting_table_data = True
                    continue
                elif phrase is not None and phrase != '':
                    collecting_table_data = False
                    self.addPhrase(
                        activePredicate, phrase, feature_name, file_name)

            match_on = self.get_match_on(activePredicate)
            match = re.match(
                r'^\s*(?:' + match_on + ')\s+(.*)$', line, re.IGNORECASE)
            if match is not None:
                if match.group('given'):
                    activePredicate = 'given'
                elif match.group('when') is not None:
                    activePredicate = 'when'
                elif match.group('then') is not None:
                    activePredicate = 'then'

                phrase = match.group(4)
            else:
                activePredicate = None

    def get_feature_files(self, dir_name, *args):
        fileList = set()

        for file in os.listdir(dir_name):
            dirfile = os.path.join(dir_name, file)
            if os.path.isfile(dirfile):
                fileName, fileExtension = os.path.splitext(dirfile)
                if fileExtension == '.feature':
                    fileList.add(dirfile)
            elif os.path.isdir(dirfile):
                fileList.update(self.get_feature_files(dirfile, *args))

        return fileList
