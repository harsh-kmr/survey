import streamlit as st
import pandas as pd

# Define subject sets for each class
subjects_class_10 = ['Mathematics', 'Science', 'Social Science', 'English', 'Hindi']
subjects_class_12 = ['Physics', 'Chemistry', 'Mathematics']

# CSV file to store responses
CSV_FILE = 'survey_responses.csv'

def main():
    st.title('Teacher Survey Form')


    # First MCQ: What classes do you teach? (single select)
    class_choice = st.selectbox('What classes do you teach?', ['Class 10', 'Class 12', 'Both'])

    # For compatibility with rest of code, create a list of classes
    if class_choice == 'Both':
        classes = ['Class 10', 'Class 12']
    else:
        classes = [class_choice]

    teaching_exp = st.selectbox('How long have you been teaching?', [
        '0-5 years', 'More than 5 years'
    ])


    # Subject selection logic using checkboxes
    # Store subjects with class prefix to avoid duplicates
    selected_subjects = []
    if class_choice == 'Both':
        st.markdown('**Which Class 10 subjects do you teach?**')
        selected_subjects_10 = [(f'Class 10 - {subj}', subj) for subj in subjects_class_10 if st.checkbox(subj, key=f'class10_{subj}')]
        st.markdown('**Which Class 12 subjects do you teach?**')
        selected_subjects_12 = [(f'Class 12 - {subj}', subj) for subj in subjects_class_12 if st.checkbox(subj, key=f'class12_{subj}')]
        selected_subjects = selected_subjects_10 + selected_subjects_12
    elif class_choice == 'Class 10':
        st.markdown('**Which Class 10 subjects do you teach?**')
        selected_subjects = [(f'Class 10 - {subj}', subj) for subj in subjects_class_10 if st.checkbox(subj, key=f'class10_{subj}')]
    elif class_choice == 'Class 12':
        st.markdown('**Which Class 12 subjects do you teach?**')
        selected_subjects = [(f'Class 12 - {subj}', subj) for subj in subjects_class_12 if st.checkbox(subj, key=f'class12_{subj}')]

    # For each subject, ask for percentage ranges using integer inputs
    subject_ranges = {}
    for subj_full, subj_display in selected_subjects:
        st.subheader(f'Set percentage ranges for {subj_full}')
        avg_min = st.number_input(f'Average student percentage min for {subj_full}', min_value=0, max_value=100, step=10, key=f'avg_min_{subj_full}')
        avg_max = st.number_input(f'Average student percentage max for {subj_full}', min_value=0, max_value=100, step=10, key=f'avg_max_{subj_full}')
        st.markdown(f"Average: {int(avg_min)}% to {int(avg_max)}%")
        good_min = st.number_input(f'Good student percentage min for {subj_full}', min_value=0, max_value=100, step=10, key=f'good_min_{subj_full}')
        good_max = st.number_input(f'Good student percentage max for {subj_full}', min_value=0, max_value=100, step=10, key=f'good_max_{subj_full}')
        st.markdown(f"Good: {int(good_min)}% to {int(good_max)}%")
        bad_min = st.number_input(f'Bad student percentage min for {subj_full}', min_value=0, max_value=100, step=10, key=f'bad_min_{subj_full}')
        bad_max = st.number_input(f'Bad student percentage max for {subj_full}', min_value=0, max_value=100, step=10, key=f'bad_max_{subj_full}')
        st.markdown(f"Bad: {int(bad_min)}% to {int(bad_max)}%")
        subject_ranges[subj_full] = {
            'avg': f'{int(avg_min)} to {int(avg_max)}',
            'good': f'{int(good_min)} to {int(good_max)}',
            'bad': f'{int(bad_min)} to {int(bad_max)}'
        }

    if st.button('Submit'):
        # Prepare data for saving
        subject_names = [subj_full for subj_full, _ in selected_subjects]
        data = {
            'classes': ', '.join(classes),
            'teaching_experience': teaching_exp,
            'subjects': ', '.join(subject_names)
        }
        for subj, ranges in subject_ranges.items():
            data[f'{subj}_avg'] = ranges['avg']
            data[f'{subj}_good'] = ranges['good']
            data[f'{subj}_bad'] = ranges['bad']

        # Save to CSV
        try:
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        except FileNotFoundError:
            df = pd.DataFrame([data])
        df.to_csv(CSV_FILE, index=False)
        st.success('Response submitted!')

    # Optionally, show all responses
    if st.checkbox('Show all responses'):
        try:
            df = pd.read_csv(CSV_FILE)
            st.dataframe(df)
        except FileNotFoundError:
            st.info('No responses yet.')

if __name__ == '__main__':
    main()
