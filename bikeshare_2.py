import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
  
    while True:
        city = input('Select a city to be analyzed: \n').lower()
        if city in CITY_DATA:
            break
        else:
            print('Your input does not match a city the database has data for.  Please revise.')
    
    while True:
        month = input('Select a month to be analyzed, or say \'all\' to apply no month filter: \n').lower()
        if month in months:
            break
        else:
            print('Your input does not match a month the database has data for.  Please revise.')
    
    while True:
        day = input('Select a day of the week to be analyzed, or say \'all\' to apply no day of the week filter: \n').lower()
        if day in days:
            break
        else:
            print('Your input does not match a day of the week the database has data for.  Please revise.')

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

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    most_common_month = df['month'].value_counts().idxmax()
    print('The most common month is: ', most_common_month)
   
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print('The most common day of the week is: ', most_common_day_of_week)
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour is: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station is: ', most_common_start_station)
    
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print('The most commonly used end station is: ', most_common_end_station)
    
    df['StartEnd'] = df['Start Station'].map(str) + '  &  ' + df['End Station']
    most_frequent_trip = df['StartEnd'].value_counts().idxmax()
    print('The most frequent combination of start station and end station trip is: ', most_frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    total_time = df['Trip Duration'].sum()
    print('Total travel time is: ', total_time)
   
    mean_time = df['Trip Duration'].mean()
    print('Mean travel time is: ', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    user_types = df['User Type'].value_counts().to_frame()
    print('A count of user types: ', user_types)
   
    try:
        gender_counts = df['Gender'].value_counts().to_frame()
        print('A count of user gender: ', gender_counts)
    except:
        print('There is no gender data for this city.')
    
    try:
        birth_year = df['Birth Year']
    
        earliest_year_of_birth = birth_year.min()
        print('The earliest year of birth is: ', earliest_year_of_birth)
    
        most_recent_year_of_birth = birth_year.max()
        print('The most recent year of birth is: ', most_recent_year_of_birth)
    
        most_common_year = birth_year.value_counts().idxmax()
        print('The most common year of birth is: ', most_common_year)
    except:
        print('There is no birth year data for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def display_data(df):
    """Displays raw bikeshare data."""
    
    print('\nDisplay Data...\n')
    
    lower_bound=0; upper_bound=5
    
    while True:
        raw = input('\nWould you like to view 5 (more) lines of raw bikeshare data? Enter yes or no.\n')
        if raw.lower() != 'yes':
            break
        else:
            print(df[df.columns[0:]].iloc[lower_bound:upper_bound])
            lower_bound += 5; upper_bound += 5
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
