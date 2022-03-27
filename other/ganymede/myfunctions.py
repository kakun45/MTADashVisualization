import pandas as pd
import folium
import numpy as np

IMPORTANT_FILE1 = "turnstile_191019.txt"
MTA1stTxt = "turnstile_191019.txt"

#a dataFrame for testing
def newdf():
    return pd.DataFrame({
        "a": [1,2,3],
        "b": [4,5,6]
    })

#apply a diff func for entire df
def diffAll(df):
    #_59THST_NQR456W["entries_diff"] = _59THST_NQR456W["ENTRIES"].diff()
    return df.diff()


# this func creates/add a new column 'newcolname' to df, requires a col 'colname' 
# newcolname: how to call a brandnew col
# colname: which col will be used to preform diff
def diffCol(df, colname, newcolname):
    df2 = df.copy()
    df2[newcolname] = df2[colname].diff()
    return df2

# old ver: this func creates/add a new column 'entries_diff' to df, requires a col 'ENTRIES' 
def diffColEntr(df):
    df2 = df.copy()
    df2["entries_diff"] = df2["ENTRIES"].diff()
    return df2

def addDiffs(df_list, colname, newcolname):
    """
    :param df_list: a list of dataFrames that contiain an "ENTRIES" column
        each dataFrame is for a specific turnstile
    :returns: a list of dataFrames, each with a new 'newcolname' 
        (ex."entries_diff"/"exits_diff") column added
    """
    turnstile_dfs_diff = []
    for dfs in df_list:
        #dfs2 = dfs.copy()    #or just use existing func of mine
        #dfs2['entries_diff'] = dfs2['ENTRIES'].diff()
        #turnstile_dfs_diff.append(dfs2)
        turnstile_dfs_diff.append(diffCol(dfs, colname, newcolname))
    return turnstile_dfs_diff
    

#plot the E 59th station on the map. >> index10.html
#pin one location of E 59th st in blue on the Midtown map, save the result into html file map-index
def map59th():
    map = folium.Map(location = [40.7628, -73.9676], zoom_start = 70, tiles = 'Stamen Terrain')

    folium.CircleMarker(location=[40.7628, -73.9676],
                    popup = "59THST (NQR456W trains)",
                    radius = 10,
                    color = 'blue',
                    fill = True).add_to(map)
    map.save('map-index.html')

# plot all the stations on the map
#def mapMidtown(df):
    #map = folium.Map(location = [40.7628, -73.9676], zoom_start = 60, tiles = 'Stamen Terrain')

    #folium.CircleMarker([r for r in df[station_id]: location=[df['LAT'], df['LON']],
                    #popup = df['station_id'],
                    #radius = df['ENTRIES_diff_sum']/2,
                    #color = 'green',
                    #fill = True]).add_to(map)
    #return map.save('map-test-index.html')


#Add a weekday to a df, requires a 'DATE' col
#Requires & Performed on df with coloumn named 'DATE'. 
# outcome: new col named 'WEEKDAY'
def myweekday(df):
    df2 = df.copy()
    df2['WEEKDAY'] = pd.to_datetime(df2['DATE']).dt.weekday_name
    return df2


# takes a 'df' with the col 'LINENAME', creates a working col by: 
# -separates each char, 
# -sort them alphabeticaly, 
# -merge them back together 
# -concat station name and a new col separated by '-', 
# -drops a working col
# returns a df with a new col named in 'colname'
def unique_station(df, colname):
    df["LINENAME2"] = df["LINENAME"].apply(sorted).apply("".join)
    df[colname] = df["STATION"] + "-" + df["LINENAME2"]
    df = df.drop(["LINENAME2"], axis=1)
    return df

