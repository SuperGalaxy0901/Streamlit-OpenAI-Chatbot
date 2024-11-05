# import library
import streamlit as st
from captcha.image import ImageCaptcha
import random, string


# define the costant
length_captcha = 4
width = 220
height = 100

# define the function for the captcha control
def captcha_control():
    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
        st.session_state['controllo'] = False
        
        # Set up the captcha text
        if 'Captcha' not in st.session_state:
            st.session_state['Captcha'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        
        # Create columns for the captcha image, input, and verify button
        col1, col2, col3 = st.columns([2, 4, 1])
        
        with col1:
            image = ImageCaptcha(width=width, height=height)
            data = image.generate(st.session_state['Captcha'])
            st.image(data)
            
        with col2:
            capta2_text = st.text_input('Enter captcha text', placeholder='Type here...')
        
        with col3:
            st.text('')
            if st.button("Verify", key="verify_button", help="Click to verify the captcha"):
            # if st.button("Verify", key="verify_button"):
                if st.session_state['Captcha'].lower() == capta2_text.lower().strip():
                    del st.session_state['Captcha']
                    st.session_state['controllo'] = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect captcha. Please try again.")
                    del st.session_state['Captcha']
                    st.rerun()
            else:
                st.stop()