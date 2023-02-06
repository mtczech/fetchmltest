import matplotlib.pyplot as plt
import csv
import sys

# This function assumes that the dates are written in the form "YYYY-MM-DD".
def return_month_vals(dates_list):
    months = {'January':0, 'February':0, 'March':0, 'April':0, 'May':0, 'June':0, 'July':0, 'August':0,\
        'September':0, 'October':0, 'November':0, 'December':0}
    index_to_months = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', \
        '06':'June', '07':'July', '08': 'August', '09':'September', '10':'October', '11':'November', '12':'December'}
    for date in dates_list:
        split_date = date[0].split('-')
        current_month = index_to_months[split_date[1]]
        months[current_month] += date[1]
    return months


# Takes in the previous values and calculates a weighted derivative based on
# how recent they were
def calculate_derivative(prev_values, decay_coeff, threshold):
    decay_factor = 1
    total_deriv = 0
    total_coeff = 0
    for i in range(-1, -len(prev_values) + 1, -1):
        current_deriv = prev_values[i] - prev_values[i - 1]
        total_deriv += current_deriv * decay_factor
        total_coeff += decay_factor
        decay_factor *= decay_coeff
        if decay_factor < threshold:
            break
    return total_deriv/total_coeff

# Note: this is based on the assumption that the next year will not be a leap year


if __name__ == "__main__":
    decay_factor = float(sys.argv[1]) # The first argument put in after the name
    threshold = float(sys.argv[2]) # The second argument put in after the name
    master_list = []
    csv_input = "data_daily.csv"
    with open(csv_input) as file:
        read_csv = csv.reader(file, delimiter=',')
        for row in read_csv:
            master_list.append(row)
    del master_list[0]
    total_list = [int(x[1]) for x in master_list]
    new_year_list = []
    DECAY_COEFF = decay_factor
    THRESHOLD = threshold
    master_list = [[x[0], int(x[1])] for x in master_list]
    first_year = return_month_vals(master_list)
    for i in range(len(master_list)):
        new_date = master_list[i][0]
        new_date.replace('2021', '2022')
        # Hard coded here to change the year 2021 to 2022
        new_val = int(total_list[len(total_list) - 1] + calculate_derivative(total_list, DECAY_COEFF, THRESHOLD))
        # Note: The values might be off by a few thousand due to rounding errors
        # since the int() function always rounds down, changing the derivatives gained at the next step.
        total_list.append(new_val)
        new_year_list.append([new_date, new_val])
    second_year = return_month_vals(new_year_list)
    final_month_returns = []
    for x in first_year.keys():
        final_month_returns.append((x + ' 2021', first_year[x]))
    for x in second_year.keys():
        final_month_returns.append((x + ' 2022', second_year[x]))
    plt.plot([x[0] for x in final_month_returns], [x[1] for x in final_month_returns])
    plt.xticks([0, 6, 12, 18])
    plt.xlabel('Months')
    plt.ylabel('Scanned receipts (1e8 = in tens of millions)')
    plt.show()
