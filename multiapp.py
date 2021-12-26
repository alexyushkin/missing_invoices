import streamlit as st


class MultiApp:


    def __init__(self) -> None:

        self.apps = []


    def add_app(self, title, function) -> None:

        self.apps.append(
            {
                'title': title,
                'function': function
            }
        )

    def run_app(self):

#         page = st.sidebar.selectbox(
#             'Applications',
#             self.apps,
#             format_func=lambda page: page['title']
#         )
    if st.session_state['authentication_status']:
        st.write('Welcome *%s*' % (st.session_state['name']))
            if st.session_state['name'] == 'Test':
                page['App 1']() 
            if st.session_state['name'] == 'Test':
                page['App 2']() 
    elif st.session_state['authentication_status'] == False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] == None:
        st.warning('Please enter your username and password')
 
        # run the app function
#         page['function']()
