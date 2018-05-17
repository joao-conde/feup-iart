class Paper():
    def __init__(self, id, title, speaker, themes, duration):
        self.id = id
        self.title = title
        self.speaker = speaker
        self.themes = themes
        self.duration = int(duration)  # Either 20 mins (short-paper) or 30 mins (full-paper).

    def __str__(self):
        return "paper: " + str(self.id) + " ; " + self.title + " ; " + self.speaker + " ; " + str(self.duration)
         


