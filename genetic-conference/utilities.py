import openpyxl as sheets

"""
"""
def export_to_spreadsheet(wb_path, population):
    wb = sheets.Workbook()
    ws = wb.active
    wb.save(wb_path)


def print_conference(conference):
    for presentation in conference:
        print(presentation)
