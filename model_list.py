import google.generativeai as genai
genai.configure(api_key="AIzaSyC2CmC3UpnGy0QIx8Ebz0x8YqdBktBNfmU")
models = list(genai.list_models())

# Print available models
for model in models:
    print(model.name)