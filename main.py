from src.llm_providers.openai import OpenAIProvider
from langchain_core.messages import HumanMessage
from src.graphs.graph_builder import GraphBuilder
from src.utils.logger import log_data
from langgraph.types import Command
from src.utils.graph import handle_interrupt
import os
from dotenv import load_dotenv
import questionary
import textwrap

# Load environment variables
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"

graph_builder = GraphBuilder()
graph = graph_builder.compile_graph()


def run_request(user_input: str, model_provider: str, model_name: str):
    messages = [HumanMessage(content=user_input)]
    request = {"messages": messages}
    config = {"configurable": {"thread_id": "1", "user_id": "1"}}
    sections = [
        "decode_files",
        "human_feedback",
        "analyse_feedback",
        "fetch_files",
        "llm_call",
        "approved_path",
        "rejected_path",
    ]

    for chunk in graph.stream(
        request,
        config=config,
        stream_mode="updates",
        context={
            "model_provider": model_provider,
            "model_name": model_name,
        },
    ):
        log_data(chunk, sections)
        resume = handle_interrupt(graph, config, chunk)
        if resume:
            for chunk in graph.stream(
                Command(resume=resume),
                config=config,
                stream_mode="updates",
                context={
                    "model_provider": model_provider,
                    "model_name": model_name,
                },
            ):
                log_data(chunk, sections)
                resume = handle_interrupt(graph, config, chunk)
                if resume:
                    graph.invoke(
                        Command(resume=resume),
                        config=config,
                    )


def get_model_selection():
    """Get model provider and name selection from user"""
    model_provider = questionary.select(
        "Which provider do you want to use?", choices=["openai", "groq"]
    ).ask()

    if not model_provider:  # User cancelled
        return None, None

    print()

    if model_provider.lower().strip() == "openai":
        model_name = questionary.select(
            "Select OpenAI model name: ",
            choices=["gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini", "gpt-4.1"],
        ).ask()
    elif model_provider.lower().strip() == "groq":
        model_name = questionary.select(
            "Select Groq model name: ",
            choices=["llama3-8b-8192", "qwen/qwen3-32b"],  # Fixed empty choice
        ).ask()
    else:
        raise ValueError("Invalid model provider")

    if not model_name:  # User cancelled
        return None, None

    return model_provider, model_name


def main():
    """Main interactive loop"""
    # Beautiful welcome banner
    print("\n" + "═" * 70)
    print("║" + " " * 68 + "║")
    print("║" + "🤖  WELCOME TO THE AI ASSISTANT  🤖".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╠" + "═" * 68 + "╣")
    print("║" + " " * 68 + "║")
    print("║  📝 Commands:".ljust(68) + " ║")
    print("║" + "     • Type your questions naturally".ljust(68) + " ║")
    print("║" + "     • 'quit', 'exit', 'bye' → End session".ljust(68) + " ║")
    print("║" + "     • 'change model' → Switch AI model".ljust(68) + " ║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    # Initial model selection
    model_provider, model_name = get_model_selection()
    if not model_provider:
        print("No model selected. Exiting...")
        return

    # Model selection confirmation
    print("┌" + "─" * 68 + "┐")
    print(
        "│"
        + f" ✅ SELECTED MODEL: {model_provider.upper()} - {model_name.upper()}".ljust(
            68
        )
        + "│"
    )
    print("└" + "─" * 68 + "┘")

    while True:
        try:
            # Get user input
            user_input = questionary.text(
                "\n💬 Enter your query (or 'quit' to exit): "
            ).ask()

            # Handle exit conditions
            if not user_input or user_input.lower().strip() in [
                "quit",
                "exit",
                "bye",
                "q",
            ]:
                print("\n┌" + "─" * 50 + "┐")
                print(
                    "│"
                    + " 👋 GOODBYE! THANKS FOR USING AI ASSISTANT! ".center(50)
                    + "│"
                )
                print("└" + "─" * 50 + "┘")
                break

            # Handle model change
            if user_input.lower().strip() == "change model":
                print("\n🔄 Switching model configuration...")
                print("─" * 40)
                new_provider, new_model = get_model_selection()
                if new_provider and new_model:
                    model_provider, model_name = new_provider, new_model
                    print("┌" + "─" * 60 + "┐")
                    print(
                        "│"
                        + f" ✅ UPDATED TO: {model_provider.upper()} - {model_name.upper()}".ljust(
                            60
                        )
                        + "│"
                    )
                    print("└" + "─" * 60 + "┘")
                else:
                    print("┌" + "─" * 50 + "┐")
                    print(
                        "│"
                        + " ❌ SELECTION CANCELLED - KEEPING CURRENT MODEL ".center(50)
                        + "│"
                    )
                    print("└" + "─" * 50 + "┘")
                continue

            # Handle empty input
            if not user_input.strip():
                print("┌" + "─" * 40 + "┐")
                print("│" + " ❌ PLEASE ENTER A VALID QUERY ".center(40) + "│")
                print("└" + "─" * 40 + "┘")
                continue

            print(
                f"\n🚀 Processing your request with {model_provider.upper()} - {model_name.upper()}..."
            )
            print("╔" + "═" * 68 + "╗")
            print("║" + " 🔄 REQUEST IN PROGRESS... ".center(68) + "║")
            print("╚" + "═" * 68 + "╝")

            # Run the request
            run_request(user_input, model_provider, model_name)

            print("\n╔" + "═" * 68 + "╗")
            print("║" + " ✅ REQUEST COMPLETED SUCCESSFULLY! ".center(68) + "║")
            print("║" + " Ready for your next question... ".center(68) + "║")
            print("╚" + "═" * 68 + "╝")

        except KeyboardInterrupt:
            print("\n")
            print("╔" + "═" * 50 + "╗")
            print("║" + " 👋 SESSION INTERRUPTED - GOODBYE! ".center(50) + "║")
            print("╚" + "═" * 50 + "╝")
            break
        except Exception as e:
            error_msg = str(e)
            wrapped_lines = textwrap.wrap(f"❌ ERROR: {error_msg}", width=60)
            print("\n╔" + "═" * 60 + "╗")
            for line in wrapped_lines:
                print("║" + line.ljust(60) + "║")
            print("║" + " Please try again or type 'quit' to exit. ".center(60) + "║")
            print("╚" + "═" * 60 + "╝")
            continue


if __name__ == "__main__":
    main()
