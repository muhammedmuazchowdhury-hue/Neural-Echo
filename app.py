import streamlit as st
import assemblyai as aai
import os
import tempfile

# Page Configuration
st.set_page_config(page_title="AssemblyAI Voice Agent", page_icon="🎙️")

st.title("🎙️ AssemblyAI Voice-to-Text Prototype")
st.write("Upload an audio file to transcribe it using AssemblyAI.")

# Retrieve API Key (Streamlit Secrets -> Environment Variable -> Sidebar Input)
api_key = None

if "ASSEMBLYAI_API_KEY" in st.secrets:
    api_key = st.secrets["ASSEMBLYAI_API_KEY"]
elif os.environ.get("ASSEMBLYAI_API_KEY"):
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")

# Fallback to sidebar input if API key is not set in environment/secrets
if not api_key:
    api_key = st.sidebar.text_input("AssemblyAI API Key", type="password")
    st.sidebar.info("Enter your AssemblyAI API Key or set it in Streamlit Secrets.")

if api_key:
    aai.settings.api_key = api_key

# Audio File Uploader
uploaded_file = st.file_uploader("Select an audio file (MP3, WAV, M4A, OGG)", type=["mp3", "wav", "m4a", "ogg"])

if uploaded_file is not None:
    # Display Audio Player
    st.audio(uploaded_file)
    
    if st.button("Transcribe Audio"):
        if not api_key:
            st.error("⚠️ AssemblyAI API Key is required to transcribe!")
        else:
            with st.spinner("Processing audio with AssemblyAI..."):
                # Save uploaded file to a temporary location
                file_extension = uploaded_file.name.split(".")[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                try:
                    # Transcribe using AssemblyAI SDK
                    transcriber = aai.Transcriber()
                    transcript = transcriber.transcribe(tmp_path)

                    if transcript.status == aai.TranscriptStatus.error:
                        st.error(f"Error: {transcript.error}")
                    else:
                        st.success("Transcription completed successfully!")
                        st.subheader("Transcribed Text:")
                        st.write(transcript.text)
                except Exception as e:
                    st.error(f"Processing failed: {e}")
                finally:
                    # Cleanup temporary file
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)