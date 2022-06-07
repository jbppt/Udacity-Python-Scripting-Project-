import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
      city = input('\nWhich city would you like to see data for? Please enter either Chicago, New York City, or Washington.\nType the option exactly as you see it with no extra spaces.\n')
      if city not in ('Chicago', 'New York City', 'Washington'):
        print('Please try again. Remember to type the option exactly as you see it with no spaces!')
        continue
      else:
        break

    # get user input for month (all, january, february, ... , june)
    while True:
      month = input('\nWhich month would you like to see data for? Please enter either January, February, March, April, May, or June.\nType the word all if you want to see data for all.\nType the option exactly as you see it with no extra spaces.\n')
      if month not in ('January', 'February', 'March', 'April', 'May', 'June', 'all'):
        print('Please try again. Remember to type the option exactly as you see it with no spaces!')
        continue
      else:
        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
      day = input('\nWhich day would you like to see data for? Please enter either Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday.\nType the word all if you want to see data for all.\nType the option exactly as you see it with no extra spaces.\n')
      if day not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'all'):
        print('Please try again. Remember to type the option exactly as you see it with no spaces!')
        continue
      else:
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is ', most_common_month)

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day is ', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common start hour is ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('The most commonly used start station is ', most_common_start)

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('The most commonly used end station is ', most_common_end)

    # display most frequent combination of start station and end station trip
    most_frequent_combination = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('The most frequent combination of start station and end station trip is ', most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types = df['User Type'].value_counts()
    print('Counts of user types: ', counts_of_user_types)

    # Display counts of gender
    if 'Gender' in df:
        counts_of_gender = df['Gender'].value_counts()
        print('Counts of gender: ', counts_of_gender)
    else:
        print('Gender information not available.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('The most common birth year is ', int(most_common_birth_year))
        most_recent = df['Birth Year'].max()
        print('The most recent birth year is ', int(most_recent))
        earliest = df['Birth Year'].min()
        print('The earliest birth year is ', int(earliest))
    else:
        print('Birth year information not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_raw_data(df):
    raw = 0
    while True:
        see_raw_data = input("Would you like to see raw data? Please type 'Yes' or 'No' exactly as you see it.")
        if see_raw_data not in ['Yes', 'No']:
            see_raw_data = input("Please type 'Yes' or 'No' exactly as you see it.")
        elif see_raw_data == 'Yes':
            raw += 5
            print(df.iloc[raw : raw + 5])
        elif see_raw_data == 'No':
            return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
