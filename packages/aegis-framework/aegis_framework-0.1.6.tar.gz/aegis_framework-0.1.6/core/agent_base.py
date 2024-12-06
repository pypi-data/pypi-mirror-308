import abc

class BaseAgent(abc.ABC):
    """
    Base class for all agents in the Aegis Framework.
    This class serves as an abstract base class that enforces the implementation
    of the run_task method, which each derived agent must define.
    """

    def __init__(self, name):
        self.name = name
        self.status = "Idle"
    
    @abc.abstractmethod
    def run_task(self, task, *args, **kwargs):
        """
        Abstract method that must be implemented by all subclasses.
        This method defines how the agent processes tasks.

        Args:
            task (str): The task or input to be processed by the agent.
            *args: Additional positional arguments for specific tasks.
            **kwargs: Additional keyword arguments for specific tasks.

        Returns:
            str: The result or output of the task.
        """
        pass

    def update_status(self, status):
        """
        Update the status of the agent.

        Args:
            status (str): The new status of the agent.
        """
        self.status = status
        print(f"[{self.name}] Status updated to: {self.status}")

    def log_activity(self, message):
        """
        Log an activity or message from the agent.

        Args:
            message (str): The message to log.
        """
        print(f"[{self.name}] Activity Log: {message}")
