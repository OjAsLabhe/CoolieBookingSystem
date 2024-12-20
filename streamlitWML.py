import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor

def calculate_efficiency(data):
    df = pd.DataFrame(data)
    
    data.iloc[:, 1:] += np.random.choice([-1, 1], size=df.iloc[:, 1:].shape)

    X_train = df.drop(columns=['coolie_id'])
    y_train = df['coolie_id']

    weights = np.random.dirichlet(np.ones(len(X_train.columns)), size=1)[0] * 100

    efficiency_scores = {}

    for coolie_id in df['coolie_id']:
        X_train_excluded = X_train[X_train.index != coolie_id - 1]
        y_train_excluded = y_train[X_train.index != coolie_id - 1]
        model = DecisionTreeRegressor(random_state=42)
        model.fit(X_train_excluded, y_train_excluded)
        efficiency = model.predict(X_train.iloc[coolie_id - 1:coolie_id])
        weighted_efficiency = sum(weight * eff for weight, eff in zip(weights, efficiency))
        efficiency_scores[coolie_id] = max(0, min(100, weighted_efficiency))

    efficiency_above_90 = {coolie_id: efficiency for coolie_id, efficiency in efficiency_scores.items() if efficiency > 90}

    random_5_coolie_ids = np.random.choice(list(efficiency_above_90.keys()), size=min(5, len(efficiency_above_90)), replace=False)
    random_5_results = [(coolie_id, efficiency_above_90[coolie_id]) for coolie_id in random_5_coolie_ids]

    return random_5_results

def calculate_charge(weight_of_bags):
    rate_per_kg = 20
    charge = weight_of_bags * rate_per_kg
    return charge

def main():
    st.title("Coolie Booking Form")

    st.header("Passenger Information")
    with st.form(key='user_info_form'):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        email = st.text_input("Email")
        gender = st.radio("Gender", options=["Male", "Female", "Other"])
        numbags = st.number_input("Number of Bags", min_value=0, step=1)
        webags = st.number_input("Approx Weight of Bags (in kg)", min_value=0.0, step=0.1)
        date = st.date_input("Date for Booking")
        platformno = st.number_input("Platform Number", min_value=1, step=1)
        traino = st.number_input("Train Number", min_value=1, step=1)
        find_coolies_button = st.form_submit_button(label='Find Coolies')

    if find_coolies_button:
        data = pd.read_csv(r"C:\Users\labhe\OneDrive\Desktop\dataset (2).csv")  
        results = calculate_efficiency(data)
        st.write("Coolies with best performance available right now!! ")

        df_results = pd.DataFrame(results, columns=['Coolie ID', 'Efficiency'])

        st.table(df_results)

        if 'selected_coolie_id' not in st.session_state:
            st.session_state.selected_coolie_id = None  

    if "selected_coolie_id" in st.session_state:
        st.write("Coolie Chosen (Enter Coolie ID):")
        coolie_chosen = st.text_input("Coolie ID")
        
        confirm_booking_button = st.button("Confirm Booking")

        if confirm_booking_button:
            charge = calculate_charge(webags)

            user_details = {
                "Details": ["Name", "Age", "Email", "Gender", "Number of Bags", "Approx Weight of Bags (kg)","Approx cost ", "Date for Booking", "Platform Number", "Train Number", "Coolie ID"],
                "Data": [name, age, email, gender, numbags, webags,charge, date, platformno, traino, coolie_chosen]
            }
            df_user_details = pd.DataFrame(user_details)
            st.write("User Details:")
            st.table(df_user_details)
            if st.button("Finalize Booking"):
                st.write("Booking Finalized!")

if __name__ == "__main__":
    main()
