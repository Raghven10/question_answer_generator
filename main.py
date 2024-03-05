import fitz  # PyMuPDF
import csv23
import sys
import ollama # We will user local ollama api here


# Function to extract text from PDF paragraph wise
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
   
    print("stareted extarcting text")
    print("No of pages: ", len(doc))
    for page in doc:
        # print(page.get_text())
        text += page.get_text()
        #print("extracted text: ", text)
    return text.split("\n\n")  # Split text into paragraphs

def extract_final_paragraphs(paragraphs):
    final_paragraphs = []
    for paragraph in paragraphs:
        if len(paragraph) >= 100 :
            final_paragraphs.append(paragraph)
    return final_paragraphs


# Function to generate questions using GPT-3
def generate_questions(paragraphs):
    print("stareted generating questions")
    questions_answers = []
    print("No of Paragraphs: ",len(paragraphs))
    for paragraph in paragraphs:
        print("Paragraph: ", paragraph)
        print("Length:", len(paragraph))
        if len(paragraph) >= 100:
            prompt = f"""
            You are an question assistant and your job is to generate questions based on given paragraphs.
            Do not include anything except generated question.
            Do not mention here is the question.
            Generate questions for the following paragraph:\n\n{paragraph}\n\nQuestion:"""
            
            response = ollama.generate(
                model="llama2:latest",  # You can change the engine to other variants if needed
                stream= False,
                prompt=prompt,
                format="json"
            )
            print("Generated question: {}".format(response.response))
            questions_answers.append({"paragraph": paragraph, "questions": response['response']})
    return questions_answers

# Function to save questions and answers to CSV
def save_to_csv(data, filename):
    print("stareted saving text")
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv23.DictWriter(file, fieldnames=["paragraph", "questions"])
        writer.writeheader()
        writer.writerows(data)

# Main function
def main(pdf_path, output_csv):
    print("stareted main")
    paragraphs = extract_text_from_pdf(pdf_path)
    final_paragraphs = extract_final_paragraphs(paragraphs)
    questions_answers = generate_questions(final_paragraphs)
    save_to_csv(questions_answers, output_csv)

# Example usage
if __name__ == "__main__":
    pdf_path = "DAP 2020 13 Apr 2022.pdf"
    output_csv = "question_answers.csv"
    main(pdf_path, output_csv)
