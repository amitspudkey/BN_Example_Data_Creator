import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import sqlite3
import os

def main():
    print()

    # Hide Tkinter GUI
    Tk().withdraw()

    # Ask for delimination
    delimination = input("Enter Deliminator: ")

    # Find input file
    file_in_person = select_file_in("Select Person Table")

    # Open input csv using the unknown encoder function
    data_person = open_unknown_csv(file_in_person, delimination)

    # Find input file
    file_in_personna = select_file_in("Select Personna Table")

    # Open input csv using the unknown encoder function
    data_personna = open_unknown_csv(file_in_personna, delimination)

    # Find input file
    file_in_product = select_file_in("Select Product Table")

    # Open input csv using the unknown encoder function
    data_product = open_unknown_csv(file_in_product, delimination)

    # Define Database
    database = 'database.db'

    # Delete Old Database
    delete_file(database)
    delete_file(database + "-journal")

    # Create Connenction to Database
    print('Connecting to ' + database + '...')
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    print('Connected to ' + database + '!')

    data_person.to_sql('person',conn)

    cur.execute(
        """
            select 
                *
            from 
                person;
        """
    )



def delete_file(name):
    # Deletes a given file. If the file cannot be deleted, displays message.
    print('Deleting ' + name + '...')
    try:
        os.remove(name)
        print(name + ' deleted!')
    except OSError:
        pass
        print(name + " isn't present or cannot be deleted!")
    print('')


def open_unknown_csv(file_in, delimination):
    encode_index = 0
    encoders = ['utf_8', 'latin1', 'utf_16',
                'ascii', 'big5', 'big5hkscs', 'cp037', 'cp424',
                'cp437', 'cp500', 'cp720', 'cp737', 'cp775',
                'cp850', 'cp852', 'cp855', 'cp856', 'cp857',
                'cp858', 'cp860', 'cp861', 'cp862', 'cp863',
                'cp864', 'cp865', 'cp866', 'cp869', 'cp874',
                'cp875', 'cp932', 'cp949', 'cp950', 'cp1006',
                'cp1026', 'cp1140', 'cp1250', 'cp1251', 'cp1252',
                'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257',
                'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr',
                'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp',
                'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext',
                'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4',
                'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9',
                'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15',
                'iso8859_16', 'johab', 'koi8_r', 'koi8_u', 'mac_cyrillic',
                'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish',
                'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32',
                'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le',
                'utf_7', 'utf_8', 'utf_8_sig']

    data = open_file(file_in, encoders[encode_index], delimination)
    while data is str:
        if encode_index < len(encoders) - 1:
            encode_index = encode_index + 1
            data = open_file(file_in, encoders[encode_index], delimination)
        else:
            print("Can't find appropriate encoder")
            exit()

    return data

def open_file(file_in, encoder, delimination):
    try:
        data = pd.read_csv(file_in, low_memory=False, encoding=encoder, delimiter=delimination)
        print("Opened file using encoder: " + encoder)

    except UnicodeDecodeError:
        print("Encoder Error for: " + encoder)
        return "Encode Error"
    return data


def select_file_in(note):
    file_in = askopenfilename(initialdir="../", title=note,
                              filetypes=(("Comma Separated Values", "*.csv"), ("all files", "*.*")))
    if not file_in:
        input("Program Terminated. Press Enter to continue...")
        exit()

    return file_in


def select_file_out(file_in):
    file_out = asksaveasfilename(initialdir=file_in, title="Select file",
                                 filetypes=(("Comma Separated Values", "*.csv"), ("all files", "*.*")))
    if not file_out:
        input("Program Terminated. Press Enter to continue...")
        exit()

    # Create an empty output file
    open(file_out, 'a').close()

    return file_out


if __name__ == '__main__':
    main()