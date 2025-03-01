import openai
import time

# Define the API key for accessing OpenAI's services
api_key = ""

# Initialize the OpenAI client with the API key and a custom base URL
client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.chatanywhere.org/v1"
)

# Define a function to generate a summary of a news article
def get_summary(url, title, article):
    # Create a prompt for the AI model to generate a concise news summary
    prompt = f'''
        以下是一篇新聞文章。請為這篇新聞寫一份簡短的摘要，包含一個標題以及一段約2個段落的內容，每個段落最後幫我加上 "<br />" 符號。
        請在標題的前後分別用一個 "#" 括起來，並在標題後面加上一個 "#" 以及一個換行符號。
        目標是使新聞文章更為簡潔並易於理解，以便沒有太多時間的人能夠快速掌握主要內容。
        文章標題如下：
        {title}
        文章如下：
        {article}
    '''

    # Send the request to OpenAI's chat model and receive the response
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Specify the AI model to use
        messages=[
            {"role": "system", "content": "You are a journalist writing a news article."},  # System prompt for AI behavior
            {"role": "user", "content": prompt}  # User input containing the article details
        ],
        max_tokens=1000,  # Limit the length of the response
        temperature=0.2  # Set a low temperature for more deterministic responses
    )

    # Extract the content of the response
    res = response.choices[0].message.content

    # Split the response into the title and article content, removing any extra spaces
    res_title, res_article = [i.strip() for i in res.split('#') if i]

    # Return the original URL, generated title, and summarized article content
    return (url, res_title, res_article)
