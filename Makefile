build-grpc:
	 python -m grpc_tools.protoc -I=./ --python_out=./ --grpc_python_out=./  ./proto/map_sessions_service.proto

run:
	python -m app.main

black:
	black -l50 .

docker:
	docker build -t smbrine/tm-map-sessions:v1 .
	docker push smbrine/tm-map-sessions:v1

postgres:
	docker run -ePOSTGRES_PASSWORD=password -p5432:5432 postgres