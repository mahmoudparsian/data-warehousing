from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Create a string of text
text = "Python is a versatile programming language known for its simplicity and readability. It is widely used in various fields such as data science, web development, and machine learning."

# Generate a word cloud image
wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=STOPWORDS).generate(text)

# Display the generated image
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
