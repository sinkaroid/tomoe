install:
	pip install -r requirements.txt

tomoe: 
	python -m unittest test.test_build

nhentai:
	tomoe --nhentai 255369

pururin:
	tomoe --pururin 47226

hentaifox:
	tomoe --hentaifox 59026

hentai2read:
	tomoe --hentai2read chaldea_life 1

simply:
	tomoe --simply "fate-grand-order/perros"

qhentai:
	tomoe --qhentai "eight-star-sand"
	
api-mock: # check api if something down
	python -m unittest test.test_api

upload:
	bash build.sh