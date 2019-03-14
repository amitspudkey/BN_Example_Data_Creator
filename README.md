# BN_Example_Data_Creator
A program that will create example data for teaching exercises.

This is a work in progress and a teaching excercise for a colleuge learning Github.

The script uses three csv files, included with the package, to determine how the data is created and what the values are.

    Required Columns
        Customer Input: A table that has all of the individuals used in data creation.
            Customer_ID - ID linking customers across the tables
            Average_Time - The average time someone buys a product
            Stdev_Time - The standard deviation for the purchase time
            num_transactions - The number of transactions that will be created for this person
            num_items_per_trans_avg - The number of items that will be purchased within a transactions
            num_items_per_trans_stdev - The standard deviation of the number of items that were purchased in a transaction
            Personna - The personna for this person. The personna name must match a personna within the Personna Table.
    
    Personna Input: A table that defines the purchasing habits for each person by personna.
        Personna - The personna name
        All other columns - All other columns should be the name of each item and the rolling perpensity for the personna to purchase it.
    
    Product Input: A table linking the price and items
        Item - Item name
        Price - Price of item
        