import streamlit as st
# import numpy as np
import pandas as pd

# @st.cache
def app():
    st.markdown("## Data Upload")

    # Upload the dataset and save as csv
    st.markdown("### Upload a csv or xlsx file with Salesforce invoice data")
    st.write("\n")

    # Code to read a single file 
    uploaded_file_1 = st.file_uploader("Choose a file", type = ['csv', 'xlsx'])
    global sf
    if uploaded_file is not None:
        try:
            sf = pd.read_csv(uploaded_file_1, encoding='latin1')
        except Exception as e:
            print(e)
            sf = pd.read_excel(uploaded_file_1)
    
    
    
    # uploaded_files = st.file_uploader("Upload your CSV file here.", type='csv', accept_multiple_files=False)
    # # Check if file exists 
    # if uploaded_files:
    #     for file in uploaded_files:
    #         file.seek(0)
    #     uploaded_data_read = [pd.read_csv(file) for file in uploaded_files]
    #     raw_data = pd.concat(uploaded_data_read)
    
    # uploaded_files = st.file_uploader("Upload CSV", type="csv", accept_multiple_files=False)
    # print(uploaded_files, type(uploaded_files))
    # if uploaded_files:
    #     for file in uploaded_files:
    #         file.seek(0)
    #     uploaded_data_read = [pd.read_csv(file) for file in uploaded_files]
    #     raw_data = pd.concat(uploaded_data_read)
    
    # read temp data 
    # data = pd.read_csv('data/2015.csv')


    ''' Load the data and save the columns with categories as a dataframe. 
    This section also allows changes in the numerical and categorical columns. '''
    if st.button("Load Salesforce Data"):
        
        # Raw data 
        st.dataframe(sf)
        #utils.getProfile(data)
        #st.markdown("<a href='output.html' download target='_blank' > Download profiling report </a>",unsafe_allow_html=True)
        #HtmlFile = open("data/output.html", 'r', encoding='utf-8')
        #source_code = HtmlFile.read() 
        #components.iframe("data/output.html")# Save the data to a new file 
        sf.to_csv('sf_data.csv', index=False)
        
        #Generate a pandas profiling report
        #if st.button("Generate an analysis report"):
        #    utils.getProfile(data)
            #Open HTML file

        # 	pass

        # Collect the categorical and numerical columns 
        
        # numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
        # categorical_cols = list(set(list(data.columns)) - set(numeric_cols))
        
        # Save the columns as a dataframe or dictionary
        # columns = []

        # Iterate through the numerical and categorical columns and save in columns 
        # columns = utils.genMetaData(data)
        
        # Save the columns as a dataframe with categories
        # Here column_name is the name of the field and the type is whether it's numerical or categorical
        # columns_df = pd.DataFrame(columns, columns = ['column_name', 'type'])
        # columns_df.to_csv('data/metadata/column_type_desc.csv', index = False)

        # # Display columns
        # st.markdown("**Column Name**-**Type**")
        # for i in range(columns_df.shape[0]):
        #     st.write(f"{i+1}. **{columns_df.iloc[i]['column_name']}** - {columns_df.iloc[i]['type']}")
        
        # st.markdown("""The above are the automated column types detected by the application in the data.
        # In case you wish to change the column types, head over to the **Column Change** section. """)
