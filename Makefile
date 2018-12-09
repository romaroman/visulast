start_it:
	python src/main.py

clean_output:
	rm -r out/* &&

clean_logs:
	rm -r logs/* &&

clean_projcache:
	rm -r cache/* &&

clean_pycache:
	find . -name "*.pyc" -exec rm -f {} \

start_sample:
	python src/main.py -u username -l 20

install_requirements:
	conda install --file requirements.txt

export_requirements:
	conda list --export > requirements.txt

create_environment:
	conda env create -f environment.yml

export_environment:
	conda env export > environment.yml

start_bot:
	python src/bot.py

build_image:
	docker build -t visualast .
