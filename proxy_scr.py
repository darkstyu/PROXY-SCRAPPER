import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AGENTROUTER_API_KEY"),
    base_url="https://agentrouter.org/v1"
)

# Models available on your account
MODELS = {
    "1": "claude-opus-4-8",
    "2": "claude-opus-5",
    "3": "gpt-5.6-sol",
    "4": "deepseek-v4-flash",
}

def main():
    print("=== AgentRouter Console ===")
    print("Available models:")
    for k, v in MODELS.items():
        print(f"  {k}. {v}")
    
    choice = input("\nChoose model number (default 1): ").strip() or "1"
    model = MODELS.get(choice, "claude-opus-4-8")
    print(f"\nUsing: {model}")
    print("Type 'quit' or 'exit' to stop. Type 'clear' to reset conversation.\n")

    history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    while True:
        user = input("You: ").strip()
        if not user:
            continue
        if user.lower() in {"quit", "exit", "q"}:
            break
        if user.lower() == "clear":
            history = [{"role": "system", "content": "You are a helpful assistant."}]
            print("(conversation cleared)\n")
            continue

        history.append({"role": "user", "content": user})

        try:
            response = client.chat.completions.create(
                model=model,
                messages=history,
                temperature=0.7,
            )
            reply = response.choices[0].message.content
            print(f"\nAI ({model}): {reply}\n")
            history.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"\nError: {e}\n")
            # remove the failed user message so history stays clean
            history.pop()

if __name__ == "__main__":
    main()