import os
import time
from datetime import datetime
import subprocess
import threading
import schedule

from aegis_framework.core.agent_base import BaseAgent
from aegis_framework.core.ollama_model import OllamaLocalModel

class DesignAgent(BaseAgent):
    """
    An agent responsible for designing new agents or modules that contribute to the overarching mission.
    """

    AGENT_DIRECTORY = "agent_designs"

    def __init__(self):
        super().__init__(name="DesignAgent")
        self.ollama_model = OllamaLocalModel(model="gemma2:9b")  # Replace or set dynamically if needed
        self.ensure_agent_directory()

    def ensure_agent_directory(self):
        """Ensure the directory for saving agent designs exists."""
        if not os.path.exists(self.AGENT_DIRECTORY):
            os.makedirs(self.AGENT_DIRECTORY)

    def run_task(self, task, *args, **kwargs):
        """Generates and saves agent designs based on a given task."""
        self.update_status("Running")
        self.log_activity(f"Received task: {task}")

        agent_code = self.generate_agent_code()
        additional_insights = self.ollama_model.invoke(
            f"Please generate a detailed design and Python code for an autonomous agent that contributes to a mission based on: {task}."
        )

        design_content = self.format_agent_code(agent_code, additional_insights)
        file_path = self.save_agent_to_file(design_content)

        self.update_status("Idle")
        return (
            f"Agent design created and saved successfully!\n"
            f"File Location: {file_path}\n"
            f"Additional Insights: {additional_insights}\n"
        )

    def generate_agent_code(self):
        """Generate example agent code."""
        class_name = "ColonyAgent"
        code = (
            f"# colony_agent.py\n\n"
            f"import time\n"
            f"import threading\n"
            f"import schedule\n"
            f"import subprocess\n\n"
            f"class {class_name}:\n"
            f"    def __init__(self):\n"
            f"        self.active = True\n"
            f"        self.setup_tasks()\n\n"
            f"    def setup_tasks(self):\n"
            f"        schedule.every(10).minutes.do(self.contribute_to_mission)\n\n"
            f"    def run(self):\n"
            f"        while self.active:\n"
            f"            schedule.run_pending()\n"
            f"            time.sleep(1)\n\n"
            f"    def stop(self):\n"
            f"        self.active = False\n\n"
            f"    def contribute_to_mission(self):\n"
            f"        print('Contributing to mission...')\n"
        )
        code += (
            "\nif __name__ == '__main__':\n"
            f"    agent = {class_name}()\n"
            "    agent_thread = threading.Thread(target=agent.run)\n"
            "    agent_thread.start()\n"
            "    try:\n"
            "        while True:\n"
            "            time.sleep(1)\n"
            "    except KeyboardInterrupt:\n"
            "        agent.stop()\n"
            "        agent_thread.join()\n"
            "        print('Agent has been stopped.')\n"
        )
        return code

    def format_agent_code(self, code, additional_insights):
        """Format agent code and design details for saving."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = (
            f"# Agent Design\n"
            f"**Generated on**: {current_time}\n\n"
            f"## Agent Code\n\n"
            f"{code}\n\n"
            f"## Additional Insights from LLM\n\n"
            f"{additional_insights}\n"
        )
        return content

    def save_agent_to_file(self, content):
        """Save the generated agent content to a markdown file."""
        file_name = f"colony_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        file_path = os.path.join(self.AGENT_DIRECTORY, file_name)
        with open(file_path, "w") as file:
            file.write(content)
        return file_path
