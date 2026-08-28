from lifeos.domains.learning.dependencies import build_learning_service
from lifeos.domains.learning.tools import LearningTools


service = build_learning_service()
tools = LearningTools(service)

results = tools.search_learning_memory(
    "What have I learned about Arduino inputs?"
)

for memory in results:
    print(memory.title)
    print(memory.content)
    print()

service.repository.close()