class LargeTextManager:

    def __init__(self, indent="    ", endpar="\n\n"):
        self.indent = indent
        self.endpar = endpar
        self.paragraphs = []

    def paragraph(self,*text):
        """Add a new paragraph"""
        if len(self.paragraphs) > 0:
            self.end_paragraph()
            content = self.indent
        else:
            content =""
        for t in text:
            content += t
        self.paragraphs.append(content)

    def end_paragraph(self):
        self.paragraphs[-1] += self.endpar

    def more(self, *text):
        """Append to the current paragraph"""
        for t in text:
            self.paragraphs[-1] += t

    def get_all(self):
        text = ""
        for p in self.paragraphs:
            text += p
        return text