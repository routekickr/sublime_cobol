import sublime, sublime_plugin

class CobolSequenceNumbersRemoveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.find_all('^[0-9][0-9][0-9][0-9][0-9][0-9]')
        regions.reverse()
        for region in regions:
            self.view.replace(edit,region, '      ')


class CobolInsertSequenceNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selected_region = self.view.sel()[0]
        if selected_region.size() == 0:
            text = self.view.substr(sublime.Region(0, self.view.size()))
        else:
            text = self.view.substr(sublime.Region(selected_region.begin(), selected_region.end()))
        lines = text.split("\n")
        text = ""
        for idx, val in enumerate(lines):
            text = text + "{0:06d}".format(idx + 1) + val[6:] + "\n"
        if selected_region.size() == 0:
            self.view.replace(edit, sublime.Region(0, self.view.size()), text)
        else:
            self.view.replace(edit, sublime.Region(selected_region.begin(), selected_region.end()), text)



class CobolAddBlankSequenceArea(sublime_plugin.TextCommand):
    def run(self, edit):
        selected_region = self.view.sel()[0]
        if selected_region.size() == 0:
            text = self.view.substr(sublime.Region(0, self.view.size()))
        else:
            text = self.view.substr(sublime.Region(selected_region.begin(), selected_region.end()))
        lines = text.split("\n")
        text = ""
        for idx, val in enumerate(lines):
            text = text + "      " + val + "\n"
        if selected_region.size() == 0:
            self.view.replace(edit, sublime.Region(0, self.view.size()), text)
        else:
            self.view.replace(edit, sublime.Region(selected_region.begin(), selected_region.end()), text)


class CobolRemoveSequenceArea(sublime_plugin.TextCommand):
   def run(self, edit):
        selected_region = self.view.sel()[0]

        if selected_region.size() == 0:
            text = self.view.substr(sublime.Region(0, self.view.size()))
        else:
            text = self.view.substr(sublime.Region(selected_region.begin(), selected_region.end()))
        lines = text.split("\n")
        text = ""
        for idx, val in enumerate(lines):
            text = text + val[6:] + "\n"
        if selected_region.size() == 0:
            self.view.replace(edit, sublime.Region(0, self.view.size()), text)
        else:
            self.view.replace(edit, sublime.Region(selected_region.begin(), selected_region.end()), text)                      