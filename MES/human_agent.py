from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import logging

EXPERIMENT = "rock_paper_scissors"

@directive_enabled_class
class human_agent(Agent):
    
    def __init__(self):
        self.agent_type = "human"
        self.institution_address = None
        self.current_round = 0
        self.history = []
        
        # Overall statistics
        self.human_wins = 0
        self.computer_wins = 0
        self.ties = 0
        
    @directive_decorator("request_choice")
    def request_choice(self, message: Message):
        """Institution is requesting a choice for this round"""
        payload = message.get_payload()
        self.current_round = payload.get("round_number")
        self.total_rounds = payload.get("total_rounds")
        self.institution_address = message.get_sender()
        
        self.log_message(f"[HUMAN] Received request for round {self.current_round}")
        
        # Send UI update to enable choice buttons
        self.send_to_ui({
            "message": f"Round {self.current_round} of {self.total_rounds} - Make your choice!",
            "round": self.current_round,
            "total_rounds": self.total_rounds,
            "enable_buttons": True,
            "human_wins": self.human_wins,
            "computer_wins": self.computer_wins,
            "ties": self.ties
        })
        
    @directive_decorator("ui_action")
    def ui_action(self, message: Message):
        """Receive action from UI (user's choice)"""
        payload = message.get_payload()
        action = payload.get("action")
        
        if action == "submit_choice":
            choice = payload.get("choice")
            self.log_message(f"[HUMAN] User chose: {choice}")
            
            # Disable buttons while waiting for result
            self.send_to_ui({
                "message": "Waiting for computer's choice...",
                "enable_buttons": False
            })
            
            # Send choice to institution
            new_message = Message()
            new_message.set_sender(self.myAddress)
            new_message.set_directive("submit_choice")
            new_message.set_payload({
                "choice": choice,
                "agent_type": self.agent_type,
                "round_number": self.current_round
            })
            self.send(self.institution_address, new_message)
            
    @directive_decorator("round_result")
    def round_result(self, message: Message):
        """Receive round result from institution"""
        payload = message.get_payload()
        
        round_number = payload.get("round_number")
        human_choice = payload.get("human_choice")
        computer_choice = payload.get("computer_choice")
        winner = payload.get("winner")
        
        # Update overall statistics
        self.human_wins = payload.get("human_wins")
        self.computer_wins = payload.get("computer_wins")
        self.ties = payload.get("ties")
        
        self.log_message(f"[HUMAN] Round {round_number} result: {winner}")
        
        # Determine result text
        if winner == "human":
            result_text = "You WIN!"
        elif winner == "computer":
            result_text = "You LOSE!"
        else:
            result_text = "It's a TIE!"
            
        # Add to history
        history_entry = {
            "round": round_number,
            "your_choice": human_choice,
            "computer_choice": computer_choice,
            "result": result_text
        }
        self.history.append(history_entry)
        
        # Send result to UI
        self.send_to_ui({
            "message": f"Round {round_number} Complete! {result_text}",
            "round": round_number,
            "your_choice": human_choice,
            "computer_choice": computer_choice,
            "result": result_text,
            "human_wins": self.human_wins,
            "computer_wins": self.computer_wins,
            "ties": self.ties,
            "history": self.history,
            "enable_buttons": False
        })
        
    @directive_decorator("experiment_complete")
    def experiment_complete(self, message: Message):
        """Handle experiment completion"""
        payload = message.get_payload()
        
        self.log_message("[HUMAN] Experiment complete!")
        
        # Send final message to UI
        self.send_to_ui({
            "message": f"Game Over! Final Score - You: {self.human_wins}, Computer: {self.computer_wins}, Ties: {self.ties}",
            "experiment_complete": True,
            "human_wins": self.human_wins,
            "computer_wins": self.computer_wins,
            "ties": self.ties,
            "enable_buttons": False
        })
        
    def send_to_ui(self, data):
        """Helper method to send data to UI"""
        self.log_data(data)