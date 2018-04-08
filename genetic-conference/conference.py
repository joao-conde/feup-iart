import xlsxwriter

class Conference():
    def __init__(self, days):
        self.days = days  # Conference will go on for exactly 3 days.

    def export_to_spreadsheet(self):
        workbook = xlsxwriter.Workbook('conference.xlsx')
        insert_conference_info(self, workbook)
        workbook.close()

class Day():
    def __init__(self, id, sessions):
        self.id = id
        self.sessions = sessions  # 4 sessions maximum on every room.

class Session():
    def __init__(self, id, theme, presentations, room):
        self.id = id
        self.theme = theme  # Every presented paper must have this theme in common.
        self.presentations = presentations  # At least 2 full-paper presentations obligatory.
        self.room = room

    def compute_duration(self):
        return sum([presentation.paper.duration for presentation in self.presentations])

class Presentation():
    def __init__(self, id, paper, speaker, start):
        self.id = id
        self.paper = paper
        self.speaker = speaker  # Must be the paper's author.
        self.start = start

class Paper():
    def __init__(self, id, title, authors, themes, duration):
        self.id = id
        self.title = title
        self.authors = authors
        self.themes = themes
        self.duration = duration  # Either 20 mins (short-paper) or 30 mins (full-paper).

def insert_conference_info(conference, workbook):
    pass


