FROM ubuntu:22.04

# Install Python, pip, and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /my_app

COPY . .

RUN pip3 install -r requirements.txt


#CMD ["sh", "-c", "(python3 src/option_chain.py &) && streamlit run src/display_oc.py --server.port=8501 --server.address=0.0.0.0"]
#CMD ["python3", "src/main.py"]
CMD python3 src/main.py
