import streamlit as st
from random import shuffle, choice
import pandas as pd
import matplotlib.pyplot as plt
"""
# GOAL MINE

"""
if "squares" not in st.session_state:
    st.session_state.squares = [True, True, True, True, False] 
    shuffle(st.session_state.squares)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "choices" not in st.session_state:
    st.session_state.choices = []  
if "goal_step" not in st.session_state:
    st.session_state.goal_step = False  
if "goalkeeper_choice" not in st.session_state:
    st.session_state.goalkeeper_choice = None
if "show_goalkeeper_choice" not in st.session_state:
    st.session_state.show_goalkeeper_choice = False
if "simulation_results" not in st.session_state:
    st.session_state.simulation_results = {"wins": 0, "losses": 0, "total": 0}
if "simulation_history" not in st.session_state:
    st.session_state.simulation_history = []


    

st.write("Squares sequence:") 
st.write(st.session_state.squares)
if not st.session_state.goal_step:
    st.write(f"Attempt {st.session_state.attempts + 1} out of 5")
    chosen_square = st.number_input("Chose a square (0-4)", min_value=0, max_value=4, step=1)
    if st.button("Validate my answer") and st.session_state.attempts < 5:
        st.session_state.choices.append(chosen_square)
        
        if st.session_state.squares[chosen_square]:
            st.write(f"Attempt {st.session_state.attempts + 1}: You pass to the next level!")
            st.session_state.attempts += 1
            if st.session_state.attempts < 5:
                if st.session_state.attempts == 3:
                    st.session_state.squares = [True, True, True, False, False]
                    shuffle(st.session_state.squares)
                else:
                    st.session_state.squares = [True, True, True, True, False]
                    shuffle(st.session_state.squares)
        else:
            st.write(f"Attempt {st.session_state.attempts + 1}: You have been thwarted, you lost possession of the ball!")
            st.write("Press on new game if you want to start a new match")
            st.session_state.goal_step = False
    
    if st.session_state.attempts == 5:
        st.session_state.goal_step = True
        st.session_state.goalkeeper_choice = choice(["Bottom Left", "Top Left", "Center", "Bottom Right", "Top Right"])
        st.rerun()
else:
    st.write("You are in front of the goalkeeper, choose where to shoot")
    shot_options = ["Bottom Left", "Top Left", "Center", "Bottom Right", "Top Right"]
    
    
    st.session_state.show_goalkeeper_choice = st.checkbox("Show goalkeeper's choice")
    if st.session_state.show_goalkeeper_choice:
        st.write(f"Goalkeeper will dive to: {st.session_state.goalkeeper_choice}")
    
    chosen_shot = st.radio("Select your shot", shot_options)
    
    if st.button("Shoot!"):
        if chosen_shot == st.session_state.goalkeeper_choice:
            st.write(f"The goalkeeper guessed your shot ({st.session_state.goalkeeper_choice})! You missed!")
        else:
            st.write(f"Goal!!! You shot at {chosen_shot} and the goalkeeper went {st.session_state.goalkeeper_choice}!")
        
        st.session_state.goal_step = False 
        st.session_state.attempts = 0
        st.session_state.choices = []
        st.session_state.squares = [True, True, True, True, False]
        shuffle(st.session_state.squares)
if st.button("New game"):
    st.session_state.squares = [True, True, True, True, False]
    shuffle(st.session_state.squares)
    st.session_state.attempts = 0
    st.session_state.choices = []
    st.session_state.goal_step = False
    st.session_state.goalkeeper_choice = None
    st.session_state.show_goalkeeper_choice = False
    st.rerun()

"""
## Probability of winning the game
"""


def simulate_game():
   
    sim_attempts = 0
    sim_goal_step = False
    
   
    while sim_attempts < 5 and not sim_goal_step:
        sim_squares = [True, True, True, True, False]
        if sim_attempts == 3:
            sim_squares = [True, True, True, False, False]
        shuffle(sim_squares)
        
        
        sim_chosen_square = choice(range(5))
        
        if sim_squares[sim_chosen_square]:
            sim_attempts += 1
        else:
            
            return False
    
    
    if sim_attempts == 5:
        goalkeeper_choice = choice(["Bottom Left", "Top Left", "Center", "Bottom Right", "Top Right"])
        player_choice = choice(["Bottom Left", "Top Left", "Center", "Bottom Right", "Top Right"])
        
        
        return player_choice != goalkeeper_choice
    
    return False


with st.expander("Simulation Statistics"):
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Total simulations: {st.session_state.simulation_results['total']}")
        st.write(f"Wins: {st.session_state.simulation_results['wins']}")
        st.write(f"Losses: {st.session_state.simulation_results['losses']}")
        
        if st.session_state.simulation_results['total'] > 0:
            win_rate = st.session_state.simulation_results['wins'] / st.session_state.simulation_results['total'] * 100
            st.write(f"Win rate: {win_rate:.2f}%")
    
    with col2:
        if st.session_state.simulation_results['total'] > 0:
            # Creare un grafico delle probabilità
            fig, ax = plt.subplots()
            ax.pie([st.session_state.simulation_results['wins'], st.session_state.simulation_results['losses']], 
                  labels=['Wins', 'Losses'], autopct='%1.1f%%', colors=['green', 'red'])
            ax.set_title('Simulation Results')
            st.pyplot(fig)
    
    
    sim_col1, sim_col2, sim_col3 = st.columns(3)
    with sim_col1:
        if st.button("Run 1 Simulation"):
            result = simulate_game()
            st.session_state.simulation_results['total'] += 1
            if result:
                st.session_state.simulation_results['wins'] += 1
            else:
                st.session_state.simulation_results['losses'] += 1
            st.session_state.simulation_history.append(result)
            st.rerun()
    
    with sim_col2:
        if st.button("Run 100 Simulations"):
            for _ in range(100):
                result = simulate_game()
                st.session_state.simulation_results['total'] += 1
                if result:
                    st.session_state.simulation_results['wins'] += 1
                else:
                    st.session_state.simulation_results['losses'] += 1
                st.session_state.simulation_history.append(result)
            st.rerun()
    
    with sim_col3:
        if st.button("Run 1000 Simulations"):
            for _ in range(1000):
                result = simulate_game()
                st.session_state.simulation_results['total'] += 1
                if result:
                    st.session_state.simulation_results['wins'] += 1
                else:
                    st.session_state.simulation_results['losses'] += 1
                st.session_state.simulation_history.append(result)
            st.rerun()
    
    if st.button("Reset Simulation Statistics"):
        st.session_state.simulation_results = {"wins": 0, "losses": 0, "total": 0}
        st.session_state.simulation_history = []
        st.rerun()

