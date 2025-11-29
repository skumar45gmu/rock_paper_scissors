from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import logging

EXPERIMENT = "rock_paper_scissors"

@directive_enabled_class
class rps_institution(Institution):
    
    def __init__(self):
        self.current_round = 0
        self.choices = {}  # Store agent choices {agent_address: choice}
        self.agent_addresses = []
        self.environment_address = None
        
        # Track overall results
        self.human_wins = 0
        self.computer_wins = 0
        self.ties = 0
        
    @directive_decorator("start_round")
    def start_round(self, message: Message):
        """Start a new round - request choices from agents"""
        payload = message.get_payload()
        self.current_round = payload.get("round_number")
        self.total_rounds = payload.get("total_rounds")
        self.environment_address = message.get_sender()
        
        self.log_message(f"\n[INSTITUTION] Starting Round {self.current_round}")
        
        # Clear choices from previous round
        self.choices = {}
        
        # Get all agent addresses
        self.agent_addresses = self.address_book.select_addresses(
            {"component_class": "agent"}
        )
        
        self.log_message(f"[INSTITUTION] Found {len(self.agent_addresses)} agents")
        
        # Request choices from all agents
        for agent_address in self.agent_addresses:
            new_message = Message()
            new_message.set_sender(self.myAddress)
            new_message.set_directive("request_choice")
            new_message.set_payload({
                "round_number": self.current_round,
                "total_rounds": self.total_rounds
            })
            self.send(agent_address, new_message)
            
    @directive_decorator("submit_choice")
    def submit_choice(self, message: Message):
        """Receive choice from an agent"""
        payload = message.get_payload()
        agent_address = message.get_sender()
        choice = payload.get("choice")
        agent_type = payload.get("agent_type")
        
        self.log_message(f"[INSTITUTION] Received choice from {agent_type}: {choice}")
        
        # Store the choice
        self.choices[agent_address] = {
            "choice": choice,
            "agent_type": agent_type
        }
        
        # Check if all agents have submitted
        if len(self.choices) == len(self.agent_addresses):
            self.process_round()
            
    def process_round(self):
        """Determine winner and send results"""
        self.log_message(f"[INSTITUTION] Processing round {self.current_round}")
        
        # Extract choices
        human_choice = None
        computer_choice = None
        human_address = None
        computer_address = None
        
        for address, data in self.choices.items():
            if data["agent_type"] == "human":
                human_choice = data["choice"]
                human_address = address
            elif data["agent_type"] == "computer":
                computer_choice = data["choice"]
                computer_address = address
                
        self.log_message(f"[INSTITUTION] Human chose: {human_choice}")
        self.log_message(f"[INSTITUTION] Computer chose: {computer_choice}")
        
        # Determine winner
        winner = self.determine_winner(human_choice, computer_choice)
        
        # Update overall statistics
        if winner == "human":
            self.human_wins += 1
        elif winner == "computer":
            self.computer_wins += 1
        else:
            self.ties += 1
            
        self.log_message(f"[INSTITUTION] Winner: {winner}")
        self.log_message(f"[INSTITUTION] Overall - Human: {self.human_wins}, Computer: {self.computer_wins}, Ties: {self.ties}")
        
        # Send results to both agents
        result_payload = {
            "round_number": self.current_round,
            "human_choice": human_choice,
            "computer_choice": computer_choice,
            "winner": winner,
            "human_wins": self.human_wins,
            "computer_wins": self.computer_wins,
            "ties": self.ties
        }
        
        # Send to human agent
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("round_result")
        new_message.set_payload(result_payload)
        self.send(human_address, new_message)
        
        # Send to computer agent
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("round_result")
        new_message.set_payload(result_payload)
        self.send(computer_address, new_message)
        
        # Notify environment that round is complete
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("round_complete")
        new_message.set_payload(result_payload)
        self.send(self.environment_address, new_message)
        
    def determine_winner(self, human_choice, computer_choice):
        """Determine the winner based on choices"""
        if human_choice == computer_choice:
            return "tie"
        
        winning_combinations = {
            ("rock", "scissors"),
            ("paper", "rock"),
            ("scissors", "paper")
        }
        
        if (human_choice, computer_choice) in winning_combinations:
            return "human"
        else:
            return "computer"
            
    @directive_decorator("experiment_complete")
    def experiment_complete(self, message: Message):
        """Handle experiment completion"""
        self.log_message("\n[INSTITUTION] Experiment Complete!")
        self.log_message(f"Final Results:")
        self.log_message(f"  Human Wins: {self.human_wins}")
        self.log_message(f"  Computer Wins: {self.computer_wins}")
        self.log_message(f"  Ties: {self.ties}")
        
        # Send final results to agents
        final_payload = {
            "experiment_complete": True,
            "human_wins": self.human_wins,
            "computer_wins": self.computer_wins,
            "ties": self.ties
        }
        
        for agent_address in self.agent_addresses:
            new_message = Message()
            new_message.set_sender(self.myAddress)
            new_message.set_directive("experiment_complete")
            new_message.set_payload(final_payload)
            self.send(agent_address, new_message)