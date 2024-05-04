import csv
import pandas as pd

from generate_icalendars import convert_csv_to_ics
from marathon_urls import url_dict  # Add this line
from tabulate import tabulate

csv_filename = 'majors.csv'
ics_filename = 'marathon_majors.ics'


def format_as_markdown_table(df):
    df = df.drop(columns='Year')
    df.insert(1, 'Race URL', df["Race"].map(url_dict))  # insert URLs
    md_table = tabulate(df, headers='keys', showindex=False, tablefmt='pipe')
    return md_table


def convert_csv_to_md(csv_filename, md_filename):
    with open(csv_filename, 'r', encoding='utf-8') as csv_file:
        csv_data = list(csv.reader(csv_file))
    # Prepare separate data for 2024 and 2025
    data_2024 = [x for x in csv_data if x[0] == '2024']
    data_2025 = [x for x in csv_data if x[0] == '2025']
    # Create pandas DataFrame
    df_2024 = pd.DataFrame(data_2024, columns=csv_data[0])
    df_2025 = pd.DataFrame(data_2025, columns=csv_data[0])
    # Create markdown tables
    md_table_2024 = format_as_markdown_table(df_2024)
    md_table_2025 = format_as_markdown_table(df_2025)
    # Write to md file
    with open(md_filename, 'w', encoding='utf-8') as md_file:
        md_file.write('[📅 Calendar File](' + ics_filename + ')  \n')
        md_file.write('♻️ Subscribe to this link: https://raw.githubusercontent.com/zyberzebra/MarathonMajors/master/marathon_majors.ics\n')
        md_file.write('## Marathon Majors 2025\n')
        md_file.write(md_table_2025)
        md_file.write('\n\n')
        md_file.write('## Marathon Majors 2024\n')
        md_file.write(md_table_2024)


# Call the function provide csv and markdown file

convert_csv_to_ics(csv_filename, ics_filename)
convert_csv_to_md(csv_filename, 'README.MD')
