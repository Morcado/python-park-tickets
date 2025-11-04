import glob
import json
import os
import pandas

def read_daily_sumary(base_path):
    file = glob.glob(os.path.join(base_path, r'shiftControl\shiftResults\920\shiftResult*.json'))[0]
    
    with open(file, 'r') as f:
        try:
            data = json.load(f)
            df = pandas.json_normalize(data)
            df = df[['InitialDate', 'FinalDate', 'InitInvoice', 'FinishInvoice', 'Id_PeopleOpening', 'InitialCash', 'InternalControl', 'Diference', 'Id_PeopleClosed', 'FinalCash', 'TotalTaxes', 'TotalwhitTaxes', 'TotalwhitOutTaxes', 'LastInsert']]
            
            df = df.T
            df.to_csv(os.path.join(base_path, "daily_summary.csv"))
            print(f"DataFrame saved to daily_summary.csv")
            
        except FileNotFoundError:
            print(f"Error: File not found at {base_path}")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")

def read_daily_tickets(base_path):
    
    json_files = glob.glob(os.path.join(base_path, r'shiftControl\shiftResults\920\Fer*.json'))
    dfs = []
    
    for file in json_files:
        with open(file, 'r') as f:
            try:
                data = json.load(f)
                df = pandas.json_normalize(data)
                df = df[['IdInvoice', 'Id_Transaction', 'InvoiceDate', 'TotalWithoutTaxes', 'TotalTaxes', 'Subtotal', 'Total', 'PaymentDetails.change', 'Reference.Id_TransactionParent']]
                # df = [
                #     df['IdInvoice'],
                #     df['Id_Transaction'], 
                #     df['InvoiceDate'], 
                #     df['TotalWithoutTaxes'], 
                #     df['TotalTaxes'], 
                #     df['Subtotal'], 
                #     df['Total'], 
                #     df['PaymentDetails.change'],
                #     df['Reference.Id_TransactionParent']
                # ]
                #df['InvoiceDate'] = df['InvoiceDate'].astype('datetime64[as]')
                dfs.append(df)

            except FileNotFoundError:
                print(f"Error: File not found at {base_path}")
            except json.JSONDecodeError:
                print("Error: Invalid JSON format")
                
    if dfs: # Check if any dataframes were successfully loaded
        combined_df = pandas.concat(dfs, ignore_index=True)
        combined_df.to_csv(os.path.join(base_path, "daily_tickets.csv"), index=False)
        print(f"DataFrame saved to daily_tickets.csv")
    else:
        combined_df = pandas.DataFrame() # Create an empty DataFrame if no files were rea
    # print(dfs)    
    #df.to_csv(os.path.join(base_path, csv_file_name), index=False)
    #print(f"DataFrame saved to {csv_file_name}")

base_path = r"C:\Users\oscar.gonzalez\Desktop\python-park-tickets\dataBilling"  # Replace with your JSON file path
read_daily_tickets(base_path)
read_daily_sumary(base_path)