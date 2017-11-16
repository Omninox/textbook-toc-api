# upload textbook to DB
# for best results, use Python 2
from pymongo import MongoClient
import settings
import csv

client = MongoClient(settings.MONGO_URI)

db = client['textbookTOCs']
collection = db.textbooks

class TOC:
    def __init__(self, file):
        self.raw_data = []
        # with open(file, 'rU') as csvfile:
            # Toc_reader=csvfile.read()
        toc_reader = csv.reader(file, delimiter=",")
        for row in toc_reader:
            self.raw_data.append(row)

    def populate(self):
        self.chapters = {}
        self.sections = {}
        self.units = {}
        active_unit = False
        # Set super_category to top-level structure
        if 'Unit' in self.raw_data[0][0]:
            self.super_category = 'Units'
        else:
            self.super_category = 'Chapters'
        # Start looping through each chapter / section
        for row_index in range(1, len(self.raw_data)):
            row = self.raw_data[row_index]
            try:
                # Read chapter number
                chapter_number = int(row[0])
            except:
                # Add unit to self.units
                active_unit = row[0]
                self.units[active_unit] = {
                    'number': active_unit,
                    'title': row[2],
                    'chapters': []
                }
                continue
            # add chapter to collection
            if chapter_number in self.chapters:
                # Chapter already exists
                # Add new section
                section_id = row[1]
                section_title = row[2]
                # Keep a reference of section id's in chapters
                self.chapters[chapter_number]['sections'].append(section_id)
                # Create a separate self.sections property
                # This keeps the structure flat
                self.sections[section_id] = {
                    'number': section_id,
                    'title': section_title
                }
            else:
                # Chapter does not exist
                # Create new chapter
                self.chapters[chapter_number] = {
                    'number': chapter_number,
                    'title': row[2],
                    'sections': []
                }
                if active_unit != False:
                    # Add unit name to chapter
                    self.chapters[chapter_number]['unit'] = active_unit
                    # Add chapter number to unit's list of chapters
                    self.units[active_unit]['chapters'].append(chapter_number)



# ____EXAMPLES____
# statistics = TOC('stats.csv')
# statistics.populate()
# print("-------------First printing units-----------")
# print(statistics.units)
# print("-------------Now printing chapters-----------")
# print(statistics.chapters)
# print("-------------Finally, sections...-----------")
# print(statistics.sections)

# zumdahl = TOC('Chemistry_Zumdahl.csv')
# zumdahl.populate()
# print("-------------First printing units-----------")
# print(zumdahl.units)
# print("-------------Now printing chapters-----------")
# print(zumdahl.chapters)
# print("-------------Finally, sections...-----------")
# print(zumdahl.sections)
