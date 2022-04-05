import streamlit as st
import pickle
from datetime import datetime
import sklearn
startTime = datetime.now()


st.set_page_config(page_title="Heart Disease App")

filename = "hw_model.sv"
model = pickle.load(open(filename,'rb'))


overview = st.container()
left, right = st.columns(2)


with overview:
    st.title("Heart Disease Prediction")


with left:
    sex_d = st.selectbox('Sex',('M', 'F'))
    pain_type_d = st.selectbox('ChestPainType',('ATA', 'NAP','ASY','TA'))
    resting_d = st.selectbox('RestingECG',('Normal', 'ST','LVH'))
    angina_d = st.selectbox('ExerciseAngina',('N', 'Y'))
    slope_d = st.selectbox('ST_Slope',('Up', 'Flat','Down'))


with right:
	age_slider = st.slider("Age", value=40, min_value=1, max_value=100)
	RestingBP_slider = st.slider("RestingBP",value=100, min_value=0, max_value=200)
	Cholesterol_slider = st.slider("Cholesterol",value=200, min_value=0, max_value=700)
	FastingBS_slider = st.slider("FastingBS", min_value=0, max_value=1, step=1)

Oldpeak_slider = st.slider("Oldpeak", min_value=-3.0, max_value=6.0, step=0.1)
hr_slider = st.slider("MaxHR" ,value=130, min_value = 50, max_value=200)

prediction = st.container()
data = [[age_slider, {'M':1,'F':0}.get(sex_d),{'ATA':1, 'NAP':2, 'ASY':0, 'TA':3}.get(pain_type_d),
 RestingBP_slider, Cholesterol_slider, FastingBS_slider, {'Normal':1, 'ST':2, 'LVH':0}.get(resting_d),
  hr_slider, {'N':0, 'Y':1}.get(angina_d),Oldpeak_slider,{'Up':2, 'Flat':1, 'Down':0}.get(slope_d)
  ]]

survival = model.predict(data)
s_confidence = model.predict_proba(data)

with prediction:
	st.subheader("Do I have heart disease?")
	st.subheader(("Yes" if survival[0] == 1 else "No"))
	st.write("Prob {0:.2f} %".format(s_confidence[0][survival][0] * 100))
