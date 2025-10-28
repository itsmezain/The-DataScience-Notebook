import streamlit as st
import pandas as pd
import time 


# Text utility / widgets
st.title("Startup Dashboard")

st.header("I am learning Streamlit")

st.subheader("And I am loving it!!!")

st.write("This is normal text")

st.markdown("""
### My favorite movies
- Race 3
- GOT
- The Witcher
""")


st.code("""
def square(x):
    return x**2
    
x = square(4)
""")


st.latex(" x^2 + y^2 + 2 = 0")

# Display Elements 

df = pd.DataFrame({
    'name': ['Syed','Ali','Zain'],
    'marks': [50,60,70],
    'package': [10,12,14]
})

st.dataframe(df)

st.metric('Revenue', 'Rs 3L', "-3%", border = True)


st.json({
    'name': ['Syed','Ali','Zain'],
    'marks': [50,60,70],
    'package': [10,12,14]
})

# Display Media

st.image('Zain.jpg', width=800)

st.video('video.mp4')



# Creating Layout

st.sidebar.title("Sidebar Title") # isme saare cheeze add kar skte hai joo hamne abhi tkk seekha hai

col1, col2, col3 = st.columns(3)

with col1:
    st.image('Zain.jpg')
with col2:
    st.image('Zain.jpg')
with col3:
    st.image('Zain.jpg')
    
    
### Showing Status


st.error('Login Failed')
st.success('Login Completed')
st.info('Login Completed')
st.warning('Login Completed')

# Progress Bar

# bar = st.progress(0)

# for i in range(1,101):
#     time.sleep(1)
#     bar.progress(i)
    


#### Taking user input
#----------------------------#

# Text input

email_inp = st.text_input('Enter email0')

# Number input
number = st.number_input('Enter number:', 184565)

# Date input
date_inp = st.date_input('Enter a date')


## Button

email = st.text_input('Enter email')

password = st.text_input('Enter password', type = 'password')

## DropDown
gender = st.selectbox('Select Gender', ['male','female', 'others'])

btn = st.button("Login Button")

# if the button is clicked
if btn:
    if email == "zain@gmail.com" and password == "123":
        st.balloons()
        st.write(gender)
        st.success("Login Sucessful")
        
    else:
        st.error("Login failed")
        



###     File upload
#----------------------------------#

file = st.file_uploader("Upload a csv file")

if file is not None:
    pd.read_csv(file)
    st.dataframe(df.describe())