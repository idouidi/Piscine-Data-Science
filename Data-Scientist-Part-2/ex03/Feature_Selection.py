import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

df = pd.read_csv('Train_knight.csv')
df.columns = df.columns.str.strip()
df = df.drop('knight', axis=1)

scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

# Step 2: Calculate VIF for each attribute
vif_results = []

for attr in df_scaled.columns:
    # X = all other attributes (drop the current attribute)
    X = df_scaled.drop(attr, axis=1).values

    # y = current attribute
    y = df_scaled[attr].values

    # Linear regression 
    model = LinearRegression()
    model.fit(X, y)

    # R² = (1 - (SS_res / SS_tot))  <= how well model predicts this attribute from others 
    # y_pred = model.predict(X)     <= Model's predictions for the current attribute
    # SS_res = Σ(y - y_pred)²       <= Residual sum of squares (how much error in prediction)
    # SS_tot = Σ(y - y_mean)²       <= Total variation of  the attribute
    # R² = 1                        <= means perfect prediction, R²
    r_squared = model.score(X, y)

    # VIF = 1 / (1 - R²)
    vif = 1 / (1 - r_squared)

    vif_results.append({'VIF': vif, 'Tolerance': 1/vif})

# Convert to dataframe and sort
vif_df = pd.DataFrame(vif_results, index=df_scaled.columns)
vif_df = vif_df.sort_values('VIF')

# Keep only VIF < 5
vif_filtered = vif_df[vif_df['VIF'] < 5]

print(vif_filtered.to_string())