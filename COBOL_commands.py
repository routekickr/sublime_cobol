import sublime, sublime_plugin,codecs,re

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


class CobolFindProcedureDivision(sublime_plugin.TextCommand):
      def run(self, edit):
        proc_div_region = self.view.find('procedure\s*division', 0, sublime.IGNORECASE)
        if not proc_div_region:
            sublime.error_message("COBOL Procedure Division not found")
            return
        self.view.show(proc_div_region)



class CobolCommentToggleCommand(sublime_plugin.TextCommand):
    def replaceLine(self, lineContents):
        pat = re.compile('[0-9a-zA-Z\-][0-9a-zA-Z\-][0-9a-zA-Z\-][0-9a-zA-Z\-][0-9a-zA-Z\-][0-9a-zA-Z\-][\* ]')
        if pat.match(lineContents):
                if lineContents[6] == '*':
                        lineContents = lineContents[0:6] + ' ' + lineContents[7:]
                else:
                        lineContents = lineContents[0:6] + '*' + lineContents[7:]
        else:
                i = lineContents.find('*>') 

                if i != -1:
                        lineContents = lineContents[0:i] +  lineContents[2+i:]
                else:
                        l = len(lineContents)
                        if ((l > 6) and (lineContents[0:6] == '      ')):
                              i=6
                        else:
                              i = len(lineContents) - len(lineContents.lstrip())
                        lineContents = lineContents[0:i] + '*>' + lineContents[i:]

        return lineContents

    def run(self, edit, block):  
        print('SPG - Skipping -> '+self.view.settings().get('syntax'))
        if self.view.settings().get('syntax') != 'Packages/COBOL Syntax/COBOL.tmLanguage':
                self.view.run_command("toggle_comment", {"block": block})
                return

	
        for region in self.view.sel():  

            if region.empty():  
                # Get the selected text  
                line = self.view.line(region)  
                lineContents = self.replaceLine(self.view.substr(line))
                self.view.replace(edit,line, lineContents)
            else:
                newContent = ''
                for line in self.view.split_by_newlines(region):
                        newContent += self.replaceLine(self.view.substr(line))+"\n"
                self.view.replace(edit,region, newContent.rstrip('\n'))

