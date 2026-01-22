import streamlit as st
import pandas as pd
import numpy as np
import pickle

file = st.file_uploader('Upload your stock csv file here:')
if file:
    df = pd.read_csv(f'{file.name}',encoding='latin1')
    df.dropna(inplace=True)
    df['precentage'] = df['Close'].pct_change()
    df['Volume'] = df['Volume']/10**6

    for i in range(0,5):
        df[f'lag{i+1}'] = np.nan

    df['lag_vol'] = np.nan

    df.reset_index(drop=True,inplace=True)
    for i in range(0,2956):
        for j in range(1,6):
            if i!=0:
                df.loc[i,f"lag{j}"] = df.loc[i-1,'precentage']

    for i in range(0,2956):
        if i!=0:
            df.loc[i,'lag_vol'] = df.loc[i-1,'Volume']

    df.dropna(inplace=True)

    df['avg_ret'] = df[['lag1','lag2','lag3','lag4','lag5']].mean(axis=1)
    df['dir'] = df['avg_ret'].apply(lambda x: 1 if x>=0 else 0)
    x = df[['lag1','lag2','lag3','lag4','lag5','lag_vol']]


    with open('Bull_Bear_model.pickle','rb') as f:
        model = pickle.load(f)
        ans = model.predict(x)
        if 0 in ans:
            ans_2 = 'Bearish'
        else:
            ans_2 = 'Bullish'
    if ans_2=="Bullish":
        st.success(f"The Selected Stock is {ans_2}")
    else:
        st.error(f"The Selected Stock is {ans_2}")
    st.write("Open price for the next day:")


    def create_sequences(df,timestep=5):
        x_open = []
        y_open = []
        df.dropna(inplace=True)
        for i in range(len(df)-timestep):
            x = df['Open'].iloc[i:i+timestep].values
            y = df['Open'].iloc[i+timestep]
            x_open.append(x)
            y_open.append(y)
        return np.array(x_open),np.array(y_open)

    x_open,y_open = create_sequences(df)


    with open('prediction_model.picke','rb') as f:
        support = pickle.load(f)
        ans_1 = support.predict(x_open)

    st.success(f"The open price for next day is {ans_1[-1]}")