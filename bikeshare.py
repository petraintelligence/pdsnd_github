import time
import math
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
cities = ["Chicago", "New York City", "Washington"]
MONTH_DATA = {'january': 1,
              'february': 2,
              'march': 3,
              'april': 4,
              'may': 5,
              'june': 6,
              'july': 7,
              'august': 8,
              'september': 9,
              'october': 10,
              'november': 11,
              'december': 12}

WEEK_DATA = {'monday': 0,
             'tuesday': 1,
             'wednesday': 2,
             'thursday': 3,
             'friday': 4,
             'saturday': 5,
             'sunday': 6}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Good day Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        while True:
            city_input = str(
                input("What city would you like to analyze:{}? ".format(cities)).title())
            if city_input in cities:
                city_final = city_input.lower()
                city = CITY_DATA[city_final]
                break
            print("Please choose one of the three cities from the list ")

    # TO DO: get user input for month (all, january, february, ... , june)
        while True:
            month_input = str(input(
                "What month would you like to filter for? If you would like see the data unfiltered, type 'all': ").lower())
            if month_input in MONTH_DATA and month_input != "all":
                month = MONTH_DATA[month_input]
                break
            if month_input == "all":
                month = month_input
                break
            print("Please select a valid month ")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            day_input = str(input(
                "What day of the week would you like to filter for? If you would like see the data unfiltered, type 'all': ").lower())
            if day_input in WEEK_DATA and day_input != "all":
                day = WEEK_DATA[day_input]
                break
            if day_input == "all":
                day = day_input
                break
            print("Please select a valid day ")
        # Verify user input is correct
        print("You chose the following filters: {}, {}, {}. ".format(
            city_final.title(), month_input.title(), day_input.title()))
        print('-'*40)
        correct_response = str(
            input("Are these filters correct (yes/no)? ").lower())
        if correct_response == "yes":
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
    df = pd.read_csv(city)
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    if day != 'all':
        df = df[df['day_of_week'] == day]
    if month != 'all':
        df = df[df['month'] == month]
    df.drop('day_of_week', axis=1, inplace=True)
    df.drop('month', axis=1, inplace=True)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    for num in MONTH_DATA:
        if MONTH_DATA[num] == common_month:
            common_month = num.title()
    print('The most common month for travel is {}'.format(common_month))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    for num in WEEK_DATA:
        if WEEK_DATA[num] == common_day:
            common_day = num.title()
    print('The most common day of week for travel is {}'.format(common_day))

    # TO DO: display the most common start hour
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour for travel is {}:00'.format(common_hour))
    df.drop('hour', axis=1, inplace=True)
    df.drop('day_of_week', axis=1, inplace=True)
    df.drop('month', axis=1, inplace=True)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station was {}'.format(
        df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('The most commonly used end station was {}'.format(
        df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    combo = df['Start Station'] + ' to ' + df['End Station']
    print('The most frequnt combination of start station and end station trip was {}'.format(
        combo.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    travel_durations = pd.to_datetime(
        df['End Time']) - pd.to_datetime(df['Start Time'])

    # TO DO: display total travel time
    td_sum = df['Trip Duration'].sum()
    sum_seconds = td_sum % 60
    sum_minutes = td_sum//60 % 60
    sum_hours = td_sum//3600 % 60
    sum_days = td_sum//24//3600
    print('Passengers traveled a total of {} days, {} hours, {} minutes and {} seconds'.format(
        sum_days, sum_hours, sum_minutes, sum_seconds))

    # TO DO: display mean travel time
    td_mean = math.ceil(df['Trip Duration'].mean())
    mean_seconds = td_mean % 60
    mean_minutes = td_mean//60 % 60
    mean_hours = td_mean//3600 % 60
    mean_days = td_mean//24//3600
    print('Passengers traveled an average of {} hours, {} minutes and {} seconds'.format(
        mean_hours, mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.groupby('User Type', as_index=False).count()
    print('Number of types of users are {}'.format(len(user_types)))
    for i in range(len(user_types)):
        print(
            '{}s - {}'.format(user_types['User Type'][i], user_types['Start Time'][i]))

    # TO DO: Display counts of gender
    print()
    if 'Gender' not in df:
        print('No gender data for this selection')
    else:
        gender_counts = df.groupby('Gender', as_index=False).count()
        print('Number of genders of users mentioned in the data are {}'.format(
            len(gender_counts)))
        for i in range(len(gender_counts)):
            print(
                '{}s - {}'.format(gender_counts['Gender'][i], gender_counts['Start Time'][i]))
        print('Gender data for {} users is not available'.format(
            len(df)-gender_counts['Start Time'][0]-gender_counts['Start Time'][1]))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print('Birth year data is not available for this selection')
    else:
        birth = df.groupby('Birth Year', as_index=False).count()
        print('Earliest year of birth was {}.'.format(
            int(birth['Birth Year'].min())))
        print('Most recent year of birth was {}.'.format(
            int(birth['Birth Year'].max())))
        print('Most common year of birth year was {}.'.format(
            int(birth.iloc[birth['Start Time'].idxmax()]['Birth Year'])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    choice = input('Would you like to review the raw data? Yes/No ').lower()
    print()
    if choice == 'yes':
        choice = True
    elif choice == 'no':
        choice = False
    else:
        print('Please select Yes/No ')
        display_data(df)
        return

    if choice:
        while 1:
            for i in range(5):
                print(df.iloc[i])
                print()
            choice = input('Another five? Yes/No ').lower()
            if choice == 'yes':
                continue
            elif choice == 'no':
                break
            else:
                print('Please select Yes/No')
                return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('Would you like to restart? Yes/No').lower()
        print()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
