"""Creating a Chatbot to review the Pride and Prejudice story by Jane Austen."""

# Import necessary libraries
import nltk
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st

# Load the text file and preprocess the data
with open('Pride and Prejudice by Jane Austen.txt', 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')

# Tokenize the text into sentences
sentences = sent_tokenize(data)

# Define a function to preprocess each sentence
def preprocess(sentence):
    """Preprocess a sentence by tokenizing, removing stopwords, and lemmatizing."""
    words = word_tokenize(sentence)
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.lower() not in stop_words and word not in string.punctuation]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Preprocess each sentence
corpus = [preprocess(sentence) for sentence in sentences]

# Define a function to find the most relevant sentence
def get_most_relevant_sentence(query):
    """Find the most relevant sentence based on word overlap."""
    query = preprocess(query)
    max_similarity = 0
    most_relevant_sentence = "I’m sorry, I couldn’t find a relevant response."
    for original_sentence, processed_sentence in zip(sentences, corpus):
        similarity = len(set(query).intersection(processed_sentence)) / float(len(set(query).union(processed_sentence)))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = original_sentence
    return most_relevant_sentence

# Define the chatbot function
def chatbot(question):
    """Generate a response to the user's question."""
    if not question.strip():
        return "Please ask a question."
    return get_most_relevant_sentence(question)

# Create a Streamlit app
def main():
    st.title("Chatbot")
    st.write("Hello! I'm a chatbot. Ask me anything about the topic in the text file.")
    st.write("Example: 'What happened during the war?'")
    
    question = st.text_input("You:")
    if st.button("Submit"):
        response = chatbot(question)
        st.write("Chatbot: " + response)

if __name__ == "__main__":
    main()
