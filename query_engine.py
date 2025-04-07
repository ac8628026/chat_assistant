from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import CSVLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# path for insurance sources 

file_paths = [
    "./sources/insurance/America's_Choice_2500_Gold_SOB (1) (1).pdf",
    "./sources/insurance/America's_Choice_5000_Bronze_SOB (2).pdf",
    "./sources/insurance/America's_Choice_5000_HSA_SOB (2).pdf",
    "./sources/insurance/America's_Choice_7350_Copper_SOB (1) (1).pdf",
]

doc_file_paths = [
    "./sources/insurance/America's_Choice_Medical_Questions_-_Modified_(3) (1).docx",
]

angelone_file_paths = [
    "./sources/angelone/angelone_faqs/Add_and_Withdraw_Funds.csv",
    "./sources/angelone/angelone_faqs/Angel_One_Recommendations.csv",
    "./sources/angelone/angelone_faqs/Charges_and_Cashbacks.csv",
    "./sources/angelone/angelone_faqs/Charts.csv",
    "./sources/angelone/angelone_faqs/Compliance.csv",
    "./sources/angelone/angelone_faqs/Fixed_Deposits.csv",
    "./sources/angelone/angelone_faqs/IPO_&_OFS.csv",
    "./sources/angelone/angelone_faqs/Loans.csv",
    "./sources/angelone/angelone_faqs/Margin_Pledging_and_Margin_Trading.csv",
    "./sources/angelone/angelone_faqs/Mutual_Funds.csv",
    "./sources/angelone/angelone_faqs/Portfolio_and_Corporate_Actions.csv",
    "./sources/angelone/angelone_faqs/Reports_and_Statements.csv",
    "./sources/angelone/angelone_faqs/Your_Account.csv",
    "./sources/angelone/angelone_faqs/Your_Orders.csv",
]

all_contents = []   # to store all documents contents in a list ( unique format)

#load all insurace documents contents in all_contents list
for file in file_paths:
    loader = PyPDFLoader(file)
    # print(f"Loading file: {file} loader: {loader}")
    doc = loader.load()
    # print(f"doc: {doc}")
    all_contents.extend(doc)

for file in doc_file_paths:
    loader = UnstructuredWordDocumentLoader(file)
    # print(f"Loading file: {file} loader: {loader}")
    doc = loader.load()
    # print(f"doc: {doc}")
    all_contents.extend(doc)

for file in angelone_file_paths:
    loader = CSVLoader(file, encoding="utf-8")
    # print(f"Loading file: {file} loader: {loader}")
    doc = loader.load()
    # print(f"doc: {doc}")
    all_contents.extend(doc)
    

# config for text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 100,
    separators=["\n\n", "\n", " ", "","."],
)

#spliting all_contents list into smaller chunks chunk_docs list
chunk_docs = text_splitter.split_documents(all_contents)
# print(f"total original docs: {len(all_contents)}")
# print(f"total chunked docs: {len(chunk_docs)}")

# embedding model 
embedding_model = GoogleGenerativeAIEmbeddings(model ="models/embedding-001",google_api_key=GOOGLE_API_KEY)
# embedding the chunks
embedded_chunks = FAISS.from_documents(chunk_docs, embedding_model)
# save the vector store to disk
embedded_chunks.save_local("embedded_chunks")

# load the vector store from disk
embedded_chunks = FAISS.load_local("embedded_chunks", embedding_model, allow_dangerous_deserialization=True)



query = "What PSM Health Plan?"
# manually search and send the query to the model
#embed the query
embedded_query = embedding_model.embed_query(query)
# print(f"embedded query: {embedded_query}")
top_matched_chunks = embedded_chunks.similarity_search_by_vector(embedded_query, k=3) # get top 3 matched chunks
# print(f"top matched chunks: {top_matched_chunks[0].page_content}")

final_source = "\n\n".join([chunk.page_content for chunk in top_matched_chunks])   # join all 3 chunks to make a single string
# print(f"final source: {final_source}")
final_prompt = f"Use only this info and give response and if not found any response give response 'I don't know':\n{final_source}\n\nQ: {query}\nA:"

llm = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="gemini-1.5-flash")

response = llm.invoke(final_prompt)


print(f"Response: {response.content}")



















