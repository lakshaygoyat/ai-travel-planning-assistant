from __future__ import annotations

from src.assistant import TravelAssistant


def main() -> None:
    assistant = TravelAssistant()
    history: list[dict[str, str]] = []
    print("AI Travel Planning Assistant — type 'exit' to stop")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        response = assistant.ask(question, history)
        print(f"\nAssistant:\n{response.answer}")
        print(f"\nTrace: {response.trace}")
        history.extend(
            [
                {"role": "user", "content": question},
                {"role": "assistant", "content": response.answer},
            ]
        )


if __name__ == "__main__":
    main()
