start:
	python visulast/run.py

act:
	source activate visulast

clean_out:
	rm -r out/* &&

clean_logs:
	rm -r logs/* &&

clean_prjcache:
	rm -r cache/* &&

clean_pycache:
	find . -name "*.pyc" -exec rm -f {} \

install_reqs:
	conda install --file requirements.txt

export_reqs:
	conda list --export > requirements.txt

create_env:
	conda env create -f environment.yaml

export_env:
	conda env export > environment.yaml

build_container:
	docker build -t visulast .
