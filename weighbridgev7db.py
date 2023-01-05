
import tkinter as tk
import datetime
import sqlite3

# Create window object
window = tk.Tk()
window.title('Weighbridge System')
window.geometry('1024x450')

# Create database connection
conn = sqlite3.connect('weighbridge.db')
cursor = conn.cursor()

# Create table if it doesn't exist
try:
    cursor.execute("CREATE TABLE weighbridge (vehicle_no VARCHAR, weigh_slip_no INTEGER, \
                    inbound_outbound TEXT, voucher INTEGER, ledger TEXT, stock_items TEXT, \
                    first_weight REAL, second_weight REAL, net_weight REAL, date TEXT, time TEXT)")
except:
    pass

# Create labels
lbl_vehicle_no = tk.Label(window, text='Vehicle No.')
lbl_vehicle_no.place(x=20, y=20)

lbl_weigh_slip_no = tk.Label(window, text='Weigh Slip No.')
lbl_weigh_slip_no.place(x=440, y=20)

lbl_inbound_outbound = tk.Label(window, text='Inbound/Outbound')
lbl_inbound_outbound.place(x=20, y=60)

lbl_voucher = tk.Label(window, text='Voucher')
lbl_voucher.place(x=440, y=60)

lbl_ledger = tk.Label(window, text='Ledger')
lbl_ledger.place(x=720, y=20)

lbl_stock_items = tk.Label(window, text='Stock Items')
lbl_stock_items.place(x=20, y=100)

lbl_first_weight = tk.Label(window, text='First Weight')
lbl_first_weight.place(x=20, y=160)

lbl_second_weight = tk.Label(window, text='Second Weight')
lbl_second_weight.place(x=440, y=160)

lbl_net_weight = tk.Label(window, text='Net Weight')
lbl_net_weight.place(x=700, y=160)

lbl_date = tk.Label(window, text='Date')
lbl_date.place(x=20, y=200)

lbl_time = tk.Label(window, text='Time')
lbl_time.place(x=20, y=240)

# Create entry fields
txt_vehicle_no = tk.Entry(window, width=20)
txt_vehicle_no.place(x=150, y=20)

txt_weigh_slip_no = tk.Entry(window, width=20)
txt_weigh_slip_no.place(x=560, y=20)

# Create dropdown fields
inbound_outbound_options = ['Inbound', 'Outbound']
opt_inbound_outbound = tk.StringVar(window)
opt_inbound_outbound.set(inbound_outbound_options[0])

dropdown_inbound_outbound = tk.OptionMenu(window, opt_inbound_outbound, *inbound_outbound_options)
dropdown_inbound_outbound.place(x=150, y=60)

voucher_options = ['Delivery Note', 'Voucher 2', 'Voucher 3']
opt_voucher = tk.StringVar(window)
opt_voucher.set(voucher_options[0])

dropdown_voucher = tk.OptionMenu(window, opt_voucher, *voucher_options)
dropdown_voucher.place(x=560, y=60)

ledger_options = ['Sundry Debtors', 'Ledger 2', 'Ledger 3']
opt_ledger = tk.StringVar(window)
opt_ledger.set(ledger_options[0])

dropdown_ledger = tk.OptionMenu(window, opt_ledger, *ledger_options)
dropdown_ledger.place(x=790, y=20)

stock_items_options = ['Item 1', 'Item 2', 'Item 3']
opt_stock_items = tk.StringVar(window)
opt_stock_items.set(stock_items_options[0])

dropdown_stock_items = tk.OptionMenu(window, opt_stock_items, *stock_items_options)
dropdown_stock_items.place(x=150, y=100)

txt_first_weight = tk.Entry(window, width=20)
txt_first_weight.place(x=150, y=160)

txt_second_weight = tk.Entry(window, width=20)
txt_second_weight.place(x=560, y=160)

txt_net_weight = tk.Entry(window, width=20)
txt_net_weight.place(x=790, y=160)

txt_date = tk.Entry(window, width=20)
txt_date.place(x=150, y=200)

txt_time = tk.Entry(window, width=20)
txt_time.place(x=150, y=240)

# Create buttons
btn_reset = tk.Button(window, text='Reset', command=lambda: reset_window())
btn_reset.place(x=520, y=260)

btn_save = tk.Button(window, text='Save', command=lambda: save_data())
btn_save.place(x=420, y=260)

# Create functions
def reset_window():
    txt_vehicle_no.delete(0, 'end')
    txt_weigh_slip_no.delete(0, 'end')
    opt_inbound_outbound.set(inbound_outbound_options[0])
    opt_voucher.set(voucher_options[0])
    opt_ledger.set(ledger_options[0])
    opt_stock_items.set(stock_items_options[0])
    txt_first_weight.delete(0, 'end')
    txt_second_weight.delete(0, 'end')
    txt_net_weight.delete(0, 'end')
    txt_date.delete(0, 'end')
    txt_time.delete(0, 'end')

def save_data():
    # Validate data
    if txt_vehicle_no.get() == '' or txt_weigh_slip_no.get() == '' or \
        txt_first_weight.get() == '' or txt_second_weight.get() == '' or \
        txt_net_weight.get() == '' or txt_date.get() == '' or txt_time.get() == '':
        tk.messagebox.showinfo('Error', 'Please complete all fields!')
        return
    
    # Calculate net weight
    net_weight = round(float(txt_second_weight.get()) - float(txt_first_weight.get()), 2)
    txt_net_weight.delete(0, 'end')
    txt_net_weight.insert(0, str(net_weight))

    # Get current date and time
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H:%M:%S')
    txt_date.delete(0, 'end')
    txt_date.insert(0, date)
    txt_time.delete(0, 'end')
    txt_time.insert(0, time)

    # Insert data into database
    cursor.execute("INSERT INTO weighbridge (vehicle_no, weigh_slip_no, inbound_outbound, \
                    voucher, ledger, stock_items, first_weight, second_weight, net_weight, \
                    date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                    (txt_vehicle_no.get(), txt_weigh_slip_no.get(), opt_inbound_outbound.get(), \
                     opt_voucher.get(), opt_ledger.get(), opt_stock_items.get(), \
                     txt_first_weight.get(), txt_second_weight.get(), txt_net_weight.get(), \
                     txt_date.get(), txt_time.get()))
    conn.commit()
    tk.messagebox.showinfo('Success', 'Weighbridge data saved successfully!')

window.mainloop()