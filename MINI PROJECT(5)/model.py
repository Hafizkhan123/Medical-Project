import dotenv 
import google.generativeai as genai 
import streamlit as st 

# Configure the API key for the generative AI
from api_key import api_key 
genai.configure(api_key=api_key) 

# Define the generation configuration
generation_config = { 
 "temperature": 0.4, 
 "top_p": 0.95, 
 "top_k": 64, 
 "max_output_tokens": 8192, 
} 

def model(prompt):
    # Debugging: Print the input prompt
    print(f"Debug: Input to model: {prompt}")

    # Predefined medical conditions with reasons and remedies
    medical_data = {
        "cold": {
            "reason": "A cold is usually caused by a viral infection, such as rhinovirus.",
            "remedy": "Stay hydrated, rest, and consider over-the-counter medications like decongestants."
        },
        "malaria": {
            "reason": "Malaria is caused by a parasite transmitted through the bite of infected mosquitoes.",
            "remedy": "Seek medical attention immediately. Antimalarial drugs like chloroquine may be prescribed."
        },
        "fever": {
            "reason": "Fever is often a symptom of an underlying infection or inflammation.",
            "remedy": "Drink plenty of fluids, rest, and take antipyretics like paracetamol if needed."
        },
        "dengue": {
            "reason": "Dengue is caused by the dengue virus, transmitted by Aedes mosquitoes.",
            "remedy": "Stay hydrated and seek medical attention if symptoms worsen. Pain relievers like acetaminophen may help."
        },
        "cancer": {
            "reason": "Cancer is caused by uncontrolled cell growth and can be influenced by genetic and environmental factors.",
            "remedy": "Consult an oncologist for diagnosis and treatment options, which may include surgery, chemotherapy, or radiation."
        },
        "diabetes": {
            "reason": "Diabetes is a chronic condition that affects how your body processes blood sugar (glucose).",
            "remedy": "Manage blood sugar levels through diet, exercise, and medication as prescribed by a healthcare provider."
        },
        "hypertension": {
            "reason": "Hypertension, or high blood pressure, can be caused by various factors including diet, stress, and genetics.",
            "remedy": "Lifestyle changes such as a low-sodium diet, regular exercise, and medication may be recommended."
        },
        "asthma": {
            "reason": "Asthma is a chronic condition that affects the airways in the lungs, often triggered by allergens or irritants.",
            "remedy": "Use inhalers as prescribed, avoid triggers, and consult a healthcare provider for management strategies."
        # Add more conditions as needed
    },
        "allergy": {
            "reason": "Allergies occur when the immune system reacts to a substance (allergen) as if it were harmful.",
            "remedy": "Avoid known allergens, use antihistamines, and consult an allergist for further management."
        },
        "headache": {
            "reason": "Headaches can be caused by tension, dehydration, or underlying medical conditions.",
            "remedy": "Stay hydrated, rest in a dark room, and consider over-the-counter pain relievers."
        },
        "stomach ache": {
            "reason": "Stomach aches can result from various causes including indigestion, gas, or infections.",
            "remedy": "Stay hydrated, avoid heavy meals, and consider over-the-counter antacids."
        },
        "back pain": {
            "reason": "Back pain can be caused by muscle strain, injury, or underlying conditions.",
            "remedy": "Rest, apply heat or cold packs, and consider over-the-counter pain relievers."
        },
        "skin rash": {
            "reason": "Skin rashes can be caused by allergies, infections, or irritants.",
            "remedy": "Avoid scratching, keep the area clean, and consider over-the-counter hydrocortisone cream."
        },
        "fatigue": {
            "reason": "Fatigue can result from lack of sleep, stress, or underlying medical conditions.",
            "remedy": "Ensure adequate rest, manage stress, and consult a healthcare provider if fatigue persists."
        },
        "nausea": {
            "reason": "Nausea can be caused by various factors including motion sickness, infections, or medications.",
            "remedy": "Stay hydrated, avoid strong odors, and consider over-the-counter anti-nausea medications."
        },
        "cough": {
            "reason": "Coughing can be caused by infections, allergies, or irritants.",
            "remedy": "Stay hydrated, use cough drops, and consider over-the-counter cough suppressants."
        },
        "sore throat": {
            "reason": "A sore throat can be caused by infections, allergies, or irritants.",
            "remedy": "Gargle with warm salt water, stay hydrated, and consider over-the-counter pain relievers."
        },
        "insomnia": {
            "reason": "Insomnia can be caused by stress, anxiety, or underlying medical conditions.",
            "remedy": "Establish a regular sleep routine, avoid caffeine, and consider relaxation techniques."
        },
        "anxiety": {
            "reason": "Anxiety can be caused by stress, genetics, or environmental factors.",
            "remedy": "Practice relaxation techniques, exercise regularly, and consider consulting a mental health professional."
        },
        "depression": {
            "reason": "Depression can be caused by a combination of genetic, biological, environmental, and psychological factors.",
            "remedy": "Seek professional help, consider therapy or medication, and engage in regular physical activity."
        },
        "arthritis": {
            "reason": "Arthritis is inflammation of the joints, which can be caused by various factors including age and genetics.",
            "remedy": "Consult a rheumatologist for diagnosis and treatment options, which may include medication and physical therapy."
        },
        "eczema": {
            "reason": "Eczema is a condition that makes the skin red and itchy, often caused by allergies or irritants.",
            "remedy": "Keep the skin moisturized, avoid known triggers, and consider over-the-counter hydrocortisone cream."
        },
        "psoriasis": {
            "reason": "Psoriasis is an autoimmune condition that causes rapid skin cell growth, leading to scaling and inflammation.",
            "remedy": "Consult a dermatologist for treatment options, which may include topical treatments or phototherapy."
        },
        "gout": {
            "reason": "Gout is a form of arthritis caused by excess uric acid in the blood, leading to joint inflammation.",
            "remedy": "Avoid purine-rich foods, stay hydrated, and consult a healthcare provider for medication."
        },
        "migraine": {
            "reason": "Migraines are severe headaches often accompanied by nausea and sensitivity to light.",
            "remedy": "Identify triggers, stay hydrated, and consider over-the-counter or prescription medications."
        },
        "pneumonia": {
            "reason": "Pneumonia is an infection that inflames the air sacs in one or both lungs, often caused by bacteria or viruses.",
            "remedy": "Seek medical attention for diagnosis and treatment, which may include antibiotics or antiviral medications."
        },
        "bronchitis": {
            "reason": "Bronchitis is inflammation of the bronchial tubes, often caused by infections or irritants.",
            "remedy": "Stay hydrated, rest, and consider over-the-counter cough medications."
        },
        "ulcer": {
            "reason": "Ulcers are sores that develop on the lining of the stomach or intestines, often caused by H. pylori infection or NSAID use.",
            "remedy": "Consult a healthcare provider for diagnosis and treatment, which may include antibiotics and acid-reducing medications."
        },
        "constipation": {
            "reason": "Constipation can be caused by a lack of fiber, dehydration, or certain medications.",
            "remedy": "Increase fiber intake, stay hydrated, and consider over-the-counter laxatives if needed."
        },
        "diarrhea": {
            "reason": "Diarrhea can be caused by infections, food intolerances, or medications.",
            "remedy": "Stay hydrated, avoid dairy and fatty foods, and consider over-the-counter anti-diarrheal medications."
        },
        "acne": {
            "reason": "Acne is caused by clogged hair follicles due to oil, dead skin cells, and bacteria.",
            "remedy": "Keep the skin clean, avoid picking, and consider over-the-counter topical treatments."
        },
        "obesity": {
            "reason": "Obesity is caused by an imbalance between calorie intake and expenditure, influenced by genetics and lifestyle.",
            "remedy": "Adopt a balanced diet, increase physical activity, and consult a healthcare provider for personalized advice."
        },
        "osteoporosis": {
            "reason": "Osteoporosis is a condition that weakens bones, making them fragile and more likely to fracture.",
            "remedy": "Ensure adequate calcium and vitamin D intake, engage in weight-bearing exercises, and consult a healthcare provider."
        },
        "thyroid disorder": {
            "reason": "Thyroid disorders can be caused by autoimmune diseases, iodine deficiency, or genetic factors.",
            "remedy": "Consult an endocrinologist for diagnosis and treatment options, which may include medication or surgery."
        },
        "kidney stones": {
            "reason": "Kidney stones are hard deposits made of minerals and salts that form in the kidneys.",
            "remedy": "Stay hydrated, avoid high-oxalate foods, and consult a healthcare provider for treatment options."
        },
        "liver disease": {
            "reason": "Liver disease can be caused by viral infections, alcohol abuse, or fatty liver disease.",
            "remedy": "Consult a hepatologist for diagnosis and treatment options, which may include lifestyle changes and medications."
        },
        "heart disease": {
            "reason": "Heart disease can be caused by a combination of genetic, lifestyle, and environmental factors.",
            "remedy": "Adopt a heart-healthy diet, exercise regularly, and consult a cardiologist for personalized advice."
        },
        "anemia": {
            "reason": "Anemia is a condition in which you lack enough healthy red blood cells to carry adequate oxygen to your body's tissues.",
            "remedy": "Increase iron-rich foods in your diet, consider iron supplements, and consult a healthcare provider."
        },
        "allergic rhinitis": {
            "reason": "Allergic rhinitis is an allergic reaction that causes sneezing, stuffy or runny nose, and itchy eyes.",
            "remedy": "Avoid allergens, use antihistamines, and consider nasal corticosteroids."
        },
        "chickenpox": {
            "reason": "Chickenpox is a highly contagious viral infection characterized by an itchy rash and flu-like symptoms.",
            "remedy": "Stay hydrated, avoid scratching, and consult a healthcare provider for antiviral medications if needed."
        },
        "shingles": {
            "reason": "Shingles is a viral infection that causes a painful rash, caused by the varicella-zoster virus.",
            "remedy": "Consult a healthcare provider for antiviral medications and pain relief."
        },
        "whooping cough": {
            "reason": "Whooping cough is a highly contagious respiratory disease caused by the bacterium Bordetella pertussis.",
            "remedy": "Consult a healthcare provider for antibiotics and supportive care."
        },
        "tuberculosis": {
            "reason": "Tuberculosis (TB) is a bacterial infection that primarily affects the lungs.",
            "remedy": "Seek medical attention for diagnosis and treatment, which may include a long course of antibiotics."
        },
        "HIV/AIDS": {
            "reason": "HIV is a virus that attacks the immune system, leading to AIDS if untreated.",
            "remedy": "Consult a healthcare provider for antiretroviral therapy and regular monitoring."
        },
        "hepatitis": {
            "reason": "Hepatitis is inflammation of the liver, often caused by viral infections or alcohol use.",
            "remedy": "Consult a healthcare provider for diagnosis and treatment options, which may include antiviral medications."
        },
        "chronic obstructive pulmonary disease (COPD)": {
            "reason": "COPD is a progressive lung disease that makes it hard to breathe, often caused by smoking.",
            "remedy": "Quit smoking, use bronchodilators as prescribed, and consult a healthcare provider for management."
        },
        "multiple sclerosis": {
            "reason": "Multiple sclerosis (MS) is an autoimmune disease that affects the central nervous system.",
            "remedy": "Consult a neurologist for diagnosis and treatment options, which may include medications to manage symptoms."
        },
        "Parkinson's disease": {
            "reason": "Parkinson's disease is a progressive neurological disorder that affects movement.",
            "remedy": "Consult a neurologist for diagnosis and treatment options, which may include medications and physical therapy."
        },
        "Alzheimer's disease": {
            "reason": "Alzheimer's disease is a progressive neurodegenerative disorder that affects memory and cognitive function.",
            "remedy": "Consult a neurologist for diagnosis and treatment options, which may include medications to manage symptoms."
        },
        "bipolar disorder": {
            "reason": "Bipolar disorder is a mental health condition characterized by extreme mood swings.",
            "remedy": "Consult a mental health professional for diagnosis and treatment options, which may include therapy and medication."
        },
        "schizophrenia": {
            "reason": "Schizophrenia is a severe mental disorder that affects how a person thinks, feels, and behaves.",
            "remedy": "Consult a mental health professional for diagnosis and treatment options, which may include antipsychotic medications."
        },
        "autism spectrum disorder": {
            "reason": "Autism spectrum disorder (ASD) is a developmental disorder that affects communication and behavior.",
            "remedy": "Consult a healthcare provider for diagnosis and treatment options, which may include therapy and support services."
        },
        "attention deficit hyperactivity disorder (ADHD)": {
            "reason": "ADHD is a neurodevelopmental disorder characterized by inattention, hyperactivity, and impulsivity.",
            "remedy": "Consult a healthcare provider for diagnosis and treatment options, which may include behavioral therapy and medication."
        },
        "obsessive-compulsive disorder (OCD)": {
            "reason": "OCD is a mental health condition characterized by obsessive thoughts and compulsive behaviors.",
            "remedy": "Consult a mental health professional for diagnosis and treatment options, which may include therapy and medication."
        },
        "heart attack": {
            "reason": "A heart attack occurs when blood flow to a part of the heart is blocked, often by a blood clot.",
            "remedy": "Seek immediate medical attention. Treatment may include medications, angioplasty, or surgery."
        },
        "stroke": {
            "reason": "A stroke occurs when blood flow to the brain is interrupted, often caused by a blood clot or bleeding.",
            "remedy": "Seek immediate medical attention. Treatment may include medications or surgery."
        },
        "kidney disease": {
            "reason": "Kidney disease can be caused by diabetes, high blood pressure, or other conditions that damage the kidneys.",
            "remedy": "Consult a nephrologist for diagnosis and treatment options, which may include lifestyle changes and medications."
        },
        "liver cirrhosis": {
            "reason": "Liver cirrhosis is scarring of the liver caused by various factors including alcohol use and viral hepatitis.",
            "remedy": "Consult a hepatologist for diagnosis and treatment options, which may include lifestyle changes and medications."
        },
        "gastroesophageal reflux disease (GERD)": {
            "reason": "GERD is a chronic digestive condition where stomach acid or bile irritates the food pipe lining.",
            "remedy": "Avoid trigger foods, eat smaller meals, and consider over-the-counter antacids."
        },
    }

    # Generate a response based on the user's input
    condition = prompt.lower()  # Convert input to lowercase for matching
    if condition in medical_data:
        reason = medical_data[condition]["reason"]
        remedy = medical_data[condition]["remedy"]
        response = f"Reason: {reason}\n\nSuggestion: {remedy}"
    else:
        response = "I'm sorry, I don't have information about that condition. Please consult a medical professional."

    # Debugging: Print the generated response
    print(f"Debug: Generated response: {response}")

    return response