import matplotlib.pyplot as plt
import pandas as pd

sales_data = pd.read_csv("./resources/sales_data.csv")
""""
df = pd.read_csv("../results/sales_data.csv", header=None, nrows=1)
df.iloc[0][1:7]
"""""
# 1 Read Total profit of all months and show it using a line plot
profit_list = sales_data['total_profit'].values
months = sales_data['month_number'].values
plt. figure()
plt. plot(months, profit_list, label='Month - wise Profit data of last year')
plt. xlabel('Month number')
plt. ylabel('Profit [$]')
plt. xticks(months)
plt. title('Company profit per month')
plt. yticks([100e3, 200e3, 300e3, 400e3, 500e3])
plt. show()

# 2 Get Total profit of all months and show line plot with the following Style properties:
plt.figure()
months = sales_data['month_number'].values
plt.plot(months, profit_list, label='Profit data of last year', color='r', marker='o', markerfacecolor='k', linestyle='--', linewidth=3)
plt.ylabel('Profit in dollar')
plt.xlabel('Month Number')
plt.legend(loc='lower right')
plt.title('Company Sales data of last year')
plt. xticks(months)
plt. yticks([100e3, 200e3, 300e3, 400e3, 500e3])
plt.show()

# 3 Read all product sales data and show it using a multiline plot
sales_data = pd.read_csv("./resources/sales_data.csv")
profit_list = sales_data['total_profit'].values
plt.figure()
headers = sales_data.columns.delete(0) # removing column 0 month_number
print(headers)
products = sales_data.iloc[:, 1:7]
print(products)
months = sales_data['month_number'].values
lines = []
lines = plt.plot(months, products, marker='o', linewidth=3)
plt.xlabel('Month Number ')
plt.ylabel('Sales units in number ')
plt.legend(loc='upper left')
plt.legend(lines, headers)
plt.xticks(months)
plt.yticks([1e3, 2e3, 4e3, 6e3, 8e3, 10e3, 12e3, 15e3, 18e3])
plt.title('Sales data')
plt.show()

'''
profit_list = sales_data['total_profit'].values
months = sales_data['month_number'].values
face_cream_sales_data = sales_data['facecream'].values
face_wash_sales_data = sales_data['facewash'].values
tooth_paste_sales_data = sales_data['toothpaste'].values
bathing_soap_sales_data = sales_data['bathingsoap'].values
shampoo_sales_data = sales_data['shampoo'].values
moisturizer_sales_data = sales_data['moisturizer'].values
plt.figure()
plt.plot(months, face_cream_sales_data, label='Face cream Sales Data', marker='o', linewidth=3)
plt.plot(months, face_wash_sales_data, label='Face wash Sales Data', marker='o', linewidth=3)
plt.plot(months, tooth_paste_sales_data, label='ToothPaste Sales Data', marker='o', linewidth=3)
plt.plot(months, bathing_soap_sales_data, label='Bathing Soap Sales Data ', marker='o', linewidth=3)
plt.plot(months, shampoo_sales_data,  label='Shampoo Sales Data ', marker='o', linewidth=3)
plt.plot(months, moisturizer_sales_data, label=' Moisturizer Sales Data ', marker='o', linewidth=3)
plt.xlabel('Month Number ')
plt.ylabel('Sales units in number ')
plt.legend(loc='upper left')
plt.xticks(months)
plt.yticks([1e3, 2e3, 4e3, 6e3, 8e3, 10e3, 12e3, 15e3, 18e3])
plt.title('Sales data')
plt.show()
'''

#4 Read toothpaste sales data of each month and show it using a scatter plot
plt.figure()
months = sales_data['month_number'].tolist()
toothpaste = sales_data['toothpaste'].values
plt.scatter(months, toothpaste,label ='Tooth paste sales data')
plt.ylabel('toothpaste')
plt.xlabel('months')
plt.legend(loc ='upper left')
plt.title('Tooth paste sales data')
plt.xticks( months )
plt.grid(True , linewidth =0.5 , linestyle ='--')
plt.show()

#5 bathingsoap

bathingsoap = sales_data['bathingsoap'].tolist()
plt.bar(months, toothpaste)
plt.ylabel('bathingsoap')
plt.xlabel('months')
plt.xticks ( months )
plt.grid (True , linewidth =0.5 , linestyle ="--")
plt.title ('Bathing soap sales data')
plt.savefig('barhinhsoap_months.png', dpi=150)
plt.show()

# 6 Read the total profit of each month and show it using the histogram to see most common profit ranges
plt.figure()
profit_range = [150e3 , 170e3 , 200e3 , 225e3 , 250e3 , 300e3 , 350e3]
plt.hist( profit_list, profit_range, label='Profit data')
plt. xlabel ('profit range [$]')
plt. ylabel ('Actual Profit [$]')
plt. legend (loc ='upper left')
plt. xticks (profit_range)
plt. title ('Profit data')
plt.show()


# 7 Read Bathing soap facewash of all months and display it using the Subplot
plt.figure()
facewash = sales_data['facewash'].values
bathingsoap = sales_data['bathingsoap'].values
f, axs = plt. subplots (2 , 1 , sharex = True )
axs[0].plot(months, bathingsoap , label ='Bathing soap Sales Data ',color ='k', marker ='o', linewidth =3)
axs[0].set_title('Sales data of a Bathing soap ')
axs[0].grid(True, linewidth =0.5 , linestyle ='--')
axs[0].legend()
axs[1].plot(months , facewash , label ='Face Wash Sales Data ', color ='r', marker ='o', linewidth =3)
axs[1].set_title('Sales data of a face wash ')
axs[1].grid(True , linewidth =0.5 , linestyle ='--')
axs[1].legend ()
plt.xticks ( months )
plt.xlabel ('Month Number ')
plt.ylabel ('Sales units in number ')
plt.show ()

# our solution
plt.figure()
facewash = sales_data['facewash'].values
bathingsoap = sales_data['bathingsoap'].values
plt.subplot(2,1,1)
plt.plot(bathingsoap, label="bathingsoap", color='y')
plt.legend()
plt.subplot(2,1,2)
plt.plot(facewash, label="facewash", color='r')
plt.legend()
plt.show()
