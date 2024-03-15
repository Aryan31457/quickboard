from flask import Flask ,request

app = Flask(__name__)

import pandas as pd

# Read the data from CSV
data = pd.read_csv("C:/Users/aryan/OneDrive/Desktop/quickboard/TrainDelay-project-main/dataset/trains.csv")

# Function to estimate delay for a given train
def estimate_delay(train_ID):
    # Filter data for the given train ID
    train_data = data[data['train_ID'] == train_ID]
    
    # If train data exists
    if not train_data.empty:
        # Filter out missing or invalid delay values
        valid_delays = train_data['delay'].dropna()
        if valid_delays.empty:
            return 0  # Return 0 if no valid delays found
        else:
            # Calculate average delay
            avg_delay = valid_delays.mean()
            return max(0, avg_delay)  # Ensure delay is non-negative
    else:
        return 0  # Return 0 if train data not found

# Function to calculate probability of missing Train B
def probability_missing_train_B(train_ID1, train_ID2):
    # Estimate delay for Train A
    delay_train_A = estimate_delay(train_ID1)
    
    # If delay for Train A is available
    if delay_train_A > 0:
        # Estimate delay for Train B
        delay_train_B = estimate_delay(train_ID2)
        
        # If delay for Train B is available
        if delay_train_B > 0:
            # Calculate the probability of missing Train B
            percentage = ((delay_train_A - delay_train_B) / delay_train_A) * 100
            return max(0, percentage)  # Ensure probability is non-negative
        else:
            return 0  # Return 0 if delay for Train B is not available
    else:
        return 0  # Return 0 if delay for Train A is not available

# Take input of train_ID from user

@app.route('/output')
def output():
    data=request.get_json()
    l=data["D1"]
    print (type(l))
    print(l)
    train_ID1 = l[0]
    train_ID2 = l[1]
    

# Get expected delays
    expected_delay1 = estimate_delay(train_ID1)
    expected_delay2 = estimate_delay(train_ID2)

    # Calculate and print delays of both trains
    print(f"Delay of train ID {train_ID1}: {expected_delay1} minutes")
    print(f"Delay of train ID {train_ID2}: {expected_delay2} minutes")

    # Calculate and print expected probability
    expected_probability = probability_missing_train_B(train_ID1, train_ID2)
    print(f"Expected probability of missing train B: {expected_probability}%")

    # Calculate and print predicted probability (use train IDs for estimation)
    predicted_probability = probability_missing_train_B(train_ID1, train_ID2)
    print(f"Predicted probability of missing train B: {predicted_probability}%")
    output_l=[expected_delay1,expected_delay2,predicted_probability]
    return output_l,200

# if __name__=='__main__':
#     app.run(debug=True,port=8000,use_reloader=True)
