from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from openai import AsyncOpenAI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Instantiate the AsyncOpenAI client
client = AsyncOpenAI()
app = FastAPI()

# Define Pydantic model for the request body
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask-question/")
async def get_medical_answer(request: QuestionRequest):
    try:
        question = request.question  # Extract the question from the request

        # Perform the chat completion asynchronously using AsyncOpenAI
        completion = await client.chat.completions.create(
            model="gpt-4o-mini",  # Use the correct model
            messages=[{"role": "system", "content": "You are a medical expert, only answer medical questions in english."},
                      {"role": "user", "content": f"{question}"}]
        )
        

        # Print the full response for debugging
        print(completion)

        # Extract the answer
        answer = completion.choices[0].message.content # Corrected access method

        # Print the answer to check if it's correct
        print(f"Answer: {answer}")

        # Check if the response is too generic or out of scope
        if "I'm sorry" in answer or "I cannot answer" in answer:
            return {"message": "This is outside of the scope of my expertise. I can only answer medical-related questions."}
        
        # Return the response
        return JSONResponse(content={"answer": answer}, headers={"Content-Type": "application/json; charset=utf-8"})

    except Exception as e:
        print(f"Error details: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")
   
