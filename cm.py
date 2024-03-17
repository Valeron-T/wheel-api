import json
import re
from pymongo import MongoClient
import tabula
import pandas as pd
from app import mongo

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def format_df(df):
    # Initialize variables
    transactions = []
    current_transaction = {}

    # Iterate over DataFrame rows
    for index, row in df.iterrows():
        if pd.notna(row['Date']):
            # If the current row has a date, add the current transaction to the list and start a new transaction
            if current_transaction:
                transactions.append(current_transaction)
                current_transaction = {}
            current_transaction = row.to_dict()
        elif current_transaction:
            # Append data to the current transaction if it exists and the 'Date' column is NaN
            for col in df.columns:
                if pd.notna(row[col]):
                    current_transaction[col] = str(current_transaction[col]) + str(row[col])

    # Append the last transaction to the list
    if current_transaction:
        transactions.append(current_transaction)

    # Convert the list of transactions to a DataFrame
    result_df = pd.DataFrame(transactions)

    # print(result_df)

    return result_df


def categorise(text):
    category = 'other'
    text = text.lower()
    name_split = text.split(" ")

    with open('categories.json', "r") as file:
        data = json.load(file)

        for key, value in data.items():
            for x in value:
                if str(x).lower() in text:
                    print(x)
                    category = key
                    return category

    matches = 0

    for name in name_split:
        print(name)
        result = mongo.db.names.count_documents(

            {
                "names": name
            }
        )

        matches += int(result)

    print(matches)
    if (matches / len(name_split)) > 0.3:
        category = "People"

    return category


def extract_beneficiary_upi(df):
    # Splitting the 'Narration' column by "-"
    split_data = df.apply(
        lambda x: x['Narration'].split("-") if x['Mode'] == 'UPI' else [None, max(x['Narration'].split("-"), key=len),
                                                                        None], axis=1)

    # Extracting the 2nd item as beneficiary and 3rd item as upi handle
    df['Beneficiary'] = split_data.apply(
        lambda x: max(re.sub(r'\d+', '', str(x[2]).split("@")[0]).split("."), key=len) if x is not None and x[
            1].isdigit() else x[1] if x is not None else None)
    df['UPI_Handle'] = split_data.apply(lambda x: x[2] if x is not None else None)

    return df


def get_payment_type(text):
    payment_pattern = r"(REV-UPI|UPI MANDATE|UPI|IMPS|CHQ|RTGS|TPT|NEFT|INWREMIT|ACH C|ACH|POS|INF|INW|ATW|ATM|IB|CASH|FT)\b"
    payment_match = re.search(payment_pattern, text)
    if payment_match:
        payment_mode = payment_match.group()
        return payment_mode


def concatenate_tables_with_headers(pdf_path):
    # Extract tables from each page
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

    # Extract headers from the first table
    if len(tables) > 0:
        headers = tables[0].columns.tolist()
    else:
        return None

    # Concatenate subsequent tables to the first table after applying headers
    combined_table = tables[0]
    for table in tables[1:]:
        # Check if the number of columns in the table matches the number of headers
        if len(table.columns) == len(headers):
            # Rename columns with headers
            table.columns = headers
            # Concatenate tables
            combined_table = pd.concat([combined_table, table], ignore_index=True)
        else:
            # If number of columns doesn't match, skip this table
            continue

    # Find the index where "STATEMENT SUMMARY :-" is encountered
    index_to_keep = combined_table[combined_table['Narration'] == 'STATEMENT SUMMARY :-'].index

    # If the string is found, slice the DataFrame to keep rows only before that index
    if not index_to_keep.empty:
        combined_table = combined_table.iloc[:index_to_keep[0]]

    # Combines rows where date is not there
    combined_table = format_df(combined_table)

    combined_table['Mode'] = combined_table['Narration'].apply(get_payment_type)

    combined_table = extract_beneficiary_upi(combined_table)

    combined_table['Category'] = combined_table['Beneficiary'].apply(categorise)
    print(combined_table)

    return combined_table


if __name__ == '__main__':
    # a = categorise("Shyam")
    # print(a)
    filename = "pdfs/test5.pdf"
    df = concatenate_tables_with_headers(f"/pdfs/${filename}")
    df.to_excel("test5.xlsx")
    # print(df)
