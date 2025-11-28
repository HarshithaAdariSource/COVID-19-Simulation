import pandas as pd
import random
from datetime import datetime, timedelta
from helper import create_plot
from sim_parameters import TRANSITION_PROBS, HOLDING_TIMES

#creating sample population
def s_pop(df, s_ratio):
    ppl = []
    p_id = 0
    ag = ['less_5', '5_to_14', '15_to_24', '25_to_64', 'over_65']
    #zip the rows to iterate
    for country, population, l5, a5_14, a15_24, a25_64, o65 in zip(df['country'], df['population'],df['less_5'], df['5_to_14'], df['15_to_24'], df['25_to_64'], df['over_65']):
        num_samples = int(population / s_ratio)
        percents = [l5, a5_14, a15_24, a25_64, o65]
        for age, percent in zip(ag, percents):
            num_age_samples = round(num_samples * percent / 100)
            for _ in range(num_age_samples):
                ppl.append({
                    'person_id': p_id,
                    'country': country,
                    'age_group': age
                })
                p_id += 1
    return ppl

#Simulating transitions
def sim_transitions(ppl, st_date, end_date):
    start = pd.to_datetime(st_date)
    end = pd.to_datetime(end_date)
    dates = pd.date_range(start, end)
    records = []

    for per in ppl:
        age_group = per['age_group']
        country = per['country']
        current_state = 'H'
        prev_state = 'H'
        stay_days = 0
        rem_days = HOLDING_TIMES[age_group][current_state]
        for current_date in dates:
            records.append({
                'p_id': per['person_id'],
                'age_group': age_group,
                'country': country,
                'date': current_date.strftime('%Y-%m-%d'),
                'state': current_state,
                'staying_days': stay_days,
                'prev_state': prev_state
            })
            if rem_days > 1:
                rem_days -= 1
                stay_days += 1
            else:
                transitions = TRANSITION_PROBS[age_group][current_state]
                next_state = random.choices(list(transitions.keys()),weights=list(transitions.values()))[0]
                prev_state = current_state
                current_state = next_state
                stay_days = 0
                rem_days = HOLDING_TIMES[age_group][current_state]
    return pd.DataFrame(records)

#plot and summarization
def sum_plot(sim_df, countries):
    summary = sim_df.groupby(['date', 'country', 'state']).size().unstack(fill_value=0).reset_index()
    tot_states = ['H', 'I', 'S', 'M', 'D']
    for state in tot_states:
        if state not in summary.columns:
            summary[state] = 0
    summary = summary[['date', 'country'] + tot_states]
    summary.to_csv('a2-covid-summary-timeseries.csv', index=False)
    create_plot('a2-covid-summary-timeseries.csv', countries)

#run method
def run(countries_csv_name, countries, sample_ratio, start_date, end_date):
    df = pd.read_csv(countries_csv_name) #reading the data
    df = df[df['country'].isin(countries)]
    people = s_pop(df, sample_ratio) #sample population
    sim_df = sim_transitions(people, start_date, end_date)
    sim_df.to_csv('a2-covid-simulated-timeseries.csv', index=False) #transition simulating
    sum_plot(sim_df, countries)#graph creation