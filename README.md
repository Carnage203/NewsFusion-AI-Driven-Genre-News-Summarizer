# AI Article Generator & Image Enhancer

## Project Description

The **AI Article Generator & Image Enhancer** is an end-to-end solution designed to streamline the consumption of news content. By automatically aggregating the latest news articles based on a user-defined genre, summarizing the content into a structured article, and generating a relevant, high-quality image, this project aims to reduce information overload and enhance user engagement. The solution leverages state-of-the-art natural language processing and image synthesis APIs to deliver concise, detailed, and visually appealing news summaries—all via an intuitive web interface built with Streamlit.

## Problem Statement

In today's fast-paced digital landscape, users are inundated with news from multiple sources. Traditional methods of news aggregation require manually sifting through content and summarizing key information, which can be both time-consuming and prone to inaccuracies. Additionally, simply presenting textual information may not capture user attention effectively. This project addresses the following challenges:

- **Information Overload:** Users struggle to process vast amounts of news data.
- **Manual Summarization:** Manual extraction of key points from multiple articles is inefficient and inconsistent.
- **Lack of Visual Engagement:** Text-only summaries often fail to capture the full essence of the news, reducing user engagement.

![](https://github.com/Carnage203/Article-Generator/blob/3ac31523b76fbe8e49681b236691de84421bfb80/1.png)
![](https://github.com/Carnage203/Article-Generator/blob/3ac31523b76fbe8e49681b236691de84421bfb80/2.png)

## Work Done

The project consists of three major components:

1. **News Aggregation:**
   - Integrates with the Google Search API to fetch the latest news articles based on a specified genre.
   - Allows users to input genres such as *Science*, *Technology*, or *Health* to retrieve targeted news.

2. **Content Summarization:**
   - Uses a large language model (ChatGoogleGenerativeAI) to generate a structured and detailed article.
   - The article is divided into key sections: **Headline/Title**, **Byline**, **Body**, **Background Information**, and **Conclusion**.
   - A carefully crafted prompt ensures that the summarization is based solely on the provided news content, reducing reliance on external or outdated data.

3. **Visual Generation:**
   - Integrates with the Flux API to produce a realistic and high-quality image that visually represents the article's headline.
   - The image prompt is optimized to capture the visual essence of the article, ensuring coherence and relevance.

4. **User Interface:**
   - Built with Streamlit, the interactive UI features an input form (with Enter-key submission) for ease-of-use.
   - The UI displays the generated article with enhanced formatting (e.g., an enlarged headline) and includes an expander to view the raw JSON response for debugging.
   - Optionally, the UI can also generate and display a related image.

## Tech Stack

The project utilizes the following technologies:

- **Python:** Core programming language for building the application and handling API integrations.
- **Streamlit:** Provides a fast and interactive web-based UI for real-time news generation and image display.
- **LangChain & ChatGoogleGenerativeAI:** Facilitate interaction with the language model for generating structured articles.
- **Google Search API (via langchain_google_community):** Fetches the latest news articles based on user input.
- **Flux API:** Generates high-quality images relevant to the article's content.
- **PIL (Python Imaging Library):** Handles image processing and display.
- **JSON & Requests:** Manage API communication and data formatting.