#create 24:00 time bins grouping by 4 hour each -1 includes 00:00:00-th hour
# requires "hODname" (!in quotetions while passing into func) - for df to have 'hour of a day' col (ex. 'HOD')
# timestamp (!in quotetions while passing into func) - combo of date and time - col (ex.'TIMESTAMP')
#'HODBIN' - will cretes a new col with HOD+bins, that is interval, not an int/float
#'HODBIN2' - a new col (int) - represents a 1st hour from bins intervals - adds +1hour for exclusively created bins
def bintimes(df, hour_day_name, timestamp):
    '''create Hour of Day bins
    use a negative number at the beginning to ensure we do not lose midnight
    '''
    bins = [-1,3,7,11,15,19,24] 
    df2 = df.copy()
    df2[hour_day_name] = [r.hour for r in df2[timestamp]] 
    df2['HODBIN'] = pd.cut(df2[hour_day_name], bins)
    #create new col to get info from bins
    df2['HODBIN_hour'] = [b.left+1 for b in df2.HODBIN]
    return df2


#groupping and sum (on the col)
#requires to drop 5 col-s: 'HOD','ENTRIES','EXITS','TIME', 'TIMESTAMP'
#requires cols to group by: 'HODBIN','HODBIN2','UNIT','SCP','STATION','LINENAME','DATE','station_id','WEEKDAY','SCP_STATION'
#sum on 2 cols "ENTRIES_diff_sum",'EXITS_diff_sum'
#renames those new col-s 
#resets the index back to the rows
#here by default: requires to drop: 'HOD','ENTRIES','EXITS','TIME', 'TIMESTAMP'
#here by default: requires to groupby: 'HODBIN','HODBIN2','UNIT','SCP','STATION','LINENAME','DATE','station_id','WEEKDAY','SCP_STATION'
def grouping_sum(
    df,
    drop_columns = ['HOD','ENTRIES','EXITS','TIME', 'TIMESTAMP'],
    group_col = ['HODBIN','HODBIN2', 'UNIT','SCP','STATION','LINENAME','DATE','station_id','WEEKDAY','SCP_STATION'],
    new_columns = ["ENTRIES_diff_sum",'EXITS_diff_sum'],
):
    df2 = df.copy()
    df2 = df2.drop(drop_columns, axis='columns')
    df2 = df2.groupby(group_col).agg([np.sum]) 
    df2.columns = new_columns
    df3 = df2.reset_index()
    return df3

#enhanced grouping_sum made more generic
# stil takes a df and copy it
# the requirements are the lists of strings of names of the df col-s
#it sums the passed list of cols sum_col = ['', '']
# it takes cols what to group as alist of strings of names of cols group_col = [' ', ' ']
# and it calculates what cols to drop 
#creates a new cols passed as a list of strings ex. new_col = ['' , '']
def grouping_sum2(
    df,
    group_col,
    sum_col,
    new_col
):
    df2 = df.copy()
    assert len(sum_col) == len(new_col)
    all_columns = list(df2.columns)
    drop_col = list(set(all_columns) - set(sum_col) - set(group_col)) 
    df2 = df2.drop(drop_col, axis='columns')
    df2 = df2.groupby(group_col).agg([np.sum]) 
    df2.columns = new_col
    df3 = df2.reset_index()
    return df3

# merge left with geo tag on same col (ex. 'UNIT') - requires the column_toMerge
def mergeLeft(df, df_with_geo, column_toMerge):
    df2 = df.copy()
    df2 = pd.merge(left=df2,right=df_with_geo, how='left', on=column_toMerge)
    return df2


#drops values less than 10,
#where num = 10 - number which defines drop those that "smaller than"
# 'col_togothrough' - the col where the fun will look for num
def less10(df, col_togothrough, num):
    df2 = df.copy() 
    df2 = df2[df2[col_togothrough] > num]  
    return df2


#to sort a df by a proper order of a weekday, this func adds a ne col Day_id according its dict, where Sun is 0..Sat is 6
#takes a 'col_weekday' col with a weekday string
def sorterOfWeekday(df, col_weekday):
    # don't use daymap = { "Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}
    daymap = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
    df2 = df.copy() 
    df2['Day_id'] = df2.index
    df2['Day_id'] = df2[col_weekday].map(daymap)
    return df2