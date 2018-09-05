############################################
#Project 6
#Prompts User to enter file name
#Prompts user to enter state
#Returns data for each county in the state
#Asks user if they would like to plot the data
#Creates pi chart
#################################################


import pylab
STATES = {'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY'}
USERS = ["Public", "Domestic", "Industrial", "Irrigation","Livestock"]

def open_file():
    '''prompts user to enter a file name, opens the file and returns it. 
    If there is an error it tells the user then prompts for another filename.'''
    filename = input("Input a file name:")
    while filename != ' ':
        
        try:
            fp = open(filename, 'r')
        
            return fp
            break
        except FileNotFoundError:
            print(" Unable to open file. Please try again.") 
            filename = input("Input a file name:")
    
def read_file(fp):
    '''reads a given file and returns a data list.
    fp: a file opened for reading
    returns a data list with relevant information from the file'''
    data_list=[]
    header = fp.readline()
    for line in fp:
        line = line.strip()
        line = line.split(",")
        for i in range(0, len(line)):
            if line[i] == 'N/A' or line[i] =='':
                line[i]= "0"
        state= line[0]      #state
        county= line[2]     #county
        population = float(line[6]) * 1000      #population
        fresh_water_usage = float(line[114])    #fresh water usage
        salt_water_usage = float(line[115])     #salt water usage
        water_usage_public = float(line[18])    #public water usage
        water_usage_domestic = float(line[26])  #domestic water usage
        water_usage_industrial = float(line[35]) #industrial water usage   
        water_usage_irrigation = float(line[45])    #irrigation water usage
        water_usage_livestock = float(line[59])     #livestock water usage
        
        tuple1 = (state, county, population,fresh_water_usage, salt_water_usage,\
                  water_usage_public, water_usage_domestic, water_usage_industrial,\
                  water_usage_irrigation, water_usage_livestock)
        data_list.append(tuple1)
        
    return data_list
  

def compute_usage(state_list):
    '''Computes total water used and fresh water usage per person.
    state_list : list of water usage for a specific state
    returns a tuple for each county in the state'''
    county_list = []        #county data for each county in the state
    for tuple1 in state_list:
        county = tuple1[1]
        population = tuple1[2]
        fresh_water = tuple1[3]
        salt_water = tuple1[4]
        total_water = fresh_water + salt_water      #calculates total water
        per_person = fresh_water / population       #calculates fresh water per person
        
        tup = (county, population, total_water, per_person)
        county_list.append(tup)
    return county_list
   
    
def extract_data(data_list, state):
    '''Gives a list of all water usage data in given state.
    data_list : all of the data in the file
    state: any given state that user enters
    returns a list of tuples for each county in the given state'''
    
    state_list = []         #water usage in the state
    for tuple1 in data_list:
        if tuple1[0] == state or state == "ALL":            #separates data based off of state
            state_list.append(tuple1)
          
    return state_list
        
        

def display_data(state_list, state):
    
    '''displays county name, population, total water usage per person, 
    total water used by the county for each county in the state.
    state_list : a list of all data for given state
    state: any state given by user
    returns formatted data for each county in the state'''

    county_list = compute_usage(state_list)    
    title = "Water Usage in " + state + " for 2010"
    header = "{:22s} {:>22s} {:>22s} {:>22s}".format("County", \
              "Population", "Total (Mgal/day)", "Per Person (Mgal/person)")
    county_data = []
    print("{:^88s}".format(title))
    print(header)
    for county in county_list:
        county_name = county[0] #name of the county
        county_pop = county[1]  #population of county
        county_twpp = county[3] #county total water per person
        county_tw = county[2]   #county total water
        data_f = "{:22s} {:>22,.0f} {:>22.2f} {:>22.4f}".format(county_name, \
              county_pop, county_tw, county_twpp)
        print(data_f)
    
    
    
    return county_data

def plot_water_usage(some_list, plt_title):
    '''
        Creates a list "y" containing the water usage in Mgal/d of all counties.
        Y should have a length of 5. The list "y" is used to create a pie chart
        displaying the water distribution of the five groups.

        This function is provided by the project.
    '''

    # accumulate public, domestic, industrial, irrigation, and livestock data
    y =[ 0,0,0,0,0 ]

    for item in some_list:

        y[0] += item[5]
        y[1] += item[6]
        y[2] += item[7]
        y[3] += item[8]
        y[4] += item[9]

    total = sum(y)
    y = [round(x/total * 100,2) for x in y] # computes the percentages.

    color_list = ['b','g','r','c','m']
    pylab.title(plt_title)
    pylab.pie(y,labels=USERS,colors=color_list)
    pylab.show()
    pylab.savefig("plot.png")  
    
def main():
    '''This function runs the main portion of the program 
    by calling all the other functions'''
    
    print("Water Usage Data from the US and its States and Territories.\n")
    fp = open_file()            #calls the open_file function which allows the user to enter a filename
    data_list = read_file(fp)   #calls the read_file function to return all the data
    state = input("\nEnter state code or 'all' or 'quit': ")    #prompts user to enter state
    state = state.upper()
    while state != 'QUIT':
        
        if state not in STATES and state != 'ALL' :         #prompts user to reenter state
            print("Error in state code.  Please try again.") 
            state = input("\nEnter state code or 'all' or 'quit': ")
            state = state.upper()
        if state == 'ALL':
           
            state_list = extract_data(data_list, state)
            display_data(state_list, state)
            answer = input("\nDo you want to plot? ")
            if answer == 'yes':
                
                plot_water_usage(state_list, "Water Usage in " + state + " for 2010")       #plots data
            else:
                state = input("\nEnter state code or 'all' or 'quit': ")
                state = state.upper()
            
        if state in STATES: 
            state_list = extract_data(data_list, state) 
            display_data(state_list, state)             #displays data for the state entered by county
            answer = input("\nDo you want to plot? ")
            if answer == 'yes':
                
                plot_water_usage(state_list, "Water Usage in " + state + " for 2010")       #plots data
            else:
                state = input("\nEnter state code or 'all' or 'quit': ")
                state = state.upper()
        
            
    

if __name__ == "__main__":  
    main()
    
