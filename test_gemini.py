import google.generativeai as genai

genai.configure(api_key="AIzaSyDgSXsv5bW-jyLfgEumNqYuLSKeAR_GRbU")

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say hello")
print(response.text)
