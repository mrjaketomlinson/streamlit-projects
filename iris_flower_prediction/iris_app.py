# Imports
import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

# Title and Description
st.write("""
# Simple Iris Flower Prediction App
This app predicts the **Iris flower** type.
* **Python libraries:** pandas, streamlit, scikit-learn, matplotlib
* **Data source:** scikit-learn
* **Project Credit:** Adapted from [Chanin Nantasenamat (aka Data Professor)](https://www.youtube.com/watch?v=JwSS70SZdyM).
Improved on the look of the prediction and prediction probability. Added a bar chart to show probability of each class.
""")

# Sidebar - User inputs
st.sidebar.header('User Input Parameters')


def user_input_features():
    # Defines user inputs and returns inputs as a data frame
    sepal_length = st.sidebar.slider('Sepal length', 4.3, 7.9, 5.4)
    sepal_width = st.sidebar.slider('Sepal width', 2.0, 4.4, 3.4)
    petal_length = st.sidebar.slider('Petal length', 1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider('Petal width', 0.1, 2.5, 0.2)
    data = {
        'sepal_length': sepal_length,
        'sepal_width': sepal_width,
        'petal_length': petal_length,
        'petal_width': petal_width
    }
    features = pd.DataFrame(data, index=[0])
    return features


df = user_input_features()

# Display user inputs
st.subheader('User Input Parameters')
st.dataframe(df)

# Load in the iris dataset
iris = datasets.load_iris()
x = iris.data # 4 features we have the user define: sepal length/width and petal length/width
y = iris.target # Class index number (0, 1, 2)

clf = RandomForestClassifier()
clf.fit(x, y)

prediction = clf.predict(df)
prediction_probability = clf.predict_proba(df)

# Write class labels + index
st.subheader('Class labels')
st.write('The possible Iris classes are: {}'.format(', '.join([x for x in iris.target_names])))

# Class prediction
st.subheader('Prediction')
st.write(iris.target_names[prediction][0])

# Prediction probability output
st.subheader('Prediction Probability')
st.write('This is the probability of being in one of the three classes mentioned above.')
# Create/show data frame
pred_proba = pd.DataFrame({
    'class': ['setosa', 'versicolor', 'virginica'], 'probability': prediction_probability[0]
})
st.dataframe(pred_proba)
# Create/show bar chart
fig, ax = plt.subplots(figsize=(5,2))
p1 = ax.bar(pred_proba['class'], pred_proba['probability']*100)
ax.bar_label(p1, labels=[f'{int(x)}%' for x in pred_proba['probability']*100])
plt.ylim([0,100])
plt.xlabel('Iris Class')
plt.ylabel('Probability')
st.pyplot(plt)
