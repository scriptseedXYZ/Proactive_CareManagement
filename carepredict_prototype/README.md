# CarePredict Prototype

This is a workable prototype designed for stakeholder demonstrations. It features a clickable UI built with Streamlit, showcasing patient risk distributions and detailed AI-generated clinical insights.

## Running the Prototype
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `streamlit run app.py`

## Future Architecture Integration
* **Data Streams:** Mocked data can be replaced by actual data streams (e.g., AWS S3 or AWS Glue) by modifying `src/data_streams.py`.
* **AI Logic:** The placeholder ML and GenAI functions in `app.py` can be routed directly to your RAG pipeline via `src/rag_pipeline.py`.
