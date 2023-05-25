import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
from st_aggrid import (
    GridOptionsBuilder,
    AgGrid,
    GridUpdateMode,
    ColumnsAutoSizeMode,
)
import warnings

warnings.filterwarnings("ignore")
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# # Page 1: File Upload
# st.title("File Upload")

# uploaded_file1 = st.file_uploader("Upload CSV file", type="csv")

# if uploaded_file1 is not None:
#     gold_st = pd.read_csv("car_data.csv", index_col=[0]).applymap(
#         lambda x: x.lower() if isinstance(x, str) else x
#     )

# uploaded_file2 = st.file_uploader("Upload CSV file", type="xlsx", key="1")

# if uploaded_file2 is not None:
#     data = pd.read_excel("labels_output.xlsx", index_col=[0])
#     df = pd.DataFrame(data[:5])

# Page 1: File Upload
st.title("File Upload")


# Cache the file reading function using st.cache decorator


@st.cache_data()
def read_csv(file):
    return pd.read_csv(file, index_col=[0]).applymap(
        lambda x: x.lower() if isinstance(x, str) else x
    )


@st.cache_data()
def read_excel(file):
    data = pd.read_excel(file, index_col=[0])
    return pd.DataFrame(data[:5])


uploaded_file1 = st.file_uploader("Upload CSV file", type="csv", key="gold_st")

if uploaded_file1 is not None:
    gold_st1 = read_csv(uploaded_file1)
    st.session_state["gold_st1"] = gold_st1

uploaded_file2 = st.file_uploader("Upload Excel file", type="xlsx", key="df")

if uploaded_file2 is not None:
    df1 = read_excel(uploaded_file2)
    st.session_state["df1"] = df1


is_uploaded = st.button("NEXT!")

if is_uploaded:
    switch_page("test")

# selected_df = pd.DataFrame()

# names = [
#     "matched_brand",
#     "matched_model",
#     "matched_coupe",
#     "matched_hp",
#     "matched_fuel",
#     "matched_engine",
#     "matched_doors",
#     "matched_places",
#     "matched_generation",
#     "matched_yearstart",
#     "matched_yearstop",
# ]

# names_for_byhand = [
#     "temp",
#     "matched_brand",
#     "matched_model",
#     "matched_coupe",
#     "matched_hp",
#     "matched_fuel",
#     "matched_engine",
#     "matched_doors",
#     "matched_places",
#     "matched_generation",
#     "matched_yearstart",
#     "matched_yearstop",
# ]


# Page 2: Data Display


# def main():
#     st.title("Data Display")
#     selected_values = []
#     for index, row in df.iterrows():
#         # # BY HAND ENTRY
#         # by_hand_dict = {}
#         # all_fields = {}

#         # for idx, i in enumerate(names):
#         #     if idx < 5:
#         #         by_hand_dict[i] = ""
#         #     all_fields[i] = ""

#         # st.write(f"{row[['brand','raw_model']].values}")
#         # st.write(row.T)

#         table = row.to_frame()[:-2].T

#         # Use st.markdown() to display the HTML table with larger font size
#         # st.markdown(
#         #     f"<style>table {{font-size: 16px;}}</style>{table}", unsafe_allow_html=True
#         # )
#         data = AgGrid(
#             table,
#             enable_enterprise_modules=True,
#             allow_unsafe_jscode=True,
#             update_mode=GridUpdateMode.SELECTION_CHANGED,
#             columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
#             theme="streamlit",
#             height=100,
#         )

#         test = row["matches"].replace("nan", "None")

#         temp = pd.DataFrame(eval(test), columns=names)

#         # select the columns you want the users to see

#         gb = GridOptionsBuilder.from_dataframe(temp)
#         # configure selection
#         gb.configure_selection(selection_mode="single", use_checkbox=True)
#         gb.configure_side_bar()
#         gridOptions = gb.build()

#         data = AgGrid(
#             temp,
#             gridOptions=gridOptions,
#             enable_enterprise_modules=True,
#             allow_unsafe_jscode=True,
#             update_mode=GridUpdateMode.SELECTION_CHANGED,
#             columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
#         )
#         selected_rows = data["selected_rows"]
#         if len(selected_rows) != 0:
#             selected_values.append(selected_rows)

#         # BY HAND
#         # options brand
#         # Disable manual entry checkbox if selection is made
#         disable_manual_entry = bool(selected_rows)

#         manual_entry = st.checkbox(
#             "Manually Enter Data", key=f"checkb_{index}", disabled=disable_manual_entry
#         )

#         if manual_entry:
#             brand_opt = list(set(gold_st.brand.tolist()))
#             selected_option_1 = st.selectbox(
#                 "Select brand:", brand_opt, key=f"brand_{index}"
#             )

#             model_opt = list(
#                 set(gold_st[gold_st["brand"] == selected_option_1].model.tolist())
#             )
#             selected_option_2 = st.selectbox(
#                 "Select model:", model_opt, key=f"model_{index}"
#             )

#             # create empty dict:
#             selected_rows = {}
#             for i in names_for_byhand:
#                 selected_rows[i] = ""
#                 if i == "matched_brand":
#                     selected_rows[i] = selected_option_1
#                 elif i == "matched_model":
#                     selected_rows[i] = selected_option_2

#             no_data = st.checkbox("Model not in database", key=f"no_{index}")

#             if no_data:
#                 selected_values.append([])
#             else:
#                 selected_values.append([selected_rows])

#         elif disable_manual_entry == False and manual_entry == False:
#             selected_values.append([])

#         st.markdown(
#             '<hr style="height:10px;border:none;color:#333;background-color:#333;" />',
#             unsafe_allow_html=True,
#         )

#     # Save selected values to a CSV file
#     if st.button("Save"):
#         out = pd.DataFrame()
#         for i in selected_values:
#             if len(out) == 0:
#                 out = pd.DataFrame.from_dict(i)
#             elif len(i) == 1:
#                 temp = pd.DataFrame.from_dict(i)
#                 out = pd.concat([out, temp], axis=0).reset_index(drop=True)
#             elif len(i) == 0:
#                 emp = pd.Series()
#                 out.loc[len(out)] = emp

#         selected_df = out.iloc[:, 1:]

#         # merging with original df
#         selected_df = pd.concat([df.loc[:, "brand":"raw_model"], selected_df], axis=1)

#     st.download_button(
#         label="Download labels!", data=selected_df.to_csv(), file_name="test.csv"
#     )
