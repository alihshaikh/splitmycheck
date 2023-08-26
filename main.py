def main():
    customerList = []
    print("Enter the names of the people you would like to split the check with. Please enter *DONE* when done adding people to check")


    while True:
        name = input("Enter a name (or 'exit' to quit): ")

        if name == 'exit':
            break
        
        customerList.append([name, 0])
    
    print("For each participant with the check, enter the itemized cost of each item they have ordered.")

    for i in range(len(customerList)):
        while True:
            itemPrice = input("Enter price for item which " + customerList[i][0] + " has bought (or 'exit' when done entering items): ")

            if itemPrice == 'exit':
                break
            customerList[i][1] += itemPrice

    tipTotal = input("Enter the tip total with the bill: ")
       
    taxRate = input("Enter the tax rate in decimal for the bill (i.e if tax rate is 10.25%, input 0.1025): ")

    totalCostOfBill = 0
    for i in range(len(customerList)):
        totalCostOfBill += customerList[i][1]

    for i in range(len(customerList)):
        originalCost = customerList[i][1]
        percentageOfTipOwed = (totalCostOfBill - originalCost) / totalCostOfBill * 100
        addedTax = customerList[i][1] * taxRate
        addedTipCost = percentageOfTipOwed * tipTotal
        customerList[i][1] = customerList[i][1] + addedTax + addedTipCost

    for i in range(len(customerList)):
        print("{} owes ${:.2f}".format(customerList[i][0], customerList[i][1]))







    

if __name__ == "__main__":
    main()

