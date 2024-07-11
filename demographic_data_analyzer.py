import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_df = df.dropna(subset=['race'])
    race_count = race_df['race'].value_counts()

    # What is the average age of men?
    average_age_men = df[df['sex'] == 'Male']['age'].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = (((df['education'] == 'Bachelors').sum() / len(df.index)) * 100).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    higher_education_high_income = higher_education[higher_education['salary'] == '>50K']

    lower_education = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_education_high_income = lower_education[lower_education['salary'] == '>50K']
    
    # percentage with salary >50K
    higher_education_rich = round(((len(higher_education_high_income) / len(higher_education)) * 100), 1)
    lower_education_rich = round(((len(lower_education_high_income) / len(lower_education)) * 100), 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    hours_per_week = pd.to_numeric(df['hours-per-week'], errors='coerce')
    hours_per_week = hours_per_week.dropna()

    min_work_hours = hours_per_week.min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    temp_df = df.copy()
    temp_df['hours-per-week'] = pd.to_numeric(temp_df['hours-per-week'], errors='coerce')
    temp_df = temp_df.dropna(subset=['hours-per-week'])

    num_min_workers = temp_df[temp_df['hours-per-week'] == min_work_hours]

    num_min_workers_rich = num_min_workers[num_min_workers['salary'] == '>50K'] 
    rich_percentage = (len(num_min_workers_rich) / len(num_min_workers)) * 100

    # What country has the highest percentage of people that earn >50K?
    temp_df = pd.DataFrame().assign(Country=df['native-country'], Salary=df['salary'])
    temp_df = temp_df.dropna()
    temp_df['Salary'] = temp_df['Salary'].apply(lambda x: 1 if x == '>50K' else 0)

    earnings_in_countries_percentage =  (temp_df.groupby('Country')['Salary'].mean() * 100).round(1)

    highest_earning_country = earnings_in_countries_percentage.idxmax()
    highest_earning_country_percentage = earnings_in_countries_percentage.max()

    # Identify the most popular occupation for those who earn >50K in India.
    temp_df = df[df['native-country'] == 'India']
    temp_df = temp_df[temp_df['salary'] == '>50K']

    occupation_counts = temp_df['occupation'].value_counts()
    top_IN_occupation = occupation_counts.idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(
            f"Percentage with higher education that earn >50K: {higher_education_rich}%"
        )
        print(
            f"Percentage without higher education that earn >50K: {lower_education_rich}%"
        )
        print(f"Min work time: {min_work_hours} hours/week")
        print(
            f"Percentage of rich among those who work fewest hours: {rich_percentage}%"
        )
        print("Country with highest percentage of rich:",
              highest_earning_country)
        print(
            f"Highest percentage of rich people in country: {highest_earning_country_percentage}%"
        )
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
