import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
##   pip install wordcloud

# Generate random data
categories = ['Madrid', 'New York', 'Mumbai', 'Paris', 'Toronto', 'Tokyo', 'London']
num_data_points = 500
data = np.random.choice(categories, num_data_points)

# Create a DataFrame
df = pd.DataFrame({'Category': data})

# Count the occurrences of each category
category_counts = df['Category'].value_counts()

# Generate word cloud based on category counts
wordcloud = WordCloud(width=800, height=400, background_color='white', 
                      colormap='viridis', max_font_size=100, max_words=50, 
                      margin = 5, prefer_horizontal = 0.7)
wordcloud.generate_from_frequencies(category_counts)

# Display the word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
