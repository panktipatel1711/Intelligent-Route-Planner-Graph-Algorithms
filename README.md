# Intelligent Route Planner Engine Using Graph Algorithms
A high-performance routing framework that models urban transit spaces as weighted directed topologies.

## 💻 Technical Setup Guide
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python -m src.data_builder
python -m uvicorn src.app:app --reload
```