import streamlit as st
import google.generativeai as genai

# Access the API key from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]

# Configure the Gemini 1.5 Pro model with the API key
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Set page config with title and favicon
st.set_page_config(
    page_title="GeminiDriveMate 🚗✨",
    page_icon="✨🚗✨",
)

# Add custom CSS for styling
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #001F54;  /* Deep blue for sidebar */
    }
    .stButton>button {
        color: #FFFFFF;
        background-color: #0066CC;  /* Bright blue for buttons */
        border-radius: 5px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #3399FF;  /* Lighter blue on hover */
    }
    .stChatMessage--assistant {
        background-color: #E0F7FA;  /* Light cyan for assistant messages */
    }
    .stChatMessage--user {
        background-color: #B3E5FC;  /* Light blue for user messages */
    }
    .title {
        color: #EE204E;
        font-family: 'Arial Black', Gadget, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.write("""
**GeminiDriveMate** is your intelligent assistant for diagnosing vehicle issues. Powered by advanced AI technology, GeminiDriveMate helps you troubleshoot problems by providing detailed insights and potential solutions. Whether you have a Nissan, Ford, Toyota, or any other vehicle, GeminiDriveMate is here to assist you.
""")

st.sidebar.header("How to Use GeminiDriveMate")
st.sidebar.write("""
1. **Enter Your Vehicle Information**:
   - Provide the vehicle company, model, and year.
   - Describe the issue or fault you are experiencing with your vehicle.

2. **Submit the Information**:
   - Use the input field at the bottom of the page to enter the required details.

3. **Get a Response**:
   - GeminiDriveMate will process your input and generate a detailed response with possible causes and solutions for the issue.

4. **Review and Take Action**:
   - Read the response provided by GeminiDriveMate and follow the suggested steps to address the vehicle issue.
   - If necessary, consult with a professional mechanic for further assistance.
""")
st.sidebar.markdown("### Social Links:")
st.sidebar.write("🔗 [GitHub](https://www.github.com)")

# Show title and description.
st.markdown('<h1 class="title">GeminiDriveMate 🚗✨</h1>', unsafe_allow_html=True)
st.write(
    "This is your GeminiDriveMate that uses the Gemini 1.5 Pro model to generate solutions to your vehicle problems."
)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []
    instruction = "Hi! This is your GeminiDriveMate 🚗. Please mention the Vehicle Company, Model, Year, the Fault/Issue you are facing. For example; My vehicle company is Nissan, model Sentra 2000, and the issue I am facing is Fuel Pump Failure."
    st.session_state.messages.append({"role": "assistant", "content": instruction})

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is the issue you are facing with your Vehicle?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the Gemini API.
    with st.spinner("Generating response..."):
        try:
            response = model.generate_content(prompt)
            
            # Extract the content from the response
            full_response = response.text

            # Stream the full response to the chat using `st.write`
            with st.chat_message("assistant"):
                st.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"An error occurred: {e}")