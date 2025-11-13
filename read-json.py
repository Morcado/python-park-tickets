import glob
import json
import os
import pandas

def read_shift_control(base_path, current_working_dir):
    rename_map = {
        'Id_Shift': 'ID Turno',
        'InitialDate': 'Fecha Inicio',
        'FinalDate': 'Fecha Fin',
        'Status': 'Estado',
        'Id_PeopleOpening': 'ID Persona Apertura',
        'InitialCash': 'Efectivo Inicial',
        'InternalControl': 'Control Interno',
        'Diference': 'Diferencia',
        'Id_PeopleClosed': 'ID Persona Cierre',
        'FinalCash': 'Efectivo Final',
        'TotalInvoices': 'Total Facturas',
        'TotalTaxes': 'Total Impuestos',
        'TotalwhitTaxes': 'Total con Impuestos',
        'TotalwhitOutTaxes': 'Total sin Impuestos'
    }
    
    file = glob.glob(os.path.join(base_path, r'shiftControl\controlShift.json'))[0]
    
    with open(file, 'r') as f:
        try:
            data = json.load(f)
            df = pandas.json_normalize(data, record_path=['listShifts'])
            df = df[['Id_Shift', 'InitialDate', 'FinalDate', 'Status', 'Id_PeopleOpening', 'InitialCash', 'InternalControl', 'Diference', 'Id_PeopleClosed', 'FinalCash', 'TotalInvoices', 'TotalTaxes', 'TotalwhitTaxes', 'TotalwhitOutTaxes']]
            df.rename(columns=rename_map, inplace=True)
            
            writer =  pandas.ExcelWriter(os.path.join(current_working_dir, f"shift_control.xlsx"), engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Control', index=False)
            
            for column in df.columns:
                column_length = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets['Control'].set_column(col_idx, col_idx, column_length)
            
            
            for shift_id in df['ID Turno']:
                if shift_id == None or shift_id == 1:
                    continue
                shift_summary = read_shift_sumary(base_path, shift_id)
                shift_tickets = read_shift_tickets(base_path, shift_id)
                
                shift_summary.to_excel(writer, sheet_name=f'Turno {shift_id}')
                
                    
                for col in shift_summary.columns:
                    column_length = max(shift_summary[col].astype(str).map(len).max(), len(str(col)))
                    col_idx = shift_summary.columns.get_loc(col)
                    writer.sheets[f'Turno {shift_id}'].set_column(col_idx, col_idx, column_length)
                    
                shift_tickets.to_excel(writer, sheet_name=f'Facturas del turno {shift_id}', index=False)
                
                for col in shift_tickets.columns:
                    column_length = max(shift_tickets[col].astype(str).map(len).max(), len(col))
                    col_idx = shift_tickets.columns.get_loc(col)
                    writer.sheets[f'Facturas del turno {shift_id}'].set_column(col_idx, col_idx, column_length)
                
            writer.close()
            
            
            print(f"Control de turnos exportado exitosamente a {current_working_dir}\\shift_control.xlsx")
        except FileNotFoundError:
            print(f"Error: archivo no encontrado en {base_path}")
        except json.JSONDecodeError:
            print("Error: Formato JSON invalido")

def read_shift_sumary(base_path, shift_id):
    rename_map = {
        'InitialDate': 'Fecha Inicio',
        'FinalDate': 'Fecha Fin',
        'InitInvoice': 'Factura Inicial',
        'FinishInvoice': 'Factura Final',
        'Id_PeopleOpening': 'ID Persona Apertura',
        'InitialCash': 'Efectivo Inicial',
        'InternalControl': 'Control Interno',
        'Diference': 'Diferencia',
        'Id_PeopleClosed': 'ID Persona Cierre',
        'FinalCash': 'Efectivo Final',
        'TotalTaxes': 'Total Impuestos',
        'TotalwhitTaxes': 'Total con Impuestos',
        'TotalwhitOutTaxes': 'Total sin Impuestos',
        'LastInsert': 'Ultima Insercion'
    }

    file = glob.glob(os.path.join(base_path, rf'shiftControl\shiftResults\{shift_id}\shiftResult-{shift_id}.json'))
    
    if (len(file)==0):
        return pandas.DataFrame()
    
    if (os.path.isfile(file[0])==False):
        return pandas.DataFrame()
    
    with open(file[0], 'r') as f:
        try:
            data = json.load(f)
            df = pandas.json_normalize(data)
            df = df[['InitialDate', 'FinalDate', 'InitInvoice', 'FinishInvoice', 'Id_PeopleOpening', 'InitialCash', 'InternalControl', 'Diference', 'Id_PeopleClosed', 'FinalCash', 'TotalTaxes', 'TotalwhitTaxes', 'TotalwhitOutTaxes', 'LastInsert']]
            df.rename(columns=rename_map, inplace=True)
            
            df = df.T
            print(f"Se han leido los datos del resumen del turno {shift_id}")
            return df
            
        except FileNotFoundError:
            print(f"Error: no se encontro el archivo en {base_path}")
        except json.JSONDecodeError:
            print("Error: Formato JSON invalido")

def read_shift_tickets(base_path, shift_id):
    rename_map = {
        'IdInvoice': 'ID Factura',
        'Id_Transaction': 'ID Transaccion',
        'InvoiceDate': 'Fecha Factura',
        'TotalWithoutTaxes': 'Total sin Impuestos',
        'TotalTaxes': 'Total Impuestos',
        'Subtotal': 'Subtotal',
        'Total': 'Total',
        'PaymentDetails.change': 'Cambio',
        'Reference.Id_TransactionParent': 'ID Transaccion Padre'
    }
    
    json_files = glob.glob(os.path.join(base_path, rf'shiftControl\shiftResults\{shift_id}\Fer*.json'))
    dfs = []
    
    for file in json_files:
        with open(file, 'r') as f:
            try:
                data = json.load(f)
                df = pandas.json_normalize(data)
                df = df[['IdInvoice', 'Id_Transaction', 'InvoiceDate', 'TotalWithoutTaxes', 'TotalTaxes', 'Subtotal', 'Total', 'PaymentDetails.change', 'Reference.Id_TransactionParent']]
                df.rename(columns=rename_map, inplace=True)
                dfs.append(df)

            except FileNotFoundError:
                print(f"Error: File not found at {base_path}")
            except json.JSONDecodeError:
                print("Error: Invalid JSON format")
                
    if dfs:
        combined_df = pandas.concat(dfs, ignore_index=True)
        print(f"Se calcularon {len(combined_df)} tickets para el turno {shift_id}")
        return combined_df
    else:
        combined_df = pandas.DataFrame()
        print(f"No se encontraron tickets para el turno {shift_id}")
        return combined_df


if __name__ == "__main__":
    current_working_dir = os.getcwd()

    base_path = open("./ticket-dir.txt", "r").read().strip()
    if (not os.path.exists(base_path)):
        print("El directorio no existe. Verifique la ruta e intente de nuevo.")
        exit(1)
        
    read_shift_control(base_path, current_working_dir)