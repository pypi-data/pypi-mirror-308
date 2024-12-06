import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

def pls_da_plot(df, label_column='sample', n_components=2):
    # Extract features (X) and labels (y) from the DataFrame
    X = df.drop(columns=[label_column])  # Drop non-feature columns
    y = df[label_column].apply(lambda x: 'OE' if 'oe' in x else 'WT')  # Label the sample types
    
    # Encode the labels for PLS-DA
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)  # Convert 'OE'/'WT' to numeric labels
    
    # Split the data for validation
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Initialize PLS-DA with the specified number of components
    pls_da = PLSRegression(n_components=n_components)
    
    # Fit the PLS-DA model on the training data
    pls_da.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = pls_da.predict(X_test)
    y_pred_class = [1 if pred >= 0.5 else 0 for pred in y_pred.ravel()]  # Threshold at 0.5 for classification
    
    # Evaluate the accuracy and display the confusion matrix
    accuracy = accuracy_score(y_test, y_pred_class)
    conf_matrix = confusion_matrix(y_test, y_pred_class)
    
    print(f"PLS-DA Accuracy: {accuracy}")
    print("Confusion Matrix:")
    print(conf_matrix)
    
    # Transform the entire dataset to PLS components
    X_scores = pls_da.transform(X)
    
    # Create a plot for the PLS-DA components
    plt.figure(figsize=(10, 8))
    plt.scatter(X_scores[y_encoded == 0, 0], X_scores[y_encoded == 0, 1], label='WT', color='b')
    plt.scatter(X_scores[y_encoded == 1, 0], X_scores[y_encoded == 1, 1], label='OE', color='r')
    
    # Annotate the points with the sample names
    for i, txt in enumerate(df[label_column]):
        plt.text(X_scores[i, 0] + 0.05, X_scores[i, 1], txt, fontsize=8)
    
    # Plot settings
    plt.xlabel('PLS Component 1')
    plt.ylabel('PLS Component 2')
    plt.title('PLS-DA Plot with Sample Names')
    plt.legend(title='Sample Type')
    plt.grid(True)
    plt.show()

# Example Usage:
# df = pd.read_csv("your_data.csv")  # Load your DataFrame
# perform_pls_da_plot(df)  # Call the function with your DataFrame
