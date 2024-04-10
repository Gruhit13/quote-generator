import streamlit as st
import json
import requests

request_url = 'https://gruhit13-quote-generator-backend.hf.space'
# request_url = 'http://127.0.0.1:8000'

# Main title of the page
st.title('Quote Generator 🤖')

# a row for containing the text_input and submit button
input_container = st.columns([0.7, 0.3])

# Display the tags that are selected
input_container[0].text_input(
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

    with st.spinner("🤖 is generating quote for you..."):
        response = requests.post(
            request_url+'/generate_quote',
            json = {'tags': tags},
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

# List of the tags that are selected
tags = {
    'love': False,
    'inspirational': False,
    'philosophy': False,
    'humor': False,
    'god': False,
    'truth': False,
    'wisdom': False,
    'happiness': False,
    'hope': False,
    'life': False
}

# Checkbox checked handler
def on_checkbox_change():
    tags_input_text = []
    for key in tags.keys():
        if st.session_state[key]:
            tags_input_text.append(key)
    
    st.session_state['tags_input'] = ', '.join(tags_input_text)

#  Create a list of all tags
tags_list = list(tags.keys())

# set all tags to true when select_alls are checked
def select_all_changed():
    # When this callback is called at that time the select_all variable
    # is still false and will be set to true after this function ends
    # so here we need to set to reverse of what its value is
    # Thus if false -> True and true -> false
    st.write('select all set to ', select_all)
    for tag in tags_list:
        st.session_state[tag] = not select_all
        tags[tag] = not select_all
    
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

# We need 5 rows and for each row we need 2 columns
for index in range(0, len(tags_list), 2):
    row = st.columns([0.5, 0.5])
    for col_idx, col in enumerate(row):
        # Create a container for each
        tag_container = col.container()
        
        # Fetch the tag at the index
        tag = tags_list[index+col_idx]

        # Add the checkbox for that tag
        tag_container.checkbox(
            label=tag.capitalize(),
            key=tag,
            value=tags[tag],
            on_change=on_checkbox_change
        )

st.text_area(label='quote', value='', key='quote', label_visibility="collapsed", disabled=True)