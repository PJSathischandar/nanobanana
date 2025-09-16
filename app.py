# app.py
import streamlit as st
from PIL import Image
from io import BytesIO

try:
    from google import genai
    from google.genai import errors  # for nicer error messages
except ImportError:
    genai = None
    errors = None

st.set_page_config(page_title="Nano Banana Chat Image Generator", layout="centered")
st.title("Nano Banana Chat Image Generator")
st.markdown("Enter a prompt below and generate an image using nano banana!")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

user_input = st.text_input("Your prompt:", "")

def make_client():
    # NEVER hardcode keys; use Streamlit secrets or env var
    # Set [Secrets] -> GEMINI_API_KEY in Streamlit Cloud or export GOOGLE_API_KEY locally
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        st.stop()
    return genai.Client(api_key=api_key)

if st.button("Generate Image") and user_input:
    image = None
    if genai is None:
        st.error("Gemini Python SDK not installed. Run: `pip install -U google-genai`")
    else:
        try:
            client = make_client()

            # Use the Developer API’s image-capable Gemini model (aka nano banana)
            # Docs example mirrors this exact call:
            # https://ai.google.dev/gemini-api/docs/image-generation
            resp = client.models.generate_content(
                model="gemini-2.5-flash-image-preview",
                contents=[user_input],
            )

            # Extract any returned images
            images = []
            cand = resp.candidates[0] if resp.candidates else None
            if cand and cand.content and cand.content.parts:
                for part in cand.content.parts:
                    if getattr(part, "text", None):
                        st.info(part.text)
                    elif getattr(part, "inline_data", None):
                        raw = part.inline_data.data  # bytes per docs
                        try:
                            img = Image.open(BytesIO(bytes(raw)))
                            images.append(img)
                        except Exception as decode_err:
                            st.error(f"Failed to decode image: {decode_err}")
            else:
                st.warning("No candidates returned. Try a different prompt.")

            image = images[0] if images else None

        except errors.APIError as e:
            # Show helpful details (status + message)
            st.error(f"Gemini API error {getattr(e, 'code', '')}: {getattr(e, 'message', e)}")
        except Exception as e:
            st.error(f"Image generation failed: {e}")

    st.session_state["chat_history"].append((user_input, image))

# Display chat history
for prompt, img in reversed(st.session_state["chat_history"]):
    st.markdown(f"**You:** {prompt}")
    if img is not None:
        st.image(img, caption="Generated Image")
    else:
        st.info("[Image will appear here once generation succeeds]")
