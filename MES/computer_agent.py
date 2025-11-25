from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import logging
import random

EXPERIMENT = "rock_paper_scissors"

@directive_enabled_class
class computer_agent(Agent):
    
    def __init__(self):
        self.agent_type = "computer"
        self.institution_address = None
        self.current_round = 0
        
    @directive_decorator("request_choice")
    def request_choice(self, message: Message):
        """Institution is requesting a choice for this round"""
        payload = message.get_payload()
        self.current_round = payload.get("round_number")
        self.institution_address = message.get_sender()
        
        self.log_message(f"[COMPUTER] Received request for round {self.current_round}")
        
        # Make random choice
        choices = ["rock", "paper", "scissors"]
        choice = random.choice(choices)
        
        self.log_message(f"[COMPUTER] Chose: {choice}")
        
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
        winner = payload.get("winner")
        
        self.log_message(f"[COMPUTER] Round {round_number} result: {winner}")
        
    @directive_decorator("experiment_complete")
    def experiment_complete(self, message: Message):
        """Handle experiment completion"""
        self.log_message("[COMPUTER] Experiment complete!")