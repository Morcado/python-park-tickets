import glob
import json
import os
import pandas

def read_shift_control(base_path):
    file = glob.glob(os.path.join(base_path, r'shiftControl\controlShift.json'))[0]
    
    with open(file, 'r') as f:
        try:
            data = json.load(f)
            df = pandas.json_normalize(data, record_path=['listShifts'])
            df = df[['Id_Shift', 'InitialDate', 'FinalDate', 'Status', 'Id_PeopleOpening', 'InitialCash', 'InternalControl', 'Diference', 'Id_PeopleClosed', 'FinalCash', 'TotalInvoices', 'TotalTaxes', 'TotalwhitTaxes', 'TotalwhitOutTaxes']]
            
            writer =  pandas.ExcelWriter(os.path.join(base_path, f"shift_control.xlsx"))
            df.to_excel(writer, sheet_name='Control', index=False)
            
            for shift_id in df['Id_Shift']:
                if shift_id == 1: # Skip invalid shift IDs
                    continue
                shift_summary = read_shift_sumary(base_path, shift_id)
                shift_tickets = read_shift_tickets(base_path, shift_id)
    
                shift_summary.to_excel(writer, sheet_name=f'Summary-{shift_id}')
                shift_tickets.to_excel(writer, sheet_name=f'Tickets-{shift_id}', index=False)
                
                print(f"Details for shift {shift_id} saved to shift_{shift_id}_details.xlsx")
            
            writer.close()
            
            
            print(f"DataFrame saved to shift_control.csv")
        except FileNotFoundError:
            print(f"Error: File not found at {base_path}")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")

def read_shift_sumary(base_path, shift_id='920'):
    file = glob.glob(os.path.join(base_path, rf'shiftControl\shiftResults\{shift_id}\shiftResult-{shift_id}.json'))
    print( len(file))
    
    if (len(file)==0):
        return pandas.DataFrame()
    
    if (os.path.isfile(file[0])==False):
        return pandas.DataFrame()
    
    with open(file[0], 'r') as f:
        try:
            data = json.load(f)
            df = pandas.json_normalize(data)
            df = df[['InitialDate', 'FinalDate', 'InitInvoice', 'FinishInvoice', 'Id_PeopleOpening', 'InitialCash', 'InternalControl', 'Diference', 'Id_PeopleClosed', 'FinalCash', 'TotalTaxes', 'TotalwhitTaxes', 'TotalwhitOutTaxes', 'LastInsert']]
            
            df = df.T
            return df
            #df.to_csv(os.path.join(base_path, "daily_summary.csv"))
            #print(f"DataFrame saved to daily_summary.csv")
            
        except FileNotFoundError:
            print(f"Error: File not found at {base_path}")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")

def read_shift_tickets(base_path, shift_id='920'):
    
    json_files = glob.glob(os.path.join(base_path, rf'shiftControl\shiftResults\{shift_id}\Fer*.json'))
    dfs = []
    
    for file in json_files:
        with open(file, 'r') as f:
            try:
                data = json.load(f)
                df = pandas.json_normalize(data)
                df = df[['IdInvoice', 'Id_Transaction', 'InvoiceDate', 'TotalWithoutTaxes', 'TotalTaxes', 'Subtotal', 'Total', 'PaymentDetails.change', 'Reference.Id_TransactionParent']]
                dfs.append(df)

            except FileNotFoundError:
                print(f"Error: File not found at {base_path}")
            except json.JSONDecodeError:
                print("Error: Invalid JSON format")
                
    if dfs: # Check if any dataframes were successfully loaded
        combined_df = pandas.concat(dfs, ignore_index=True)
        return combined_df
        #combined_df.to_csv(os.path.join(base_path, "daily_tickets.csv"), index=False)
        print(f"DataFrame saved to daily_tickets.csv")
    else:
        combined_df = pandas.DataFrame() # Create an empty DataFrame if no files were rea
        return combined_df


base_path = r"C:\Users\oscar.gonzalez\Desktop\python-park-tickets\dataBilling"  # Replace with your JSON file path
#read_shift_tickets(base_path, 920)
#read_shift_sumary(base_path, 920)
read_shift_control(base_path)