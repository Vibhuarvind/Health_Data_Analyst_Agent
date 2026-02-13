def get_schema_info():
    """
    Returns schema metadata for LLM context.
    Provides detailed column descriptions and value ranges/types.
    """
    return {
        "df1": {
            "description": "Patient Health Metrics (N=2000)",
            "columns": {
                "Patient_Number": "Unique ID for patient",
                "Blood_Pressure_Abnormality": "0=Normal, 1=Abnormal",
                "Level_of_Hemoglobin": "Hemoglobin level (g/dl)",
                "Genetic_Pedigree_Coefficient": "Disease risk score (0-1)",
                "Age": "Patient age in years",
                "BMI": "Body Mass Index",
                "Sex": "0=Male, 1=Female",
                "Pregnancy": "0=No, 1=Yes",
                "Smoking": "0=No, 1=Yes",
                "salt_content_in_the_diet": "Daily salt intake (mg)",
                "alcohol_consumption_per_day": "Daily alcohol intake (ml)",
                "Level_of_Stress": "1=Low, 2=Normal, 3=High",
                "Chronic_kidney_disease": "Target Variable: 0=No, 1=Yes",
                "Adrenal_and_thyroid_disorders": "0=No, 1=Yes"
            }
        },
        "df2": {
            "description": "Physical Activity Data (N=20,000, 10 days per patient)",
            "columns": {
                "Patient_Number": "Foreign key to join with df1",
                "Day_Number": "Day index (1-10)",
                "Physical_activity": "Number of steps taken per day"
            }
        },
        "relationships": {
            "join_key": "Patient_Number",
            "join_type": "One-to-Many (df1 has 1 record per patient, df2 has 10)"
        }
    }
