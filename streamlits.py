# streamlit run streamlits.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="WU Directory", layout="wide")

st.title("Westminster University")
st.write("Campus Directory")

data = pd.read_csv("WU_directory.csv")

department_list = sorted(data['Department'].dropna().unique().tolist())
department_list.insert(0, 'All Departments')
department = st.selectbox(label='Choose one department from below:', options=department_list)

if department == 'All Departments':
    dept_bool = data['Department'].isin(department_list)
else:
    dept_bool = data['Department'] == department

role1, role2, role3, role4 = st.columns([0.2, 0.2, 0.2, 0.4])
with role1:
    st.text("Type of Role:")
with role2:
    faculty = st.checkbox('Faculty')
with role3:
    staff = st.checkbox('Staff')

if faculty and not staff:
    role_bool = data['Role'].str.contains('Faculty', case=False, na=False)
elif staff and not faculty:
    role_bool = data['Role'].str.contains('Staff', case=False, na=False)
elif faculty and staff:
    role_bool = data['Role'].str.contains(r'Faculty|Staff', case=False, na=False, regex=True)
else:
    role_bool = data['Role'].str.match('.+', na=False)

contract1, contract2, contract3, contract4 = st.columns([0.2, 0.2, 0.2, 0.4])
with contract1:
    st.text("Contract type:")
with contract2:
    full = st.checkbox('Full-time')
with contract3:
    part = st.checkbox('Part-time')

if full and not part:
    contract_bool = data['Contract'] == 'Full-time'
elif part and not full:
    contract_bool = data['Contract'] == 'Part-time'
elif full and part:
    contract_bool = data['Contract'].isin(['Full-time', 'Part-time'])
else:
    contract_bool = data['Contract'].isin(data['Contract'].dropna().unique())

rank1, rank2, rank3, rank4, rank5, rank6 = st.columns([0.2,0.2,0.2,0.2,0.2,0.4])
with rank1:
    st.text("Faculty Rank:")
with rank2:
    assistant = st.checkbox('Assistant')
with rank3:
    associate = st.checkbox('Associate')
with rank4:
    professor = st.checkbox('Professor')
with rank5:
    other = st.checkbox('Other')

pos = data['Position'].fillna('')

assistant_bool = pos.str.contains('Assistant', case=False, na=False)
associate_bool = pos.str.contains('Associate', case=False, na=False)
professor_bool = pos.str.contains('Professor', case=False, na=False) & ~pos.str.contains(r'Assistant|Associate', case=False, na=False, regex=True)
other_bool = ~pos.str.contains(r'Assistant|Associate|Professor', case=False, na=False, regex=True)

if assistant and associate and professor and other:
    rank_bool = data['Position'].notna()
elif assistant and associate and professor and not other:
    rank_bool = assistant_bool | associate_bool | professor_bool
elif assistant and associate and not professor and other:
    rank_bool = assistant_bool | associate_bool | other_bool
elif assistant and not associate and professor and other:
    rank_bool = assistant_bool | professor_bool | other_bool
elif not assistant and associate and professor and other:
    rank_bool = associate_bool | professor_bool | other_bool
elif assistant and associate and not professor and not other:
    rank_bool = assistant_bool | associate_bool
elif assistant and not associate and professor and not other:
    rank_bool = assistant_bool | professor_bool
elif assistant and not associate and not professor and other:
    rank_bool = assistant_bool | other_bool
elif not assistant and associate and professor and not other:
    rank_bool = associate_bool | professor_bool
elif not assistant and associate and not professor and other:
    rank_bool = associate_bool | other_bool
elif not assistant and not associate and professor and other:
    rank_bool = professor_bool | other_bool
elif assistant and not associate and not professor and not other:
    rank_bool = assistant_bool
elif not assistant and associate and not professor and not other:
    rank_bool = associate_bool
elif not assistant and not associate and professor and not other:
    rank_bool = professor_bool
elif not assistant and not associate and not professor and other:
    rank_bool = other_bool
else:
    rank_bool = data['Position'].notna()

name1, name2, name3 = st.columns([0.2,0.2,0.4])
with name1:
    name = st.text_input(label='Enter name:')
with name2:
    regex_on = st.checkbox('Enable Regex')
    all = st.checkbox('Enable All', value=True)

if name == '':
    name_bool = data['Name'].str.match(r'.*', na=False)
else:
    if not regex_on:
        name_bool = data['Name'].str.contains(rf'(^|\s){name}', case=False, na=False, regex=True)
    else:
        name_bool = data['Name'].str.contains(name, case=True, na=False,regex=True)

all_conditions = dept_bool & role_bool & contract_bool & rank_bool & name_bool

if all:
    st.dataframe(data[dept_bool])
    st.write("Total number of records: " + str(data[dept_bool].shape[0]))
elif data[all_conditions].shape[0] == 0 or (name =='' and (faculty + staff + full + part + assistant + associate + professor + other == 0)):
    st.write("No results found.")
else:
    st.dataframe(data[all_conditions])
    st.write("Total number of records: " + str(data[all_conditions].shape[0]))
