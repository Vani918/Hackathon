For the working of the project you need to have the document either in the form of text docx or pdf where you need to enter the prompt for example I want to create a speech on the topic "write the topic on which you want to create the speech" And save it locally after running the programme you can upload the file in the upload page

You need to instal the necessary packages like flask, pdf plumber ,Docx ,Google generative AI

File folder format
ai_speech_writer/ # Root project folder
│── app.py # Main Flask application
│── requirements.txt # List of dependencies
│── .env # (Optional) Environment variables for API keys
│── templates/ # HTML Templates (Front-end)
│ │── index.html # Upload page
│ │── result.html # Result page with AI-generated speech/lecture
