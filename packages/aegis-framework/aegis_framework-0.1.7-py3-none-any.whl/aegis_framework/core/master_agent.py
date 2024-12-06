import os
from aegis.design_agent import DesignsAgent
from aegis.default_llm import OllamaLocalModel  # Import your default LLM implementation

class MasterAIAgent:
    def __init__(self, llm_instance=None):
        """
        Initialize the Master Agent.
        
        Args:
            llm_instance: An instance of an LLM-compatible class (e.g., OllamaLocalModel).
        """
        self.llm = llm_instance if llm_instance else OllamaLocalModel()  # Default to OllamaLocalModel if no LLM provided
        self.agents = {}
        self._init_agents()

    def _init_agents(self):
        """Initialize and manage agents within the framework."""
        # Example: Initialize the DesignsAgent with a default mission
        self.agents['designs_agent'] = DesignsAgent(
            mission="Enhance AI capabilities through collaborative designs",
            llm_instance=self.llm
        )

    def execute_agent_task(self, agent_name, *args, **kwargs):
        """
        Execute a task for the specified agent.
        
        Args:
            agent_name (str): The name of the agent to execute a task for.
            *args: Positional arguments to pass to the agent.
            **kwargs: Keyword arguments to pass to the agent.
        
        Returns:
            str: The result of the agent's task execution.
        """
        agent = self.agents.get(agent_name)
        if agent:
            try:
                return agent.generate_design()  # High-level task execution
            except Exception as e:
                return f"Error executing task for agent '{agent_name}': {str(e)}"
        return f"No agent named '{agent_name}' found."

    def list_agents(self):
        """List all available agents managed by the Master Agent."""
        return list(self.agents.keys())

if __name__ == "__main__":
    # Example usage
    master_agent = MasterAIAgent()
    print("Available agents:", master_agent.list_agents())
    print(master_agent.execute_agent_task('designs_agent'))
