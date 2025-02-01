import os, json, requests
from PIL import Image
from io import BytesIO
import streamlit as st
from constants import GOOGLE_CSE_ID, GOOGLE_API_KEY, GOOGLE_GEMINI_API_KEY, FLUX_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_community import GoogleSearchAPIWrapper

# Set up environment variables for API keys
os.environ["GOOGLE_CSE_ID"] = GOOGLE_CSE_ID
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_GEMINI_API_KEY"] = GOOGLE_GEMINI_API_KEY
os.environ["FLUX_API_KEY"] = FLUX_API_KEY

# Streamlit UI setup
st.set_page_config(page_title="AI Article Generator", layout="wide")
st.title("AI Article Generator")
st.markdown("This application fetches news articles, summarizes them into a detailed article, and generates a related image.")

# User input 
with st.form(key="article_form"):
    genre = st.text_input("Enter the genre of articles you want:", placeholder="e.g., Science, Technology, Health")
    submit_button = st.form_submit_button(label="Generate Article and Image")
    
if submit_button:
    # Search for the genre articles using the Google Search API
    st.info("Fetching articles...")
    search = GoogleSearchAPIWrapper(k=5)
    tool = Tool(
        name="google_search",
        description="Search Google for recent news articles regarding a specific topic.",
        func=search.run,
    )

    news = tool.run(f"{genre} news articles")
    st.markdown("### News Articles")
    st.write(news)  # Display fetched articles

    # Initialize the LLM for article generation with increased max_tokens for longer output
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.8,
        max_tokens=2048,   
        timeout=None,
    )

    # Article generation prompt 
    system_prompt = """
You are a smart news editor who summarizes the provided news into a concise, yet detailed article. The article should have the following sections:

1. **Headline/Title**: A clear and engaging title that summarizes the main idea of the article.
2. **Byline**: The name of the author or byline (AI as name if necessary).
3. **Body**: The main content of the article, which should summarize the key points of the given news.**Expand on the details and provide a comprehensive overview.**
4. **Background Information**: Context or historical information relevant to the topic to help the reader understand the broader situation.
5. **Conclusion**: A summary or final thoughts of the article.

Each section should be formatted clearly with the following rules:
- Use **bold** for the section titles (e.g., **Headline**, **Byline**, **Body**, **Background Information**, and **Conclusion**).
- Leave **one line of space** between each section for clarity.
- The content of each section should follow the title. For example:
  - **Headline**: [Insert Title Here]
  - **Byline**: [Author's Name Here]
  - **Body**: [Insert Body Text Here]
  - **Background Information**: [Insert Relevant Context Here]
  - **Conclusion**: [Insert Conclusion Here]

Ensure each section is **clearly separated** and uses the exact format provided above.
Use only the provided news to generate the article.

Output the article in **JSON format** with the keys:
- "Headline"
- "Byline"
- "Body"
- "Background Information"
- "Conclusion"
"""

    question = f"Provide an article only using the following news content:{news}"

    with st.spinner("Generating article..."):
        raw_response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]).content

    # Function to clean the raw response
    def clean_raw_response(raw):
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if lines[0].strip().startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()
        lines = cleaned.splitlines()
        if lines and lines[0].strip().lower() == "json":
            lines = lines[1:]
        return "\n".join(lines).strip()

    raw_response_clean = clean_raw_response(raw_response)

    try:
        article_json = json.loads(raw_response_clean)
    except json.JSONDecodeError:
        st.error("Failed to parse JSON response from the LLM. Raw cleaned response:")
        st.text(raw_response_clean)
        article_json = {}

    # Create two columns: one for the article and one for debugging/raw response if needed
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Generated Article")
        if article_json:
            headline = article_json.get("Headline", "N/A")
            st.markdown(f"<h1 style='font-size: 36px; color: white;'>{headline}</h1>", unsafe_allow_html=True)
            st.markdown(f"**Byline:** {article_json.get('Byline', 'N/A')}")
            st.markdown("**Body:**")
            st.write(article_json.get("Body", "N/A"))
            st.markdown("**Background Information:**")
            st.write(article_json.get("Background Information", "N/A"))
            st.markdown("**Conclusion:**")
            st.write(article_json.get("Conclusion", "N/A"))
        else:
            st.write("No valid article was generated.")

    with col2:
        with st.expander("Show Raw JSON Response"):
            st.code(raw_response_clean, language="json")

    #Image Generation
    st.markdown("### Generating Image...")

    url = "https://api.segmind.com/v1/flux-1.1-pro"
    data = {
        "seed": 12345,
        "width": 1024,
        "height": 1024,
        "prompt": (f"'{article_json.get('Headline', '')}'. The image should clearly reflect the subject matter mentioned, "
        "incorporating appropriate visual elements related to the topic. Ensure the image is visually coherent and "
        "directly connected to the article's content, avoiding any misleading or false representations."),
        "aspect_ratio": "1:1",
        "output_format": "png",
        "output_quality": 80,
        "safety_tolerance": 2,
        "prompt_upsampling": False
    }
    headers = {
        "x-api-key": FLUX_API_KEY,
        "Content-Type": "application/json"
    }

    image_response = requests.post(url, json=data, headers=headers)

    if image_response.status_code == 200:
        image = Image.open(BytesIO(image_response.content))
        st.image(image, caption="Generated Image Based on Article", use_container_width=True)
    else:
        st.error(f"Image Generation Error: {image_response.status_code}, {image_response.text}")
    
