from pathlib import Path

from graph import Graph
from llm import LLM


INPUT_FOLDER = Path("input")
OUTPUT_FOLDER = Path("output")
OUTPUT_FILE = OUTPUT_FOLDER / "execution.log"


def write_log(file, message=""):
    print(message)
    file.write(message + "\n")


def main():
    # 1. input.txt
    INPUT_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    input_files = sorted(INPUT_FOLDER.glob("*.txt"))

    if not input_files:
        print("No input files found.")
        return

    graph = Graph()
    assistant = LLM(graph=graph)

    try:
        graph.verify_connection()

        # 8. output.txt
        with open(OUTPUT_FILE,"w",encoding="utf-8") as output_file:
            for input_file in input_files:
                write_log(output_file, f"\n=== Processing {input_file.name} ===")
                text = input_file.read_text(encoding="utf-8").strip()
                write_log(output_file, text)
    
                # 2. Ollama extrait les faits
                stored_facts = assistant.store_facts(text)
                write_log(output_file, "\nStored facts:")

                # 3. Neo4j stocke les relations
                for fact in stored_facts: 
                    write_log(output_file, str(fact))

            # 4. Ollama pose une question au graphe
            questions = [
                f"What is the capital of {input_file.stem}?"
                for input_file in input_files
            ]

            for question in questions:
                write_log(output_file, "\nQuestion:" + question)
                # 5. Neo4j retourne les faits pertinents
                result = assistant.pipeline_query(question)
        
                # 6. Ollama génère une réponse et verification
                write_log(output_file, f"Answer: {result['answer']}")
                write_log(output_file, f"Generated fact: {result['generated_fact']}")
                write_log(output_file, f"Verification: {result['verification']}")
                write_log(output_file, f"Verification_fact: {result['verification_fact']}")
                write_log(output_file, "Graph facts:")

                # 7. Neo4j vérifie symboliquement la relation
                for fact in result["graph_facts"]:
                    write_log(output_file, str(fact))

            write_log(output_file, "\nTHE END")

    except Exception as error:
        print(f"Error: {error}")

    finally:
        graph.close()


if __name__ == "__main__":
    main()
