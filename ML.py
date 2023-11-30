# package imports
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

# local imports
import data_handler


def train_model():
    df = data_handler.get_data()
    X = df['text']
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Define the pipeline
    pipeline = make_pipeline(TfidfVectorizer(), MultinomialNB())

    # Define the parameter grid
    parameters = {
        'tfidfvectorizer__max_df': (0.5, 0.75, 1.0),
        'tfidfvectorizer__ngram_range': [(1, 1), (1, 2)],  # unigrams or bigrams
        'multinomialnb__alpha': (1e-2, 1e-3)
    }

    # Conduct parameter search with cross-validation
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)
    print("Performing grid search...")
    print("Pipeline:", [name for name, _ in pipeline.steps])
    print("Parameters:")
    print(parameters)
    grid_search.fit(X_train, y_train)

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))

    # Evaluate the best model on the test set
    y_pred = grid_search.predict(X_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    return grid_search.best_estimator_


def analyze_sentiment(sentence, model):
    """
    Analyze the sentiment of a given sentence using the trained model.

    Args:
    sentence (str): The sentence to analyze.
    model (sklearn Pipeline): The trained sentiment analysis model.

    Returns:
    str: The predicted sentiment of the sentence.
    """
    # Ensure the input is in the same format expected by the model (e.g., a list of sentences)
    processed_sentence = [sentence]

    # Predict the sentiment
    sentiment_prediction = model.predict(processed_sentence)

    return sentiment_prediction[0]


trained_model = train_model()  # Assuming train_model() is your model training function
sentence = "I really enjoyed this movie!"
predicted_sentiment = analyze_sentiment(sentence, trained_model)
print(f"The predicted sentiment of the sentence is: {predicted_sentiment}")


