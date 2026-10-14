from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

def pick_llm(level: str):
	"""
	Picks the appropriate LLM based on the provided level.

	Args:
		level (str): The level of the LLM to pick. Can be "basic", "intermediate", or "advanced".

	Returns:
		ChatOpenAI: The LLM instance to be used
	"""
	if level.lower() == "low":
		llm = ChatOpenAI(model_name="gpt-6-luna", max_tokens=1000)
	elif level.lower() == "medium":
		llm = ChatOpenAI(model_name="gpt-5.6-terra", max_tokens=1000, use_responses_api=True)
	elif level.lower() == "high":
		llm = ChatOpenAI(model_name="gpt-4-0613", temperature=0, max_tokens=1000)
	else:
		raise ValueError(f"Invalid level provided. Choose from 'basic', 'intermediate', or 'advanced'. {level}")

	return llm

# if __name__ == "__main__":
# 	llm_obj = pick_llm("low")
# 	result = llm_obj.invoke("What is the capital of France?")
# 	print(result)