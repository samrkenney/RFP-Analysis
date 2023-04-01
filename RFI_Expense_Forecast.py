"""
The user-input fields in functions get_number, get_vendor, and get_variables are constrained to reflect only relevant vendors and products.
Placeholder names are as follows:
- Vendors: V1, V2, V3, V4
- V1 Devices: Device_A, Device_B
- V1 Instruments: Instrument_A, Instrument_B, Instrument_C
- V2 Devices: Device_C, Device_D
- V2 Instrument: Instrument_D
- V3 Devices: Device_E, Device_F
- V3 Instrument: Instrument_E
- V4 Devices: Device_G, Device_H
- V4 Instrument: Instrument_F

V1 only offers the following bundles: (Device_A, Instrument_A), (Device_B, Instrument_B), (Device_B, Instrument_C)

This program will deliver several outputs based on user-selection of vendors and products:
- total projected cost based on user-input
- several percentile calculations of user-input cost compared to similar procurement scenarios
- four histograms that compare the user-input procurement expense forecast with distributions for different procurement scenarios
- one histogram that compares all vendor proposals

"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import math

ALL_POSSIBLE_OUTCOMES = {'V1': 'v1.csv',
'V2': 'v2.csv',
'V3': 'v3.csv',
'V4': 'v4.csv'} # dictionary to contain one .csv file for each vendor, corresponding to all possible product acquisition scenarios (permutations)

def introduction():
    a = "This program draws on randomized data gathered through a fictitious RFP process for procurement of new capital equipment.\n"
    b = "In this ficticious scenario, four vendors submitted proposals in response to this RFP with different potential solutions to the user's capital equipment needs.\n"
    c = "Vendor proposals detail various pricing and discounting schemes across the two RFP product categories - here labeled as 'device' and 'instrument'. \n"
    d = "The user may forecast the 5-year expense associated with different procurement scenarios: 0-3 device procurements and 0-3 instrument procurements, for a total of 0-6 capital product procurements.\n\n"
    print(a, b, c, d)
    return

def get_vendor():
    """
    Asks user to specify which vendor they would like to forecast procurement expenses.

    Returns:
        (str) vendor - name of the vendor
    """
    try:
        vendor = str(input('Please indicate the name of the vendor you would like this forecast to cover by writing \'V1\', \'V2\', \'V3\', or \'V4\': '))
        while vendor not in ['V1','V2','V3','V4']:
            print('Something went wrong!')
            vendor = str(input('Please indicate the name of the vendor you would like this forecast to cover by writing \'V1\', \'V2\', \'V3\', or \'V4\': '))
    except Exception:
        print('Something unexpected happened! Please try again.')
    return vendor

def get_number(vendor):
    """
    Asks user to specify how many product procurements they would like to forecast.

    Returns:
        (int) num_d - number of devices to be procured
        (int) num_i - number of instruments to be procured
    """
    try:
        num_d = int(input('Please indicate the number of device procurements to be forecasted by writing \'0\', \'1\', \'2\', or \'3\': '))
        while num_d not in [0,1,2,3]:
            print('Something went wrong!')
            num_d = int(input('Please indicate the number of device procurements to be forecasted by writing \'0\', \'1\', \'2\', or \'3\': '))
        if vendor in ['V2', 'V3', 'V4']:
            num_i = int(input('Please indicate the number of instrument procurements to be forecasted by writing \'0\', \'1\', \'2\', or \'3\': '))
            while num_i not in [0,1,2,3]:
                print('Something went wrong!')
                num_i = int(input('Please indicate the number of instrument procurements to be forecasted by writing \'0\', \'1\', \'2\', or \'3\': '))
        else:
            num_i = num_d
    except Exception:
        print('Something unexpected happened! Please try again.')
    return num_d, num_i

def get_variables(vendor, num_d, num_i):
    """
    Asks user to specify which products they would like to procure given responses to previous two questions.

    Returns:
        (str) D1 - name of the first device
        (str) D2 - name of the second device
        (str) D3 - name of the third device
        (str) I1 - name of the first instrument
        (str) I2 - name of the second instrument
        (str) I3 - name of the third instrument
    """
    try:
        if vendor == 'V1':
            if num_i == 3:
                I1 = str(input('Please indicate the name of the first instrument you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                while I1 not in ['Instrument_A', 'Instrument_B', 'Instrument_C']:
                    print('Something went wrong!')
                    I1 = str(input('Please indicate the name of the first instrument you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                if I1 == 'Instrument_A':
                    D1 = 'Device_A'
                else:
                    if I1 == 'Instrument_B':
                        D1 = 'Device_B'
                    else:
                        if I1 == 'Instrument_C':
                            D1 = 'Device_B'
                I2 = str(input('Please indicate the name of the second instrment you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                while I2 not in ['Instrument_A', 'Instrument_B', 'Instrument_C']:
                    print('Something went wrong!')
                    I2 = str(input('Please indicate the name of the second instrument you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                if I2 == 'Instrument_A':
                    D2 = 'Device_A'
                else:
                    if I2 == 'Instrument_B':
                        D2 = 'Device_B'
                    else:
                        if I2 == 'Instrument_C':
                            D2 = 'Device_B'
                I3 = str(input('Please indicate the name of the third instrument you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                while I3 not in ['Instrument_A', 'Instrument_B', 'Instrument_C']:
                    print('Something went wrong!')
                    I3 = str(input('Please indicate the name of the third instrument you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                if I3 == 'Instrument_A':
                    D3 = 'Device_A'
                else:
                    if I3 == 'Instrument_B':
                        D3 = 'Device_B'
                    else:
                        if I3 == 'Instrument_C':
                            D3 = 'Device_B'
            else:
                if num_i == 2:
                    I1 = str(input('Please indicate the name of the first instrument you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                    while I1 not in ['Instrument_A', 'Instrument_B', 'Instrument_C']:
                        print('Something went wrong!')
                        I1 = str(input('Please indicate the name of the first instrument you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                    if I1 == 'Instrument_A':
                        D1 = 'Device_A'
                    else:
                        if I1 == 'Instrument_B':
                            D1 = 'Device_B'
                        else:
                            if I1 == 'Instrument_C':
                                D1 = 'Device_B'
                    I2 = str(input('Please indicate the name of the second instrment you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                    while I2 not in ['Instrument_A', 'Instrument_B', 'Instrument_C']:
                        print('Something went wrong!')
                        I2 = str(input('Please indicate the name of the second instrument you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                    if I2 == 'Instrument_A':
                        D2 = 'Device_A'
                    else:
                        if I2 == 'Instrument_B':
                            D2 = 'Device_B'
                        else:
                            if I2 == 'Instrument_C':
                                D2 = 'Device_B'
                    I3 = str(0)
                    D3 = str(0)
                else:
                    if num_i == 1:
                        I1 = str(input('Please indicate the name of the first instrument you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                        while I1 not in ['Instrument_A', 'Instrument_B', 'Instrument_C']:
                            print('Something went wrong!')
                            I1 = str(input('Please indicate the name of the first instrument you would like to procure by writing \'Instrument_A\', \'Instrument_B\', or \'Instrument_C\': '))
                        if I1 == 'Instrument_A':
                            D1 = 'Device_A'
                        else:
                            if I1 == 'Instrument_B':
                                D1 = 'Device_B'
                            else:
                                if I1 == 'Instrument_C':
                                    D1 = 'Device_B'
                        I2 = str(0)
                        I3 = str(0)
                        D2 = str(0)
                        D3 = str(0)
                    else:
                        I1 = str(0)
                        I2 = str(0)
                        I3 = str(0)
                        D1 = str(0)
                        D2 = str(0)
                        D3 = str(0)
        else:
            if vendor == 'V2':
                if num_d == 3:
                    D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                    while D1 not in ['Device_C', 'Device_D']:
                        print('Something went wrong!')
                        D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                    D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                    while D2 not in ['Device_C', 'Device_D']:
                        print('Something went wrong!')
                        D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                    D3 = str(input('Please indicate the name of the third device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                    while D3 not in ['Device_C', 'Device_D']:
                        print('Something went wrong!')
                        D3 = str(input('Please indicate the name of the third device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                else:
                    if num_d == 2:
                        D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                        while D1 not in ['Device_C', 'Device_D']:
                            print('Something went wrong!')
                            D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                        D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                        while D2 not in ['Device_C', 'Device_D']:
                            print('Something went wrong!')
                            D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                        D3 = str(0)
                    else:
                        if num_d == 1:
                            D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                            while D1 not in ['Device_C', 'Device_D']:
                                print('Something went wrong!')
                                D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_C\' or \'Device_D\': '))
                            D2 = str(0)
                            D3 = str(0)
                        else:
                            D1 = str(0)
                            D2 = str(0)
                            D3 = str(0)
                if num_i == 3:
                    I1 = 'Instrument_D'
                    I2 = 'Instrument_D'
                    I3 = 'Instrument_D'
                else:
                    if num_i == 2:
                        I1 = 'Instrument_D'
                        I2 = 'Instrument_D'
                        I3 = str(0)
                    else:
                        if num_i == 1:
                            I1 = 'Instrument_D'
                            I2 = str(0)
                            I3 = str(0)
                        else:
                            I1 = str(0)
                            I2 = str(0)
                            I3 = str(0)
            else:
                if vendor == 'V3':
                    if num_d == 3:
                        D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                        while D1 not in ['Device_E', 'Device_F']:
                            print('Something went wrong!')
                            D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                        D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                        while D2 not in ['Device_E', 'Device_F']:
                            print('Something went wrong!')
                            D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                        D3 = str(input('Please indicate the name of the third device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                        while D3 not in ['Device_E', 'Device_F']:
                            print('Something went wrong!')
                            D3 = str(input('Please indicate the name of the third device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                    else:
                        if num_d == 2:
                            D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                            while D1 not in ['Device_E', 'Device_F']:
                                print('Something went wrong!')
                                D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                            D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                            while D2 not in ['Device_E', 'Device_F']:
                                print('Something went wrong!')
                                D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                            D3 = str(0)
                        else:
                            if num_d == 1:
                                D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                                while D1 not in ['Device_E', 'Device_F']:
                                    print('Something went wrong!')
                                    D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_E\' or \'Device_F\': '))
                                D2 = str(0)
                                D3 = str(0)
                            else:
                                D1 = str(0)
                                D2 = str(0)
                                D3 = str(0)
                    if num_i == 3:
                        I1 = 'Instrument_E'
                        I2 = 'Instrument_E'
                        I3 = 'Instrument_E'
                    else:
                        if num_i == 2:
                            I1 = 'Instrument_E'
                            I2 = 'Instrument_E'
                            I3 = str(0)
                        else:
                            if num_i == 1:
                                I1 = 'Instrument_E'
                                I2 = str(0)
                                I3 = str(0)
                            else:
                                I1 = str(0)
                                I2 = str(0)
                                I3 = str(0)
                else:
                    if vendor == 'V4':
                        if num_d == 3:
                            D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                            while D1 not in ['Device_G', 'Device_H']:
                                print('Something went wrong!')
                                D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                            D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                            while D2 not in ['Device_G', 'Device_H']:
                                print('Something went wrong!')
                                D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                            D3 = str(input('Please indicate the name of the third device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                            while D3 not in ['Device_G', 'Device_H']:
                                print('Something went wrong!')
                                D3 = str(input('Please indicate the name of the third device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                        else:
                            if num_d == 2:
                                D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                                while D1 not in ['Device_G', 'Device_H']:
                                    print('Something went wrong!')
                                    D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                                D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                                while D2 not in ['Device_G', 'Device_H']:
                                    print('Something went wrong!')
                                    D2 = str(input('Please indicate the name of the second device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                                D3 = str(0)
                            else:
                                if num_d == 1:
                                    D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                                    while D1 not in ['Device_G', 'Device_H']:
                                        print('Something went wrong!')
                                        D1 = str(input('Please indicate the name of the first device you would like to procure by writing \'Device_G\' or \'Device_H\': '))
                                    D2 = str(0)
                                    D3 = str(0)
                                else:
                                    D1 = str(0)
                                    D2 = str(0)
                                    D3 = str(0)
                        if num_i == 3:
                            I1 = 'Instrument_F'
                            I2 = 'Instrument_F'
                            I3 = 'Instrument_F'
                        else:
                            if num_i == 2:
                                I1 = 'Instrument_F'
                                I2 = 'Instrument_F'
                                I3 = str(0)
                            else:
                                if num_i == 1:
                                    I1 = 'Instrument_F'
                                    I2 = str(0)
                                    I3 = str(0)
                                else:
                                    I1 = str(0)
                                    I2 = str(0)
                                    I3 = str(0)
    except Exception:
        print('Something unexpected happened! Please try again.')
    return D1, D2, D3, I1, I2, I3

def user_input_cost(D1, D2, D3, I1, I2, I3, vendor):
    """
    Assigns a forecast-expense value for each product purchase variable and calculates the total forecasted expense.
    Include V1 bundling discounts where applicable 
    """   
    product2cost = {'Device_A': 0,
	'Device_B': 0,
	'Instrument_A': 734056,
	'Instrument_B': 1014836,
    'Instrument_C': 1155106,
    'Device_C': 680128,
	'Device_D': 151903,
	'Instrument_D': 323563,
	'Device_E': 652534,
	'Device_F':416411,
	'Instrument_E': 984185,
	'Device_G': 440423,
	'Device_H': 244368,
    'Instrument_F': 418311,
	'0': 0} # the value for each key corresponds to each product's acquisition cost in USD

    discount1 = {'Instrument_A': product2cost.get('Instrument_A')*.9639,
    'Instrument_B': product2cost.get('Instrument_B')*.95886,
    'Instrument_C': product2cost.get('Instrument_C')*.95555,
    '0': 0} # the discounted values of V1 I2 instruments

    discount2 = {'Instrument_A': product2cost.get('Instrument_A')*.9278,
    'Instrument_B': product2cost.get('Instrument_B')*.91772,
    'Instrument_C': product2cost.get('Instrument_C')*.91109} # the discounted values of V1 I3 instruments

    Cost_D1 = product2cost.get(D1)
    Cost_D2 = product2cost.get(D2)
    Cost_D3 = product2cost.get(D3)
    Cost_I1 = product2cost.get(I1)
    if vendor == 'V1':
        if I3 == '0': # if I3 = 0, then I2 = 0, Instrument_A, Instrument_B, or Instrument_C. The costs corresponding to each value of I2 should be discounted.
            Cost_I2 = discount1.get(I2)
            Cost_I3 = 0
        else: # if vendor = V1 and I3 != 0, then neither I1 = 0, I2 = 0, nor I3 = 0, meaning I2 and I3 acquisition costs are discounted  
            Cost_I2 = discount1.get(I2)
            Cost_I3 = discount2.get(I3)
    else:
        Cost_I2 = product2cost.get(I2)
        Cost_I3 = product2cost.get(I3)
    sum_cost = Cost_D1 + Cost_D2 + Cost_D3 + Cost_I1 + Cost_I2 + Cost_I3
    return sum_cost

def get_dfs(vendor):
    # creates a dataframe of procurement cost-scenarios corresponding to each vendor, which are each contained in a .csv contained in the dictionary ALL_POSSIBLE_OUTCOMES
    df_vendor = pd.read_csv(ALL_POSSIBLE_OUTCOMES[vendor]) #df_vendor selects the .csv that corresponds to user-input value of vendor
    df_v1 = pd.read_csv(ALL_POSSIBLE_OUTCOMES['V1'])
    df_v2 = pd.read_csv(ALL_POSSIBLE_OUTCOMES['V2'])
    df_v3 = pd.read_csv(ALL_POSSIBLE_OUTCOMES['V3'])
    df_v4 = pd.read_csv(ALL_POSSIBLE_OUTCOMES['V3'])
    return df_vendor, df_v1, df_v2, df_v3, df_v4

def get_costs(df_vendor, df_v1, df_v2, df_v3, df_v4):
    """"
    input- dataframes for user-input and all vendor choices
    output- lists of all cost values in USD for each vendor corresponding to each purchase scenario
    """
    cost_vendor = df_vendor['cost'].values.tolist() #list of costs associated all purchase scenarios, given user-input vendor name 
    cost_v1 = df_v1['cost'].values.tolist()
    cost_v2 = df_v2['cost'].values.tolist()
    cost_v3 = df_v3['cost'].values.tolist()
    cost_v4 = df_v4['cost'].values.tolist()
    cost_list = cost_v1 + cost_v2 + cost_v3 + cost_v4
    return cost_vendor, cost_v1, cost_v2, cost_v3, cost_v4, cost_list

def get_codes(df_vendor, df_v1, df_v2, df_v3, df_v4):
    """
    input- dataframes for user-input and all vendor choices
    each dataframe has a column entitled 'i_d' in the format '#1_#2' where #1 = str(# of devices) and #2 = str(# of instruments)
    output- lists of the 'i_d' column for each vendor corresponding to each purchase scenario
    """
    code_vendor = df_vendor['i_d'].values.tolist()
    code_v1 = df_v1['i_d'].values.tolist()
    code_v2 = df_v2['i_d'].values.tolist()
    code_v3 = df_v3['i_d'].values.tolist()
    code_v4 = df_v4['i_d'].values.tolist()
    code_list = code_v1 + code_v2 + code_v3 + code_v4
    return code_vendor, code_list

def filter_cost_list(code_list, cost_list, num_d, num_i): 
    tuple_list_1 = zip(code_list, cost_list) #create a list of tuples with code_list as the first tuple value and cost_list as second tuple value
    filtered_tuple_list = list(filter(lambda x: x[0] == str(num_i) + "_" + str(num_d), tuple_list_1)) # filter the tuple list to match user-input values of num_i and num_d
    filtered_cost_list = [x[1] for x in filtered_tuple_list] #unzip the filtered list of tuples
    return filtered_cost_list

def filter_vendor_cost_list(code_vendor, cost_vendor, num_d, num_i): 
    tuple_list_2 = zip(code_vendor, cost_vendor) #create a list of tuples with code_vendor as the first tuple value and cost_vendor as second tuple value
    filtered_tuple_list_2 = list(filter(lambda x: x[0] == str(num_i) + "_" + str(num_d), tuple_list_2)) # filter the tuple list to match user-input values of num_i and num_d
    filtered_vendor_cost_list = [x[1] for x in filtered_tuple_list_2] #unzip the filtered list of tuples
    return filtered_vendor_cost_list

def data_report(cost_list, sum_cost, cost_vendor, filtered_cost_list, filtered_vendor_cost_list, vendor, num_d, num_i, code_list, code_vendor, D1, D2, D3, I1, I2, I3):
    a = [D1, D2, D3, I1, I2, I3]
    product_list = [x for x in a if x != '0']
    percentile1 = int(stats.percentileofscore(cost_list, sum_cost, kind = 'weak')) #Percentile position of user-input value relative to all possible vendor/product scenarios (permutation) 
    percentile2 = int(stats.percentileofscore(cost_vendor, sum_cost, kind = 'weak')) #Percentile position of user-input value relative to all possible product scenarios (permutation), given vendor selection
    percentile3 = int(stats.percentileofscore(filtered_cost_list, sum_cost, kind = 'weak')) #Percentile position of user-input value relative to all possible vendor/product scenarios (permutation), given num_d and num_i
    percentile4 = int(stats.percentileofscore(filtered_vendor_cost_list, sum_cost, kind = 'weak')) #Percentile position of user-input value relative to all possible product scenarios (permutation), given vendor selection, num_d, and num_i
    data_1 = "1. You have elected to forecast the expense of procuring {} device(s) and {} instrument(s) from {}, as follows: {}"
    data_2 = "2. Out of all four vendors, there exist {} possible product-procurement scenarios.\n   The forecasted expense for procuring {} is {} USD, which is in the {} percentile of all scenarios."
    data_3 = "3. For {}, there exist {} possible product-procurement scenarios.\n   The forecasted expense of {} USD is in the {} percentile of all possible product-procurement scenarios for {}."
    data_4 = "4. {} USD is in the {} percentile of all possible product procurement scenarios across the four vendors, given selection of {} device(s) and {} instrument(s)."
    data_5 = "5. {} USD is in the {} percentile of all possible product procurement scenarios for {}, given selection of {} device(s) and {} instrument(s)."
    print("\n", data_1.format(num_d, num_i, vendor, product_list), "\n")
    print(data_2.format(len(code_list), product_list, sum_cost, percentile1), "\n")
    print(data_3.format(vendor, len(code_vendor), sum_cost, percentile2, vendor), "\n")
    print(data_4.format(sum_cost, percentile3, num_d, num_i), "\n")
    print(data_5.format(sum_cost, percentile4, vendor, num_d, num_i), "\n")
    return percentile1, percentile2, percentile3, percentile4, product_list

def hist_1(sum_cost, cost_list, percentile1, product_list): #histogram of costs for all possible instrument-acquisition scenarios, given V1 user-input for vendor  
    text = str(product_list) + ': \n' + str(sum_cost) + ' USD, ' + str(percentile1) + ' percentile'
    cost_list.sort()
    num_samples = len(cost_list)
    cost_list_min = cost_list[0]
    cost_list_max = cost_list[-1]
    span = cost_list_max - cost_list_min
    cost_array = np.array(cost_list)
    num_bins = int(span * ((num_samples) ** (1/3)) / stats.tstd(cost_array) / 3.49) #Scott 1979 rule of thumb for number of bins
    if num_bins % 2 == 0:
        num_bins + 1
    if num_bins <= 4:
        num_bins = 5
    bin_size = span / num_bins
    if sum_cost == cost_list_max:
        lower_bound_bin = sum_cost - bin_size
        upper_bound_bin = sum_cost
    else:
        if sum_cost == cost_list_min:
            lower_bound_bin = sum_cost
            upper_bound_bin = sum_cost + bin_size
        else:
            lower_bound_bin = (math.trunc((sum_cost - cost_list_min) / bin_size) * bin_size) + cost_list_min
            upper_bound_bin = lower_bound_bin + bin_size
    count = len([i for i in cost_list if i > lower_bound_bin and i <= upper_bound_bin])
    b = [x for x in cost_list if x > lower_bound_bin and x <= upper_bound_bin]
    c = [y for y in cost_list if y <= lower_bound_bin]
    d = [z for z in cost_list if z > upper_bound_bin]
    highlight_values = [round(num) for num in b]
    other_values_lower = [round(num) for num in c]
    other_values_upper = [round(num) for num in d]
    num_bins_lower = round((lower_bound_bin - cost_list_min) / bin_size)
    num_bins_upper = round((cost_list_max - upper_bound_bin) / bin_size)
    mid_cost_list = len(cost_list) // 2
    med_cost_list = (cost_list[mid_cost_list] + cost_list[~mid_cost_list]) / 2
    label_y_pos = count * 1.1
    if sum_cost < med_cost_list:
        label_x_pos = sum_cost - (bin_size * 2)
    else:
        label_x_pos = sum_cost
    if sum_cost >= cost_list_min + bin_size:
        a = [cost_list_min + (bin_size * n) for n in range(0, num_bins_lower + 1)]
        plt.hist(other_values_lower, bins=a, color='#607c8e', edgecolor='black')
    else:
        a = []
    plt.hist(highlight_values, bins=[lower_bound_bin, upper_bound_bin], label='bin containing:\n' + str(product_list), color='royalblue', edgecolor='black')
    if sum_cost <= cost_list_max - bin_size:
        f = [upper_bound_bin + (bin_size * n) for n in range(0, num_bins_upper + 1)]
        plt.hist(other_values_upper, bins=f, color='#607c8e', edgecolor='black')
    else:
        f = []
    bins_list = a + f
    start_list = [bins_list[n] for n in range(0,len(bins_list)-1)]
    end_list = [bins_list[n] for n in range(1,len(bins_list))]
    count_list = []
    for i in range(0, len(start_list)):
        counts = len([x for x in cost_list if start_list[i] <= x <= end_list[i]])
        count_list.append(counts)
    count_list.sort()
    max_count = count_list[-1]
    plt.title('Distribution of all procurement scenarios- all vendors and products')
    plt.xlabel('Procurement Cost (USD)')
    plt.ylabel('Counts')
    plt.text(label_x_pos, label_y_pos, text, backgroundcolor='lightgray')
    plt.legend()
    plt.ylim((None, max_count*1.2))
    plt.xlim((None, cost_list_max * 1.1))
    plt.show()
    return

def hist_2(cost_vendor, vendor, sum_cost, percentile2, product_list): #histogram of costs for all possible instrument-acquisition scenarios, given V2 user-input for vendor
    text = str(product_list) + ': \n' + str(sum_cost) + ' USD, ' + str(percentile2) + ' percentile'
    cost_vendor.sort()
    num_samples = len(cost_vendor)
    cost_vendor_min = cost_vendor[0]
    cost_vendor_max = cost_vendor[-1]
    span = cost_vendor_max - cost_vendor_min
    cost_vendor_array = np.array(cost_vendor)
    num_bins = int(span * ((num_samples) ** (1/3)) / stats.tstd(cost_vendor_array) / 3.49) #Scott 1979 rule of thumb for number of bins
    if num_bins % 2 == 0:
        num_bins + 1
    if num_bins <= 4:
        num_bins = 5
    bin_size = span / num_bins
    if sum_cost == cost_vendor_max:
        lower_bound_bin = sum_cost - bin_size
        upper_bound_bin = sum_cost
    else:
        if sum_cost == cost_vendor_min:
            lower_bound_bin = sum_cost
            upper_bound_bin = sum_cost + bin_size
        else:
            lower_bound_bin = (math.trunc((sum_cost - cost_vendor_min) / bin_size) * bin_size) + cost_vendor_min
            upper_bound_bin = lower_bound_bin + bin_size
    count = len([i for i in cost_vendor if i > lower_bound_bin and i <= upper_bound_bin])
    b = [x for x in cost_vendor if x > lower_bound_bin and x <= upper_bound_bin]
    c = [y for y in cost_vendor if y <= lower_bound_bin]
    d = [z for z in cost_vendor if z > upper_bound_bin]
    highlight_values = [round(num) for num in b]
    other_values_lower = [round(num) for num in c]
    other_values_upper = [round(num) for num in d]
    num_bins_lower = round((lower_bound_bin - cost_vendor_min) / bin_size)
    num_bins_upper = round((cost_vendor_max - upper_bound_bin) / bin_size)
    mid_cost_list = len(cost_vendor) // 2
    med_cost_list = (cost_vendor[mid_cost_list] + cost_vendor[~mid_cost_list]) / 2
    label_y_pos = count * 1.1
    if sum_cost < med_cost_list:
        label_x_pos = sum_cost - (bin_size * 2)
    else:
        label_x_pos = sum_cost
    if sum_cost >= cost_vendor_min + bin_size:
        a = [cost_vendor_min + (bin_size * n) for n in range(0, num_bins_lower + 1)]
        plt.hist(other_values_lower, bins=a, color='#607c8e', edgecolor='black')
    else:
        a = []
    plt.hist(highlight_values, bins=[lower_bound_bin, upper_bound_bin], label='bin containing:\n' + str(product_list), color='royalblue', edgecolor='black')
    if sum_cost <= cost_vendor_max - bin_size:
        f = [upper_bound_bin + (bin_size * n) for n in range(0, num_bins_upper + 1)]
        plt.hist(other_values_upper, bins=f, color='#607c8e', edgecolor='black')
    else:
        f = []
    bins_list = a + f
    start_list = [bins_list[n] for n in range(0,len(bins_list)-1)]
    end_list = [bins_list[n] for n in range(1,len(bins_list))]
    count_list = []
    for i in range(0, len(start_list)):
        counts = len([x for x in cost_vendor if start_list[i] <= x <= end_list[i]])
        count_list.append(counts)
    count_list.sort()
    max_count = count_list[-1]
    x = "Distribution of procurement scenarios given vendor selection: {}"
    plt.title(x.format(vendor))
    plt.xlabel('Procurement Cost (USD)')
    plt.ylabel('Counts')
    plt.text(label_x_pos, label_y_pos, text, backgroundcolor='lightgray')
    plt.legend()
    plt.ylim((None, max_count*1.2))
    plt.xlim((None, cost_vendor_max * 1.1))
    plt.show()
    return

def hist_3(filtered_cost_list, num_d, num_i, sum_cost, percentile3, product_list): #histogram of costs for all possible instrument-acquisition scenarios, given V3 user-input for vendor
    text = str(product_list) + ': \n' + str(sum_cost) + ' USD, ' + str(percentile3) + ' percentile'
    filtered_cost_list.sort()
    num_samples = len(filtered_cost_list)
    filtered_cost_min = filtered_cost_list[0]
    filtered_cost_max = filtered_cost_list[-1]
    span = filtered_cost_max - filtered_cost_min
    filtered_cost_array = np.array(filtered_cost_list)
    num_bins = int(span * ((num_samples) ** (1/3)) / stats.tstd(filtered_cost_array) / 3.49) #Scott 1979 rule of thumb for number of bins
    if num_bins % 2 == 0:
        num_bins + 1
    if num_bins <= 4:
        num_bins = 5
    bin_size = span / num_bins
    if sum_cost == filtered_cost_max:
        lower_bound_bin = sum_cost - bin_size
        upper_bound_bin = sum_cost
    else:
        if sum_cost == filtered_cost_min:
            lower_bound_bin = sum_cost
            upper_bound_bin = sum_cost + bin_size
        else:
            lower_bound_bin = (math.trunc((sum_cost - filtered_cost_min) / bin_size) * bin_size) + filtered_cost_min
            upper_bound_bin = lower_bound_bin + bin_size
    count = len([i for i in filtered_cost_list if i > lower_bound_bin and i <= upper_bound_bin])
    highlight_values = [round(x) for x in filtered_cost_list if x > lower_bound_bin and x <= upper_bound_bin]
    other_values_lower = [round(y) for y in filtered_cost_list if y <= lower_bound_bin]
    other_values_upper = [round(z) for z in filtered_cost_list if z > upper_bound_bin]
    mid_cost_list = len(filtered_cost_list) // 2
    med_cost_list = (filtered_cost_list[mid_cost_list] + filtered_cost_list[~mid_cost_list]) / 2
    label_y_pos = count * 1.1
    if sum_cost < med_cost_list:
        label_x_pos = sum_cost - (bin_size * 2)
    else:
        label_x_pos = sum_cost
    if sum_cost >= filtered_cost_min + bin_size:
        num_bins_lower = round((lower_bound_bin - filtered_cost_min) / bin_size)
        a = [filtered_cost_min + (bin_size * n) for n in range(0, num_bins_lower + 1)]
        plt.hist(other_values_lower, bins=a, color='#607c8e', edgecolor='black')
    else:
        a = []
    plt.hist(highlight_values, bins=[lower_bound_bin, upper_bound_bin], label='bin containing:\n' + str(product_list), color='royalblue', edgecolor='black')
    if sum_cost <= filtered_cost_max - bin_size:
        num_bins_upper = round((filtered_cost_max - upper_bound_bin) / bin_size)
        f = [upper_bound_bin + (bin_size * n) for n in range(0, num_bins_upper + 1)]
        plt.hist(other_values_upper, bins=f, color='#607c8e', edgecolor='black')
    else:
        f = []
    if sum_cost >= filtered_cost_max - bin_size:
        bins_list = a + [upper_bound_bin]
    else:
        if sum_cost <= filtered_cost_min + bin_size:
            bins_list = f + [lower_bound_bin]
        else:
            bins_list = a + f
    start_list = [bins_list[n] for n in range(0,len(bins_list)-1)]
    end_list = [bins_list[n] for n in range(1,len(bins_list))]
    count_list = []
    for i in range(0, len(start_list)):
        counts = len([x for x in filtered_cost_list if start_list[i] <= x <= end_list[i]])
        count_list.append(counts)
    count_list.sort()
    max_count = count_list[-1]
    x = "Distribution of procurement scenarios given {} device(s) and {} instrument(s)"
    plt.title(x.format(num_d, num_i))
    plt.xlabel('Procurement Cost (USD)')
    plt.ylabel('Counts')
    plt.text(label_x_pos, label_y_pos, text, backgroundcolor='lightgray')
    plt.legend()
    plt.ylim((None, max_count*1.2))
    plt.xlim((None, filtered_cost_max * 1.1))
    plt.show()
    return

def hist_4(filtered_vendor_cost_list, vendor, sum_cost, percentile4, num_d, num_i, product_list): #histogram of costs for all possible instrument-acquisition scenarios, given V4 user-input for vendor
    text = str(product_list) + ': \n' + str(sum_cost) + ' USD, ' + str(percentile4) + ' percentile'
    filtered_vendor_cost_list.sort()
    num_samples = len(filtered_vendor_cost_list)
    filtered_vendor_cost_min = filtered_vendor_cost_list[0]
    filtered_vendor_cost_max = filtered_vendor_cost_list[-1]
    span = filtered_vendor_cost_max - filtered_vendor_cost_min
    filtered_cost_array = np.array(filtered_vendor_cost_list)
    num_bins = int(span * ((num_samples) ** (1/3)) / stats.tstd(filtered_cost_array) / 3.49) #Scott 1979 rule of thumb for number of bins
    if num_bins % 2 == 0:
        num_bins + 1
    if num_bins <= 4:
        num_bins = 5
    bin_size = span / num_bins
    if sum_cost == filtered_vendor_cost_max:
        lower_bound_bin = sum_cost - bin_size
        upper_bound_bin = sum_cost
    else:
        if sum_cost == filtered_vendor_cost_min:
            lower_bound_bin = sum_cost
            upper_bound_bin = sum_cost + bin_size
        else:
            lower_bound_bin = (math.trunc((sum_cost - filtered_vendor_cost_min) / bin_size) * bin_size) + filtered_vendor_cost_min
            upper_bound_bin = lower_bound_bin + bin_size
    count = len([i for i in filtered_vendor_cost_list if i > lower_bound_bin and i <= upper_bound_bin])
    highlight_values = [round(x) for x in filtered_vendor_cost_list if x > lower_bound_bin and x <= upper_bound_bin]
    other_values_lower = [round(y) for y in filtered_vendor_cost_list if y <= lower_bound_bin]
    other_values_upper = [round(z) for z in filtered_vendor_cost_list if z > upper_bound_bin]
    mid_cost_list = len(filtered_vendor_cost_list) // 2
    med_cost_list = (filtered_vendor_cost_list[mid_cost_list] + filtered_vendor_cost_list[~mid_cost_list]) / 2
    label_y_pos = count * 1.1
    if sum_cost < med_cost_list:
        label_x_pos = sum_cost - (bin_size * 2)
    else:
        label_x_pos = sum_cost
    if sum_cost >= filtered_vendor_cost_min + bin_size:
        num_bins_lower = round((lower_bound_bin - filtered_vendor_cost_min) / bin_size)
        a = [filtered_vendor_cost_min + (bin_size * n) for n in range(0, num_bins_lower + 1)]
        plt.hist(other_values_lower, bins=a, color='#607c8e', edgecolor='black')
    else:
        a = []
    plt.hist(highlight_values, bins=[lower_bound_bin, upper_bound_bin], label='bin containing:\n' + str(product_list), color='royalblue', edgecolor='black')
    if sum_cost <= filtered_vendor_cost_max - bin_size:
        num_bins_upper = round((filtered_vendor_cost_max - upper_bound_bin) / bin_size)
        f = [upper_bound_bin + (bin_size * n) for n in range(0, num_bins_upper + 1)]
        plt.hist(other_values_upper, bins=f, color='#607c8e', edgecolor='black')
    else:
        f = []
    if sum_cost >= filtered_vendor_cost_max - bin_size:
        bins_list = a + [upper_bound_bin]
    else:
        if sum_cost <= filtered_vendor_cost_min + bin_size:
            bins_list = f + [lower_bound_bin]
        else:
            bins_list = a + f
    start_list = [bins_list[n] for n in range(0,len(bins_list)-1)]
    end_list = [bins_list[n] for n in range(1,len(bins_list))]
    count_list = []
    for i in range(0, len(start_list)):
        counts = len([x for x in filtered_vendor_cost_list if start_list[i] <= x <= end_list[i]])
        count_list.append(counts)
    count_list.sort()
    max_count = count_list[-1]
    x = "Distribution of procurement scenarios given vendor section {}, {} device(s) and {} instrument(s)"
    plt.title(x.format(vendor, num_d, num_i))
    plt.xlabel('Procurement Cost (USD)')
    plt.ylabel('Counts')
    plt.text(label_x_pos, label_y_pos, text, backgroundcolor='lightgray')
    plt.legend()
    plt.ylim((None, max_count*1.2))
    plt.xlim((None, filtered_vendor_cost_max * 1.1))
    plt.show()
    return

def hist_5(cost_v1, cost_v2, cost_v3, cost_v4): #histogram of all vendor pricing options / procurement scenarios
    plt.hist(cost_v1, histtype='stepfilled', bins = 13, alpha = 0.25, label = 'V1', edgecolor='black', color='royalblue')
    plt.hist(cost_v2, histtype='stepfilled', bins = 12, alpha = 0.25, label = 'V2', edgecolor='black', color='lightcoral')
    plt.hist(cost_v3, histtype='stepfilled', bins = 20, alpha = 0.25, label = 'V3', edgecolor='black', color='forestgreen')
    plt.hist(cost_v4, histtype='stepfilled', bins = 10, alpha = 0.25, label = 'V4', edgecolor='black', color='dimgrey')
    plt.legend(loc = 'upper right')
    plt.title('Comparison of all vendor price options')
    plt.xlabel('Procurement Cost (USD)')
    plt.ylabel('Counts')
    plt.grid(axis = 'y')
    plt.show()
    return

def main():
    while True:
        introduction()
        vendor = get_vendor()
        num_d, num_i = get_number(vendor)
        D1, D2, D3, I1, I2, I3 = get_variables(vendor, num_d, num_i)
        sum_cost = user_input_cost(D1, D2, D3, I1, I2, I3, vendor)
        df_vendor, df_v1, df_v2, df_v3, df_v4 = get_dfs(vendor)
        cost_vendor, cost_v1, cost_v2, cost_v3, cost_v4, cost_list = get_costs(df_vendor, df_v1, df_v2, df_v3, df_v4)
        code_vendor, code_list = get_codes(df_vendor, df_v1, df_v2, df_v3, df_v4)
        filtered_cost_list = filter_cost_list(code_list, cost_list, num_d, num_i)
        filtered_vendor_cost_list = filter_vendor_cost_list(code_vendor, cost_vendor, num_d, num_i)
        percentile1, percentile2, percentile3, percentile4, product_list = data_report(cost_list, sum_cost, cost_vendor, filtered_cost_list, filtered_vendor_cost_list, vendor, num_d, num_i, code_list, code_vendor, D1, D2, D3, I1, I2, I3)
        hist_1(sum_cost, cost_list, percentile1, product_list)
        hist_2(cost_vendor, vendor, sum_cost, percentile2, product_list)
        hist_3(filtered_cost_list, num_d, num_i, sum_cost, percentile3, product_list)
        hist_4(filtered_vendor_cost_list, vendor, sum_cost, percentile4, num_d, num_i, product_list)
        hist_5(cost_v1, cost_v2, cost_v3, cost_v4)

        restart = input('\nWould you like to restart? Enter \'yes\' or \'no\'.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()