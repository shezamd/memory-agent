from dotenv import load_dotenv
load_dotenv()

from graph import agent
import memory


def main():
    print("Memory Agent — remembers across sessions")
    print("Commands: 'memories' | 'forget' | 'quit'\n")

    user_id = input("What's your name? ").strip()
    if not user_id:
        user_id = "default"
    print(f"\nHey {user_id}! Start chatting.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Bye!")
            break

        if user_input.lower() == "memories":
            all_memories = memory.get_all(user_id)
            if not all_memories:
                print("\nNo memories stored yet.\n")
            else:
                print(f"\n--- {len(all_memories)} memories ---")
                for m in all_memories:
                    print(f"  - {m['memory']}")
                print()
            continue

        if user_input.lower() == "forget":
            memory.delete_all(user_id)
            print("\nAll memories cleared.\n")
            continue

        result = agent.invoke({
            "user_input": user_input,
            "memories": "",
            "response": "",
            "user_id": user_id,
        })

        print(f"\nAssistant: {result['response']}\n")


if __name__ == "__main__":
    main()
