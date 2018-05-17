from macros import *
import openpyxl as sheets


"""
"""
def export_to_spreadsheet(wb_path, individual):
    wb = sheets.load_workbook('template.xlsx')
    ws = wb.active

    # Place day and room headers.
    for room_i in range(NUMBER_OF_ROOMS):
        for day_i in range(3):
            c = SHEET_COL_START + day_i * NUMBER_OF_ROOMS + room_i
            ws.cell(row=3, column=c, value=f"Room #{room_i + 1}")

    for talk in individual:
        c = SHEET_COL_START + (talk['day'] - 1) * NUMBER_OF_ROOMS + talk['room']
        r = SHEET_ROW_START + talk['time']

        ws.cell(row=r , column=c , value=talk['paper'].id)

    wb.save('results.xlsx')

def print_conference(conference):
    for presentation in conference:
        print(presentation)
