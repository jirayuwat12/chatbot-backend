format-all:
	isort .
	black . -l 120

test:
	pytest -v

run-dev:
	cd backend && uvicorn main:app --reload

run-prod:
	cd backend && uvicorn main:app

setup-cloud:
	sudo apt install git
	mkdir -p ~/miniconda3
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
	bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
	rm ~/miniconda3/miniconda.sh
	source ~/miniconda3/bin/activate
	conda init --all
	conda create -n chatbot-backend python=3.11
	conda activate chatbot-backend
	pip install -r requirements.txt
