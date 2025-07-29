async def get_response(human_input: str) -> str:
    from openai import OpenAI
    import os
    import base64


    def encode_image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    # Read and encode the image
    image_path = "app/uploaded/1708971797430.png"
    base64_image = encode_image_to_base64(image_path)
    data_url = f"data:image/jpeg;base64,{base64_image}"

    try:
        OPEROUTER_API_KEY = os.environ.get("OPENROUTER_KEY")
    except:
        return "Sorry. Something went wrong with getting response from LLM (API key required)"

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPEROUTER_API_KEY,
        )
        # For dev purposes override the uni prompts
        systemPrompt = "Output text in markdown format"
        developerPrompt = "Be yourself"
        message = [
            {
                "type": "text",
                "text": "What's in this image?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": data_url
                }
            }
        ]
        completion = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": systemPrompt
                },
                {
                    "role": "developer",
                    "content": developerPrompt
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        LLM_outputDICT: dict = completion.to_dict()
        LLM_output: str = LLM_outputDICT['choices'][0]['message']['content']

        return LLM_output
    except:
        return "Something went wrong with the request to the LLM. Please try again later."