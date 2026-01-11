# llm-travel-agent
A travel agent that can help you with building travel itineraries catering to your specific interests.

## Motivation
I am an avid traveller and AI enthusiast. I like to plan my travels diligently and detailed. This app is something I built to help with my personal travel plans, and making it open-source hoping that others could use this as well.

- If you like this, and have some add-ons or improvement ideas, please feel free to check this out, change and create a pull request. I would absoultely appreciate your contributions.

## Tags
- [Streamlit](https://docs.streamlit.io/develop/api-reference/widgets)
- FastAPI
- [HuggingFace](https://huggingface.co/)
- [MistralAI](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)

## How to use this app?

### 1. Set up

- Create an account with HuggingFace if not already
- Go to Access Token in Settings and Create a new token here: https://huggingface.co/settings/tokens
- Copy the token and set it as environment variable. For Mac:
    ```bash
    export HF_TOKEN=<token>
    source ~/.zshrc
    ```

### 2. Launch the app
```
# Run the backend server
uvicorn planner:app --reload

# In a separate terminal, run the frontend
streamlit run form.py
```

### 3. Run the app
In your browser, open `localhost:8501` to naviagte to AI Travel Planner
- See a demo here:
![Demo](demo_video.webm)

### 3. Customizations
- If you want to use another model, check for more models in [HuggingFace models](https://huggingface.co/models)
- Check if it requires access and apply for same. You can manage all model accesses in HuggingFace [here](https://huggingface.co/settings/gated-repos)
- Once finalized, update the [planner.py](planner.py) file with the model id.
- You can also tune the `max_tokens` and `temperature` as per your requirements