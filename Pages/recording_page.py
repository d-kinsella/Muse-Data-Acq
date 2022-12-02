from random import randint
from tkinter import *
from state_enums import *
from Pages.utils import *

# Returns page for when user has completed a session
def get_session_done_components(state):
    session_done_components = []
    text = "You have completed your session! Your results are being saved. Thank you for participating!"
    session_done_components.append(Label(text=text, font=("Arial", 25)))
    exit_button = Button(text="Exit", command=lambda: state["window"].destroy(), font=("Arial", 25))
    session_done_components.append(exit_button)
    return session_done_components

    
# Updates the state and loads the next page in sequence
def finished_prompt(state):
    if state["recording_session"]["state"] == recording_state.REST:
        state["recording_session"]["state"] = recording_state(randint(1,2))

    elif state["recording_session"]["state"] == recording_state.GO or state["recording_session"]["state"] == recording_state.STOP:
        state["recording_session"]["count"] += 1
        if state["recording_session"]["count"] >= get_sample_count():
            state["recording_session"]["state"] = recording_state.DONE
        else: 
            state["recording_session"]["state"] = recording_state.REST

    mount_page(state, get_recording_in_progress(state))


# Gets and increments the timer on the rest page
def update_countdown_timer(timer):
    old_time = int(timer.cget("text"))
    new_time = old_time - 1
    timer.configure(text = str(new_time))
    if new_time != 0:
        timer.after(1000, lambda: update_countdown_timer(timer))


# Returns sub-frame for the resting page
def get_recording_rest_components(state):
    recording_rest_components = []
    text = "You have completed prompt number " + str(state["recording_session"]["count"]) + "\n Your next prompt begins in"
    rest_text = Label(text=text, font=("Arial", 25))
    # Attach event to the header text that ends the resting stage
    rest_text.after(get_sample_period(), lambda: finished_prompt(state))
    recording_rest_components.append(rest_text)  

    timer = Label(text=str(get_sample_period()//1000), font=("Arial", 25))
    # Attach event to the timer text that updates it every second       
    timer.after(1000, lambda: update_countdown_timer(timer))
    recording_rest_components.append(timer)  
  
    return recording_rest_components


# Returns sub-frame for stop or go based on the current state, as well as start recording
def get_session_stop_go_components(state):
    if state["recording_session"]["state"] == recording_state.GO:
        prompt_label = Label(text="GO", bg="green", fg="white", font=("Arial", 300))
    
    if state["recording_session"]["state"] == recording_state.STOP:
         prompt_label = Label(text="STOP", bg="red", fg="white", font=("Arial", 300))
    
    start_sample(state)
    # Attach event to the header text that ends the sampling stage
    prompt_label.after(get_sample_period(), lambda: end_sample(state, finished_prompt))

    return [(prompt_label, {"pady": 150})]


# Returns sub-frames based on the current state
def get_recording_components(state):
    if state["recording_session"]["state"] == recording_state.REST:
        return get_recording_rest_components(state)
    elif state["recording_session"]["state"] == recording_state.DONE:
        return get_session_done_components(state)
    elif state["recording_session"]["state"] == recording_state.STOP or \
        state["recording_session"]["state"] == recording_state.GO:
        return get_session_stop_go_components(state)


# Parent frame of the recording session page
def get_recording_in_progress(state):
    state["render_state"] = render_state.SESSION_IN_PROGRESS
    recording_in_progress_components = []
    title = Label(text="Muse OSC Interface", font=("Arial", 48))
    ip_info = Label(text="Set the Server IP in Mind Monitor to " + state["ip"], font=("Arial", 25))
    id_info = Label(text="Recording session for " + state["recording_session"]["user"], font=("Arial", 18))

    recording_in_progress_components.append((title, {"pady": 5}))
    recording_in_progress_components.append(ip_info)
    recording_in_progress_components.append((id_info, {"pady": 5}))

    recording_components = get_recording_components(state)
    recording_in_progress_components += recording_components
    return recording_in_progress_components