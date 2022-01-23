from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from sklearn.linear_model import LinearRegression
import os
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/processing", methods=["POST"])
def processing():
    app.config['UPLOAD_FOLDER'] = "/Users/antarikshverma/Dev/machacks-api/uploads"
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    df = pd.read_csv("uploads/" + filename)
    order_priority = pd.get_dummies(df['Order_Priority'])
    ship_mode = pd.get_dummies(df['Ship_Mode'])
    customer_segment = pd.get_dummies(df['Customer_Segment'])
    product_container = pd.get_dummies(df['Product_Container'])
    df = df.drop(columns="Customer_Name")
    df = df.drop(columns="Region")
    df = df.drop(columns="Order_Priority")
    df = df.drop(columns="Ship_Mode")
    df = df.drop(columns="Customer_Segment")
    df = df.drop(columns="Product_Category")
    df = df.drop(columns="Product_Name")
    df = df.drop(columns="Product_Sub-Category")
    df = df.drop(columns="Product_Container")
    df = df.join(order_priority)
    df = df.join(ship_mode)
    df = df.join(customer_segment)
    df = df.join(product_container)
    
    scaler = StandardScaler()
    scaler.fit(df.drop('Profit', axis = 1))
    scaled_features = scaler.transform(df.drop('Profit', axis = 1))

    X_train, X_test, y_train, y_test = train_test_split(scaled_features, df["Profit"], test_size=0.2)
    regr = RandomForestRegressor(max_depth=7)
    regr.fit(X_train, y_train)
    print(mean_squared_error(y_test, regr.predict(X_test)))
    return { "accuracy": "pig" }


if __name__ == "__main__":
    app.run(debug=True)
