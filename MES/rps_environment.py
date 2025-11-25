from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import logging
import random

EXPERIMENT = "rock_paper_scissors"

@directive_enabled_class
class rps_environment(Environment):
    
    def __init__(self):
        self.num_rounds = 5
        self.current_round = 0
        self.institution_address = None
        
    @directive_decorator("start_environment")
    def start_environment(self, message: Message):
        """Initialize the experiment"""
        self.log_message("=" * 50)
        self.log_message("STARTING ROCK PAPER SCISSORS EXPERIMENT")
        self.log_message("=" * 50)
        
        # Get configuration properties
        self.num_rounds = self.get_property("num_rounds")
        self.institution_address = self.get_property("institution_address")
        
        self.log_message(f"Number of rounds: {self.num_rounds}")
        
        # Start the first round
        self.current_round = 1
        self.start_round()
        
    def start_round(self):
        """Start a new round"""
        self.log_message(f"\n--- ROUND {self.current_round} STARTING ---")
        
        # Send message to institution to start the round
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("start_round")
        new_message.set_payload({
            "round_number": self.current_round,
            "total_rounds": self.num_rounds
        })
        
        self.send(self.institution_address, new_message)
        
    @directive_decorator("round_complete")
    def round_complete(self, message: Message):
        """Handle round completion"""
        payload = message.get_payload()
        self.log_message(f"Round {self.current_round} complete!")
        self.log_message(f"Winner: {payload.get('winner', 'TIE')}")
        
        # Check if experiment is done
        if self.current_round >= self.num_rounds:
            self.log_message("\n" + "=" * 50)
            self.log_message("EXPERIMENT COMPLETE!")
            self.log_message("=" * 50)
            
            # Send completion message to institution
            new_message = Message()
            new_message.set_sender(self.myAddress)
            new_message.set_directive("experiment_complete")
            new_message.set_payload({})
            self.send(self.institution_address, new_message)
        else:
            # Start next round
            self.current_round += 1
            self.start_round()