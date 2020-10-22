import matplotlib.pyplot as plt, pandas as pd

sales_data = pd.read_csv("../results/sales_data.csv")
""""
df = pd.read_csv("../results/sales_data.csv", header=None, nrows=1)
df.iloc[0][1:7]
"""""
# Read Total profit of all months and show it using a line plot
total_profit = sales_data['total_profit']
print(total_profit)
plt.figure()
plt.plot(total_profit)

# Get Total profit of all months and show line plot with the following Style properties:
plt.figure()
plt.ylabel('amount')
plt.xlabel('months')
plt.plot(total_profit, label='Profit data of last year', color='r', marker='o', markerfacecolor='k', linestyle='-', linewidth=3)
plt.legend()
plt.show()

# Read all product sales data and show it using a multiline plot
print()
headers = sales_data.columns
print(headers)
print()
products = sales_data.iloc[:, 1:7]
print(products)

lines = []
lines = plt.plot(products)
plt.legend(lines, headers)
plt.show()

#Read toothpaste sales data of each month and show it using a scatter plot
months = sales_data['month_number']
toothpaste = sales_data['toothpaste']
plt.scatter(months, toothpaste)
plt.ylabel('toothpaste'
           '')
plt.xlabel('months')
plt.show()


#bathingsoap

bathingsoap = sales_data['bathingsoap']
plt.bar(months, toothpaste)
plt.ylabel('bathingsoap')
plt.xlabel('months')
plt.savefig('barhinhsoap_months.png')
plt.show()

#Read the total profit of each month and show it using the histogram to see most common profit ranges
plt.figure()
plt.hist( total_profit)
plt.show()


# . Read Bathing soap facewash of all months and display it using the Subplot
plt.figure()
facewash = sales_data['facewash']

plt.subplot(2,1,1)
plt.plot(bathingsoap, label="bathingsoap", color='y')
plt.legend()
plt.subplot(2,1,2)
plt.plot(facewash, label="facewash", color='r')
plt.legend()
plt.show()
