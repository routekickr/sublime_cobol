import sublime, sublime_plugin,codecs,re

class CobolCommentToggleCommand(sublime_plugin.TextCommand):
    def replaceLine(self, lineContents):
        pat = re.compile('[0-9][0-9][0-9][0-9][0-9][0-9][\* ]')
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
                        i = len(lineContents) - len(lineContents.lstrip())
                        lineContents = lineContents[0:i] + '*>' + lineContents[i:]

        return lineContents

    def run(self, edit, block):  
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

