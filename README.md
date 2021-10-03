# tabel-generator
##Build & Run


```console
pip install -r requirements.txt
cd src  
python main.py [-h] [--seed SEED] --columns_info COLUMNS_INFO [COLUMNS_INFO ...] [--conditions CONDITIONS [CONDITIONS ...]] file
```

## Build & Run from Docker
```
sudo docker build -t generator .
sudo docker run -v "$(pwd)"/output:/code/output generator python ./main.py output/out.txt [--seed SEED] --columns_info COLUMNS_INFO [COLUMNS_INFO ...] [--conditions CONDITIONS [CONDITIONS ...]]
```