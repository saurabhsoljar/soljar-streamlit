{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "a515de0d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# import all the app dependencies\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import sklearn\n",
    "import streamlit as st\n",
    "import joblib\n",
    "import matplotlib\n",
    "from IPython import get_ipython\n",
    "from PIL import Image\n",
    "\n",
    "# load the encoder and model object\n",
    "model = joblib.load(\"rta_model_deploy3.joblib\")\n",
    "encoder = joblib.load(\"ordinal_encoder2.joblib\")\n",
    "\n",
    "st.set_option('deprecation.showPyplotGlobalUse', False)\n",
    "\n",
    "# 1: serious injury, 2: Slight injury, 0: Fatal Injury\n",
    "\n",
    "st.set_page_config(page_title=\"Accident Severity Prediction App\",\n",
    "        page_icon=\"🚧\", layout=\"wide\")\n",
    "\n",
    "#creating option list for dropdown menu\n",
    "options_day = ['Sunday', \"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\"]\n",
    "options_age = ['18-30', '31-50', 'Over 51', 'Unknown', 'Under 18']\n",
    "\n",
    "# number of vehicle involved: range of 1 to 7\n",
    "# number of casualties: range of 1 to 8\n",
    "# hour of the day: range of 0 to 23\n",
    "\n",
    "options_types_collision = ['Vehicle with vehicle collision','Collision with roadside objects',\n",
    "              'Collision with pedestrians','Rollover','Collision with animals',\n",
    "              'Unknown','Collision with roadside-parked vehicles','Fall from vehicles',\n",
    "              'Other','With Train']\n",
    "\n",
    "options_sex = ['Male','Female','Unknown']\n",
    "\n",
    "options_education_level = ['Junior high school','Elementary school','High school',\n",
    "              'Unknown','Above high school','Writing & reading','Illiterate']\n",
    "\n",
    "options_services_year = ['Unknown','2-5yrs','Above 10yr','5-10yrs','1-2yr','Below 1yr']\n",
    "\n",
    "options_acc_area = ['Other', 'Office areas', 'Residential areas', ' Church areas',\n",
    "    ' Industrial areas', 'School areas', ' Recreational areas',\n",
    "    ' Outside rural areas', ' Hospital areas', ' Market areas',\n",
    "    'Rural village areas', 'Unknown', 'Rural village areasOffice areas',\n",
    "    'Recreational areas']\n",
    "\n",
    "# features list\n",
    "features = ['Number_of_vehicles_involved','Number_of_casualties','Hour_of_Day','Type_of_collision','Age_band_of_driver','Sex_of_driver',\n",
    "    'Educational_level','Service_year_of_vehicle','Day_of_week','Area_accident_occured']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "6e15426c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: streamlit in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (1.22.0)\n",
      "Requirement already satisfied: altair<5,>=3.2.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (4.2.2)\n",
      "Requirement already satisfied: tzlocal>=1.1 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (5.0.1)\n",
      "Requirement already satisfied: watchdog in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (2.1.6)\n",
      "Requirement already satisfied: importlib-metadata>=1.4 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (4.11.3)\n",
      "Requirement already satisfied: rich>=10.11.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (13.3.5)\n",
      "Requirement already satisfied: tenacity<9,>=8.0.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (8.0.1)\n",
      "Requirement already satisfied: gitpython!=3.1.19 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (3.1.31)\n",
      "Requirement already satisfied: click>=7.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (8.0.4)\n",
      "Requirement already satisfied: typing-extensions>=3.10.0.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (4.3.0)\n",
      "Requirement already satisfied: pympler>=0.9 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (1.0.1)\n",
      "Requirement already satisfied: numpy in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (1.21.5)\n",
      "Requirement already satisfied: pydeck>=0.1.dev5 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (0.8.1b0)\n",
      "Requirement already satisfied: packaging>=14.1 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (21.3)\n",
      "Requirement already satisfied: requests>=2.4 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (2.28.1)\n",
      "Requirement already satisfied: blinker>=1.0.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (1.6.2)\n",
      "Requirement already satisfied: pyarrow>=4.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (12.0.0)\n",
      "Requirement already satisfied: validators>=0.2 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (0.20.0)\n",
      "Requirement already satisfied: pandas<3,>=0.25 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (1.4.4)\n",
      "Requirement already satisfied: protobuf<4,>=3.12 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (3.20.3)\n",
      "Requirement already satisfied: cachetools>=4.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (5.3.0)\n",
      "Requirement already satisfied: toml in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (0.10.2)\n",
      "Requirement already satisfied: tornado>=6.0.3 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (6.1)\n",
      "Requirement already satisfied: pillow>=6.2.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (9.2.0)\n",
      "Requirement already satisfied: python-dateutil in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from streamlit) (2.8.2)\n",
      "Requirement already satisfied: toolz in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from altair<5,>=3.2.0->streamlit) (0.11.2)\n",
      "Requirement already satisfied: entrypoints in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from altair<5,>=3.2.0->streamlit) (0.4)\n",
      "Requirement already satisfied: jsonschema>=3.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from altair<5,>=3.2.0->streamlit) (4.16.0)\n",
      "Requirement already satisfied: jinja2 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from altair<5,>=3.2.0->streamlit) (2.11.3)\n",
      "Requirement already satisfied: colorama in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from click>=7.0->streamlit) (0.4.5)\n",
      "Requirement already satisfied: gitdb<5,>=4.0.1 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from gitpython!=3.1.19->streamlit) (4.0.10)\n",
      "Requirement already satisfied: zipp>=0.5 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from importlib-metadata>=1.4->streamlit) (3.8.0)\n",
      "Requirement already satisfied: pyparsing!=3.0.5,>=2.0.2 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from packaging>=14.1->streamlit) (3.0.9)\n",
      "Requirement already satisfied: pytz>=2020.1 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from pandas<3,>=0.25->streamlit) (2022.1)\n",
      "Requirement already satisfied: six>=1.5 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from python-dateutil->streamlit) (1.16.0)\n",
      "Requirement already satisfied: charset-normalizer<3,>=2 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from requests>=2.4->streamlit) (2.0.4)\n",
      "Requirement already satisfied: idna<4,>=2.5 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from requests>=2.4->streamlit) (3.3)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from requests>=2.4->streamlit) (2022.9.14)\n",
      "Requirement already satisfied: urllib3<1.27,>=1.21.1 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from requests>=2.4->streamlit) (1.26.11)\n",
      "Requirement already satisfied: markdown-it-py<3.0.0,>=2.2.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from rich>=10.11.0->streamlit) (2.2.0)\n",
      "Requirement already satisfied: pygments<3.0.0,>=2.13.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from rich>=10.11.0->streamlit) (2.15.1)\n",
      "Requirement already satisfied: tzdata in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from tzlocal>=1.1->streamlit) (2023.3)\n",
      "Requirement already satisfied: decorator>=3.4.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from validators>=0.2->streamlit) (5.1.1)\n",
      "Requirement already satisfied: smmap<6,>=3.0.1 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19->streamlit) (5.0.0)\n",
      "Requirement already satisfied: MarkupSafe>=0.23 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from jinja2->altair<5,>=3.2.0->streamlit) (2.0.1)\n",
      "Requirement already satisfied: pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from jsonschema>=3.0->altair<5,>=3.2.0->streamlit) (0.18.0)\n",
      "Requirement already satisfied: attrs>=17.4.0 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from jsonschema>=3.0->altair<5,>=3.2.0->streamlit) (21.4.0)\n",
      "Requirement already satisfied: mdurl~=0.1 in c:\\users\\saurabh\\anaconda3\\lib\\site-packages (from markdown-it-py<3.0.0,>=2.2.0->rich>=10.11.0->streamlit) (0.1.2)\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "pip install streamlit"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "8b72c5b3",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2023-05-16 10:46:43.039 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\saurabh\\anaconda3\\lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    }
   ],
   "source": [
    "# Give a title to web app using html syntax\n",
    "st.markdown(\"<h1 style='text-align: center;'>Accident Severity Prediction App 🚧</h1>\", unsafe_allow_html=True)\n",
    "\n",
    "# define a main() function to take inputs from user in form based approach\n",
    "def main():\n",
    "    with st.form(\"road_traffic_severity_form\"):\n",
    "       st.subheader(\"Please enter the following inputs:\")\n",
    "        \n",
    "       No_vehicles = st.slider(\"Number of vehicles involved:\",1,7, value=0, format=\"%d\")\n",
    "       No_casualties = st.slider(\"Number of casualties:\",1,8, value=0, format=\"%d\")\n",
    "       Hour = st.slider(\"Hour of the day:\", 0, 23, value=0, format=\"%d\")\n",
    "       collision = st.selectbox(\"Type of collision:\",options=options_types_collision)\n",
    "       Age_band = st.selectbox(\"Driver age group?:\", options=options_age)\n",
    "       Sex = st.selectbox(\"Sex of the driver:\", options=options_sex)\n",
    "       Education = st.selectbox(\"Education of driver:\",options=options_education_level)\n",
    "       service_vehicle = st.selectbox(\"Service year of vehicle:\", options=options_services_year)\n",
    "       Day_week = st.selectbox(\"Day of the week:\", options=options_day)\n",
    "       Accident_area = st.selectbox(\"Area of accident:\", options=options_acc_area)\n",
    "        \n",
    "       submit = st.form_submit_button(\"Predict\")\n",
    "\n",
    "# encode using ordinal encoder and predict\n",
    "    if submit:\n",
    "       input_array = np.array([collision,\n",
    "                  Age_band,Sex,Education,service_vehicle,\n",
    "                  Day_week,Accident_area], ndmin=2)\n",
    "        \n",
    "       encoded_arr = list(encoder.transform(input_array).ravel())\n",
    "        \n",
    "       num_arr = [No_vehicles,No_casualties,Hour]\n",
    "       pred_arr = np.array(num_arr + encoded_arr).reshape(1,-1)        \n",
    "      \n",
    "# predict the target from all the input features\n",
    "       prediction = model.predict(pred_arr)\n",
    "        \n",
    "       if prediction == 0:\n",
    "           st.write(f\"The severity prediction is fatal injury⚠\")\n",
    "       elif prediction == 1:\n",
    "           st.write(f\"The severity prediction is serious injury\")\n",
    "       else:\n",
    "           st.write(f\"The severity prediction is slight injury\")\n",
    "        \n",
    "       st.write(\"Developed By: Avi kumar Talaviya\")\n",
    "       st.markdown(\"\"\"Reach out to me on: [Twitter](https://twitter.com/avikumart_) |\n",
    "       [Linkedin](https://www.linkedin.com/in/avi-kumar-talaviya-739153147/) |\n",
    "       [Kaggle](https://www.kaggle.com/avikumart) \n",
    "       \"\"\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "2194e019",
   "metadata": {},
   "outputs": [],
   "source": [
    "a,b,c = st.columns([0.2,0.6,0.2])\n",
    "with b:\n",
    " st.image(\"banner-picture.jpeg\", use_column_width=True)\n",
    "\n",
    "\n",
    "# description about the project and code files       \n",
    "st.subheader(\"🧾Description:\")\n",
    "st.text(\"\"\"This data set is collected from Addis Ababa Sub-city police departments for master's research work. \n",
    "The data set has been prepared from manual records of road traffic accidents of the year 2017-20. \n",
    "All the sensitive information has been excluded during data encoding and finally it has 32 features and 12316 instances of the accident.\n",
    "Then it is preprocessed and for identification of major causes of the accident by analyzing it using different machine learning classification algorithms.\n",
    "\"\"\")\n",
    "\n",
    "st.markdown(\"Source of the dataset: [Click Here](https://www.narcis.nl/dataset/RecordID/oai%3Aeasy.dans.knaw.nl%3Aeasy-dataset%3A191591)\")\n",
    "\n",
    "st.subheader(\"🧭 Problem Statement:\")\n",
    "st.text(\"\"\"The target feature is Accident_severity which is a multi-class variable. \n",
    "The task is to classify this variable based on the other 31 features step-by-step by going through each day's task. \n",
    "The metric for evaluation will be f1-score\n",
    "\"\"\")\n",
    "\n",
    "st.markdown(\"Please find GitHub repository link of project: [Click Here](https://github.com/avikumart/Road-Traffic-Severity-Classification-Project)\")          \n",
    "  \n",
    "# run the main function        \n",
    "if __name__ == '__main__':\n",
    "  main()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2123a758",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
