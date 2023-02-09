import psycopg2
import collections
import re
import numpy as np
import matplotlib.pyplot as plt

def get_all_request():
# """ Connect to the PostgreSQL database server """ #
    connection = psycopg2.connect(host = "localhost",
                                  user = "postgres",
                                  password = " ",
                                  database = " ",
                                  port = "5432")
    cursor = connection.cursor()
    postgreSQL_select_Query = "SELECT * FROM public.request WHERE request LIKE '%[08/Feb/2023%'"
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from request table using cursor.fetchall")
    opts = cursor.fetchall()
    
    result_list = []
    for i in range(len(opts)):
        result_list.append(list(opts[i]))
        
    
    '''
    Extract Time
    '''
    for index, item in enumerate(result_list):
        result_list[index] = result_list[index][0].split(" - - ")

    def ExtractTime(lst):
        return [item[1] for item in lst]

    lst = result_list
 
    time_list = []
    for i in range(len(ExtractTime(lst))):
        m = re.findall('\[.*?\]', ExtractTime(lst)[i])
        time_list.append(m[0])
        
    time_array = np.array(time_list)
    
    '''
    IP address
    '''  
    def ExtractIP(lst):
        return [item[0] for item in lst]
        
    for x in time_list:
        ExtractIP(lst).append(x)
        
    ip_array = np.array(ExtractIP(lst))
    
    counter = collections.Counter(ip_array)      
        
    combine_array = np.stack((ip_array, time_array), axis=1)
    
    final_list = []
    for i in range(len(combine_array)):
        ip = combine_array[i][0]
        time = combine_array[i][1]
        final_list.append(ip + " " + time)

    counter = collections.Counter(final_list)
    
    
    labels, values = zip(*Counter(final_list).items())
    indexes = np.arange(len(labels))
    width = 1
    
    # Risize the figure (optional)    
    plt.figure(figsize=(20, 8))
    plt.bar(indexes, values, width, color='#6ce3c6', edgecolor='#20a785')
    plt.xticks(indexes + width * 0.5, labels ,rotation='vertical')
    plt.title('smart Logbook Web Application Traffic', fontsize=22)
    plt.ylabel('Request count', fontsize=18)
    plt.xlabel('IP address & Time', fontsize=18)
    
    # Display the graph
    plt.show()
    
    
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed \n")
    
