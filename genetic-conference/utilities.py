import openpyxl as sheets

"""
"""
def export_to_spreadsheet(wb_path, population):
    wb = sheets.Workbook()
    ws = wb.active
    wb.save(wb_path)


def print_conference(conference, fitness = -1):
    
    if fitness != -1: print("FITNESS", fitness, '\n')
    
    for presentation in conference:
        print(presentation['paper'], " --> room:", presentation['room'], "; day:", presentation['day'], "; time:", presentation['time'])
