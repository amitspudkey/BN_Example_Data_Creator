import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from datetime import datetime, timedelta
import numpy as np
import random


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

    # Set output file
    file_out_trans = select_file_out(file_in_person, "Select File Out Transaction Table")
    file_out_person = select_file_out(file_in_person, "Select File Out Person Table")

    # Open input csv using the unknown encoder function
    data_product = open_unknown_csv(file_in_product, delimination)

    # Enter the desired data range
    date_start = date_input("Input start date as YYYY/MM/DD: ")
    while True:
        date_end = date_input("Input end date as YYYY/MM/DD: ")
        if date_end > date_start:
            break
        else:
            print("End date must be greater input date!")

    # Convert dates from str to Date
    date_start = datetime.strptime(date_start, '%Y/%m/%d')
    date_end = datetime.strptime(date_end, '%Y/%m/%d')

    # Calculate number of days between two dates
    num_days = (date_end - date_start).days

    # Get header from personna, used for determining product name
    personna_headers = list(data_personna.columns.values)

    print("Performing Transaction Calculation")

    # Start of Transactions
    date_list = list()
    person_list = list()
    personna_list = list()
    product_list = list()
    time_list = list()
    num_person_ids = len(data_person.index)
    for person_index, person_row in data_person.iterrows():
        # Get customer_personna
        personna_list.append(person_row["Personna"])
        for transaction_index in range(1, person_row["num_transactions"]):
            # Get random date for transacation
            num_days_add = random.randint(1, num_days)
            trans_date = date_start + timedelta(num_days_add)
            for item_index in range(1, int(np.random.normal(person_row["num_items_per_trans_avg"], person_row["num_items_per_trans_stdev"]))):
                # Write person_id to list
                person_list.append(person_row["Customer_ID"])

                # Write date of transactions to list
                date_list.append(trans_date)

                # Get a transaction time
                time_list.append(np.random.normal(person_row["Average_Time"],person_row["Stdev_Time"]))

                # Set initial product found
                initial_product_found = 0

                # Get personna info for person
                personna_hold = data_personna[data_personna["Personna"] == person_row["Personna"]]

                # Get random number for product selection
                product_rand = random.uniform(0, 1)

                # Loop through all of the personna values to find product
                for personna_index, personna_product in enumerate(personna_hold.iteritems()):
                    if personna_index > 0:
                        if initial_product_found == 0:
                            if product_rand < float(personna_product[1]):
                                initial_product_found = 1
                                product_list.append(personna_headers[personna_index])

        # Print current position of transaction creation every 10 people
        if (person_index + 1) % 10 == 0:
            print("Created transaction for person " + str(person_index + 1) + " out of " + str(num_person_ids))

    # Loop through product table to randomly grab the UID for transaction table
    uid_list = list()
    for index, i in enumerate(product_list):
        # Filter items by product
        item_df = data_product[data_product["Item"] == i]

        # Reset index
        item_df = item_df.reset_index()

        # Get number of items
        num_items = len(item_df.index) - 1

        # Get random item index
        item_index = random.randint(0, num_items)

        # Get random item
        uid_list.append(item_df.iloc[item_index, :]["UID"])

        # Print current position of product creation every ten products
        if (index + 1) % 100 == 0:
            print("Created product for transaction " + str(index + 1) + " out of " + str(num_person_ids))

    # Make each list into a Pandas series
    person_series = pd.Series(person_list, name="Customer_ID")
    date_series = pd.Series(date_list, name="Date")
    time_list = pd.Series(time_list, name="Time")
    # product_series = pd.Series(product_list, name="Product")
    uid_series = pd.Series(uid_list, name="UID")

    # Concatenate data series into dataframe
    transaction_df = pd.concat([person_series, date_series, time_list, uid_series], axis=1)

    # Join all product Info
    transaction_df = transaction_df.join(data_product.set_index('UID'), on='UID')

    # Write Transaction Table
    transaction_df.to_csv(file_out_trans, index=False)

    # Drop data creation factors from person table
    person_out = data_person.drop(["Average_Time", "Stdev_Time", "num_transactions", "num_items_per_trans_avg", "num_items_per_trans_stdev", "Personna"], 1)

    # Write person table

    person_out.to_csv(file_out_person, index=False)


def date_input(note):
    while True:
        try:
            date_in = input(note)
            if len(date_in) == 10:
                datetime.strptime(date_in, '%Y/%m/%d')
                break
            else:
                print("Date is invalid!")

        except ValueError:
            print("Input not following YYYY/MM/DD format or is an invalid date!")

    return date_in


class Error(Exception):
    # Base Error
    pass


class ValueTooSmallError(Error):
    # Raise an error if value is too small
    pass


class ValueTooLargeError(Error):
    # Raise an error if value is too large
    pass


def input_int(note, min_value, max_value):
    # Ask for input of only integer
    while True:
        try:
            int_out = int(input(note))
            if int_out < min_value:
                raise ValueTooSmallError
            if int_out > max_value:
                raise ValueTooLargeError
            break
        except ValueError:
            print("Input must be an integer!")
        except ValueTooSmallError:
            print("Value must be greater than " + str(min_value))
        except ValueTooLargeError:
            print("Value must be smaller than " + str(max_value))

    return int_out


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


def select_file_out(file_in, note):
    file_out = asksaveasfilename(initialdir=file_in, title=note,
                                 filetypes=(("Comma Separated Values", "*.csv"), ("all files", "*.*")))
    if not file_out:
        input("Program Terminated. Press Enter to continue...")
        exit()

    # Create an empty output file
    open(file_out, 'a').close()

    return file_out


if __name__ == '__main__':
    main()
