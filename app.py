import streamlit as st
import json
import requests
from typing import List
from help_dict import helper

request_url = 'https://gruhit13-quote-generator-backend.hf.space'
# request_url = 'http://127.0.0.1:8000'
tags_file = 'https://huggingface.co/gruhit13/quote-generator-v2/raw/main/tags.txt'

# Main title of the page
st.title('Quote Generator 🤖')

# a row for containing the text_input and submit button
input_container = st.columns([0.7, 0.3])

# Display the tags that are selected
input_container[0].text_area(
    label='Tags', 
    key='tags_input',
    placeholder="Selects tags to generate quote", 
    disabled=True, 
    help="Select tags to add it here", 
    label_visibility="collapsed")


# When the button is clicked then make an API call
def get_quote():
    tags = st.session_state['tags_input']
    global request_url

    payload = {
        'tags' : st.session_state['tags_input'],
        'max_new_tokens': st.session_state['max_new_token_length'],
        'num_beams': st.session_state['num_beams'],
        'top_k': st.session_state['top_k'],
        'top_p': st.session_state['top_p'],
        'temperature': st.session_state['temperature'],
        'do_sample': st.session_state['do_sample']
    }

    with st.spinner("🤖 is generating quote for you..."):
        response = requests.post(
            request_url+'/generate_quote',
            json = payload,
            headers={
                'Content-type': 'application/json',
                'Authorization': f"Bearer {st.secrets['API_KEY']}"
            }
        )
        
        # Get content from response and convert it to json
        response_data = json.loads(response._content.decode('UTF-8'))
        
        # if there is an error then print the reason for error
        if response.status_code == 401:
            st.write(f":red[{response_data['detail']}!!!]")
            return

        # The response would be <startoftext>tags<bot>:AI response
        # so we just need to take the AI respones
        st.session_state['quote'] = response_data['quote'].split('<bot>:')[-1]


input_container[1].button(
    label='Get Quote',
    key='submit_btn',
    use_container_width=True,
    on_click=get_quote
)

st.divider()

# List of the tags that are selected
def get_tags() -> List[str]:
    req = requests.get(tags_file)

    tags_list = req._content.decode('UTF-8').split('\n')
    tags_list.sort()
    
    return tags_list

# Get the tags from the text file on github
tags_list = get_tags()
tags_dict = {}

# Generate a dictonary from the tags list
for tag in tags_list:
    tags_dict[tag] = False

# Checkbox checked handler
def on_checkbox_change():
    tags_input_text = []
    for key in tags_dict.keys():
        if st.session_state[key]:
            tags_input_text.append(key)
    
    st.session_state['tags_input'] = ', '.join(tags_input_text)

# set all tags to true when select_alls are checked
def select_all_changed():
    # When this callback is called at that time the select_all variable
    # is still false and will be set to true after this function ends
    # so here we need to set to reverse of what its value is
    # Thus if false -> True and true -> false
    for tag in tags_list:
        st.session_state[tag] = not select_all
        tags_dict[tag] = not select_all
    
    # st.write(tags)
    on_checkbox_change()

#### checkbox to select/disselect all checkbox
select_all_container = st.columns(3)
select_all = select_all_container[1].checkbox(
    label="select all",
    value=False,
    key="select_all",
    on_change=select_all_changed
)

# There are 34 tags 
# first 6 rows will have 5 cols each covering 30 tags
# last 4 tags will be in the final row with 4 cols 
# There will be last column which will be empty. but who cares!!
cols = 5
for row_idx in range(0, len(tags_list), cols):
    row = st.columns(cols)

    for col_idx, col in enumerate(row):
        tag_container = col.container()

        if row_idx + col_idx < len(tags_list):
            # get the tag for that container
            tag = tags_list[row_idx+col_idx]

            # Add a checkbox for that tag
            tag_container.checkbox(
                label = tag.capitalize(),
                key = tag,
                value = tags_dict[tag],
                on_change = on_checkbox_change
            )

st.divider()

st.subheader('Quote generation parameters', divider='rainbow')

# Do sample checkbox to select token after sampling
# Here initial value of do_sample variable will be False
do_sample = st.checkbox(
    label='Do sample',
    value=False,
    key='do_sample',
    help = helper['do_sample']
)

# Slider to select the tokens length
st.slider(
    label = 'Max-new-token length',
    value = 16,
    key = 'max_new_token_length',
    min_value = 8,
    max_value = 100,
    step = 1,
    format = '%d',
    help = helper['max_token_length']
)

# add slider for selecting hte number of beams
st.slider(
    label = "Number of beams:",
    min_value = 1,
    max_value = 10,
    key = 'num_beams',
    value = 1,
    step = 1,
    format = '%d',
    help = helper['num_beams']
)

# slider for selecting top-k tokens.
# if do_Sample is checked than enable it and make its value to 20
st.slider(
    label = "Top-k Tokens",
    min_value = 1,
    max_value = 100,
    key = 'top_k',
    value = 50,
    step = 1,
    format = '%d',
    disabled = not do_sample
)

# Slider for selecting the top-p token probability mass
# if do_sample is checked than enable it and make its value to 0.9
st.slider(
    label = "Top-P Cummulative token Probability mass",
    min_value = 0.0,
    max_value = 1.0,
    key = 'top_p',
    value = 1.0,
    step = 0.1,
    format = '%.1f',
    disabled = not do_sample,
    help = helper['top_p']
)

# Slider for selecting the temperature to specify the token's probability for selection
# if do_sample than its value will be set to 0.6 else 0.0
st.slider(
    label = 'temperature',
    min_value = 0.0,
    max_value = 1.0,
    key = 'temperature',
    value = 1.0,
    step = 0.1,
    format = '%.1f',
    disabled = not do_sample,
    help = helper['temperature']
)

st.text_area(label='quote', value='', key='quote', label_visibility="collapsed", disabled=True)