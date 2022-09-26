import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA= {'jan':'january','feb':'february','mar':'march',
             'apr':'april', 'may':'may', 'jun':'june', 'all':'all'}
DAY_DATA = {0: 'sunday', 1:'monday',2:'tuesday',3:'wednesday', 4:'thursday', 5:'friday', 6:'saturday', 7:'all'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('\nWich city would you like to see: "washington", "new york", "chicago\n').lower().strip()
        except ValueError:
            print('wrong input please choose one of the following options washington, new york, chicago in lower case')
            continue
        if city not in CITY_DATA:
            print('wrong input please choose one of the following options washington, new york, chicago in lower case')
            continue
        else: 
            #print('you entered', CITY_DATA[city])
            break
            
    while True:
        try:
            month = input('\n please specify a month between january and jun, using first 3 letters. \n enter "all", for no filter\n').lower().strip()
        except ValueError:
            print('''Oops you've provided a wrong input, please choose one of the following options (jan, feb, mar, apr, may, jun or all).\n''')
            continue
        if month not in MONTH_DATA:
            print('''Oops you've provided a wrong input, please choose one of the following options (jan, feb, mar, apr, may, jun or all).\n''')
            continue
        else:
            #print('you entered', MONTH_DATA[month])
            month = MONTH_DATA[month]
            break
            
    while True:
        try:
            day = int(input('\n please specify a day using a number between 0 and 7: 0 = Sunday and 7 = no filter\n'))
        except ValueError:
            continue
        if day not in DAY_DATA.keys():
            print('''Oops you've provid a wrong input, please specify a day using a number between 0 and 7: 0 = Sunday and 7 = no filter\n''')
            continue
        else:
            print('you entered', DAY_DATA[day])
            answerlist = ['y', 'n']
        try:
            question = input('if this is correct press y to continue n to select a different day\n')
        except ValueError:
            continue
        if question not in answerlist:
            print('''Opps, you've entered an invalid answer, please enter y to continue or n to select a different day\n''')
            continue
        elif question =='n':
            continue
        else:
            #print('break', DAY_DATA[day])
            day = DAY_DATA[day]
            break
    print('-'*40)  
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['month_int'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['day_of_week'].astype(str)
    df[['month_int', 'month']].value_counts()
    df.columns = df.columns.str.replace(' ', '_').str.lower().str.replace('unnamed:_0', 'ID')

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = (months.index(month)+1)
        #print('the month is',month)
        # filter by month to create the new dataframe
        df = df[df['month_int'] == month_num]
        
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode().values[0]
    num_m =df.groupby('month')['month'].count().max()
    print('Most Popular Start Month:', popular_month.capitalize(), '>> occuring',num_m,'times')


    # display the most common day of week
    popular_week = df['day_of_week'].mode().values[0]
    num_w =df.groupby('day_of_week')['day_of_week'].count().max()
    print('Most Popular Day of Week:', popular_week.capitalize(), '>> occuring',num_w,'times')

    # display the most common start hour
    df['hour'] = df['start_time'].dt.hour
    num_h =df.groupby('hour')['hour'].count().max()
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour, '>> occuring',num_h,'times')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    df_st =df['start_station'].value_counts().rename_axis('start_station').to_frame('counts').reset_index()
    pop =df_st['counts']==df_st['counts'].max()
    print('The most commonly used Start Station is:',df_st.loc[pop,'start_station']\
    .to_string(index=False),';With a count of:',df_st.loc[pop,'counts'].to_string(index=False),'rides' )

    # display most commonly used end station
    df_ed =df['end_station'].value_counts().rename_axis('end_station').to_frame('counts').reset_index()
    pop =df_ed['counts']==df_ed['counts'].max()
    print('The most commonly used End Station is:',df_ed.loc[pop,'end_station']\
    .to_string(index=False),';With a count of:',df_ed.loc[pop,'counts'].to_string(index=False),'Rides' )

    # display most frequent combination of start station and end station trip
    df_comb = df[['start_station','end_station']].value_counts().to_frame('counts')
    df_comb.reset_index()
    pop = df_comb['counts'].max()
    filt = df_comb[df_comb['counts']==pop].reset_index()
    print('The most frequent combination of start station and end station trip is:\nstart_station:',filt['start_station']\
    .to_string(index=False),'\nend_station',filt['end_station']\
    .to_string(index=False),'\nWith a count of:', filt['counts'].to_string(index = False))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    def strfdelta(tdelta, fmt):
        d = {"days": tdelta.days}
        d["hours"], rem = divmod(tdelta.seconds, 3600)
        d["minutes"], d["seconds"] = divmod(rem, 60)
        return fmt.format(**d)

    trip_sum = ((df['end_time'] - df['start_time']).sum())
    print('total travelling time is',strfdelta(trip_sum,"{hours} hours, {minutes} minutes and {seconds} seconds"))

    trip_mean = ((df['end_time'] - df['start_time']).mean())
    print('\nThe mean travelling time is:',strfdelta(trip_mean,"{hours} hours, {minutes} minutes and {seconds} seconds"))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df_types = df.user_type.value_counts().rename_axis('user_type').to_frame('counts').reset_index()
    print(df_types.to_string(index = False))

    # Display counts of gender
    try:
        df_gender = df.gender.value_counts().rename_axis('gender').to_frame('counts').reset_index()
        print(df_gender.to_string(index = False))
    except:
        print('The columns "gender" is not available in this dataseet')
    
    try:
        com_year = df.birth_year.value_counts(sort=True,ascending=False)\
        .rename_axis('common_year').to_frame('counts').reset_index()
        print('Earliest year of birth:   ',int(df.birth_year.min()),'\nMost recent year of birth:',int(df.birth_year.max()),'\nMost common year of birth:',int(com_year.loc[:0,'common_year']))
    except:
        print('The column "birth_year" is not available in this dataset')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """displaying raw data files on request"""
    start_time = time.time()
    responses = ['yes','y','no','n']
    n=5
    dfs = df.reset_index()
    while True:
        try:
            response = input('\nWould you like to see raw data set? please enter yes or no\n').lower()
        except ValueError:
            continue
        if response not in responses:
            print('''Oops you've provid a wrong input, please enter yes to continue''')
            continue
        elif response != 'yes':
            print('No raw data requested')
            break
        else:
            a=0
            b=5
            while response=='yes':
                dfs_=dfs.iloc[a:b,1:]
                for row in dfs_.iterrows():
                    time.sleep(1) # Sleep for 1 seconds
                    print(row, '*'*40)
                try:
                    follow_up = input('\nWould you like to see more raw data? please enter "yes" to continue\n').lower()
                except ValueError:
                    continue
                if follow_up != 'yes' :
                    response= follow_up
                else:
                    a += 5
                    b += 5
                    dfs_= dfs.iloc[a:b,1:]
        print('terminate raw data request')
        break
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        time.sleep(1) # Sleep for 1 seconds
        trip_duration_stats(df)
        user_stats(df)
        time.sleep(1) # Sleep for 1 seconds
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
