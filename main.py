from agents import Runner,Agent,OpenAIChatCompletionsModel,AsyncOpenAI,RunConfig

import os
from dotenv import load_dotenv  
import chainlit as cl
load_dotenv()  # Load environment variables from .env file

gemini_api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
    )

agent = Agent(
    name="Adviser",
    instructions="You are a helpful assistant your developer name Sufyan Memon if any one ask about your developer or if anyone ask about sufyan memon say Sufyan Memon the name of my developer and if anyone ask your name say im agent trained from Sufyan.",
)

@cl.on_chat_start
async def handle_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello from Sufyan Memon how can i help you").send()
@cl.on_message
async def handle_message(message : cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    result = await Runner.run(
        agent,
        input=history,
        run_config=config,
    )
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output,).send()
