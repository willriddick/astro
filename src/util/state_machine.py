import enum
from .state import State

class StateMachine:
    def __init__(self, owner: object, states: list[State]):
        self.owner = owner
        self.states: dict[enum, State] = {}
        self.add_states(states)
        self.current_state: State = states[0]
        self.previous_state: State = self.current_state
   
    def update(self):
        if self.current_state is not None:
            self.current_state.update()
    
    def switch(self, _id: enum):
        if _id not in self.states:
            raise ValueError(f'State with ID {_id} does not exist.')

        self.previous_state = self.current_state

        if self.current_state is not None:
            self.current_state.on_exit()
        
        self.current_state = self.states[_id]
        self.current_state.on_enter()
    
    def add_states(self, states: list[State]):
        for state in states:
            self.add_state(state)
    
    def add_state(self, state: State):
        if state.id in self.states:
            raise ValueError(f"State with ID {state.id} already exists.")
        self.states[state.id] = state
        state.state_machine = self
    
    def remove_state(self, _id: enum):
        if _id not in self.states:
            raise ValueError(f'State with ID {_id} does not exist.')
        del self.states[_id]
    
    def get_state(self, _id: enum) -> State:
        return self.states[_id]
    
    def get_states(self):
        return self.states.values()
    
    def get_count(self):
        return len(self.states)
